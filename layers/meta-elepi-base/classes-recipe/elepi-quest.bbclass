SUMMARY = "Base class for creating quests."

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

QUEST_DESCRIPTION[doc]      = "Describes the goal to achieve in this quest and first pointers how to get there."
QUEST_HINT_FILES[doc]       = "List of files to be deployed as hints. Note: The order in the filesystem will be used, \
                               so prefix the files numerically if you want a particular one."
QUEST_VERIFICATION_KEY[doc] = "The public key used to verify the signature of the generic solution token \
                               used for all quests (see quest-solution-token.txt). Defaults to a file named 'verification.key'."
QUEST_SETUP_SCRIPTS[doc]    = "Scripts to be deployed on the device and executed when the quest is started."
QUEST_CLEANUP_SCRIPTS[doc]  = "Scripts to be deployed on the device and executed when the quest was completed." 

QUEST_VERIFICATION_KEY ?= "${WORKDIR}/verification.key"

# Create a subpackage that only pulls in the dependencies defined in the recipe.
# This allows to install the dependencies without the actual quest.
PACKAGES += "${PN}-deps"
ALLOW_EMPTY:${PN}-deps = "1"

# Note: We need to use the __anonymous() function to ensure that the variables
# are only read after the recipe has been parsed and variable expansion is complete.
python __anonymous() {
    description = d.getVar('QUEST_DESCRIPTION')
    verification_key = d.getVar('QUEST_VERIFICATION_KEY')

    if not description or not verification_key:
        bb.fatal('Please provide both a description and a verification key for the quest.')

    quest_name = d.getVar('PN')
    dependencies = d.getVar('RDEPENDS:' + quest_name)

    if dependencies:
        d.setVar('RDEPENDS:' + quest_name + '-deps', dependencies)
        d.delVar('RDEPENDS:' + quest_name)
}

do_install:append() {
    install -d ${D}${datadir}/elepi/quest

    echo "${QUEST_DESCRIPTION}" > ${D}${datadir}/elepi/quest/description.txt
    install -m 0644 "${QUEST_VERIFICATION_KEY}" ${D}${datadir}/elepi/quest/verification.key

    install -d ${D}${datadir}/elepi/quest/hints
    for hint_file in ${QUEST_HINT_FILES}; do
        install -m 0644 ${hint_file} ${D}${datadir}/elepi/quest/hints/
    done

    install -d ${D}${datadir}/elepi/quest/hooks
    install -d ${D}${datadir}/elepi/quest/hooks/setup
    for setup_script in ${QUEST_SETUP_SCRIPTS}; do
        install -m 0755 ${setup_script} ${D}${datadir}/elepi/quest/hooks/setup/
    done
    install -d ${D}${datadir}/elepi/quest/hooks/cleanup
    for cleanup_script in ${QUEST_CLEANUP_SCRIPTS}; do
        install -m 0755 ${cleanup_script} ${D}${datadir}/elepi/quest/hooks/cleanup/
    done
}

# As setup scripts may depend on runtime properties of the system, we use the _ontarget
# variant of the function.
# Note that special care needs to be taken if read-only rootfs is introduced (see 
# https://lists.openembedded.org/g/openembedded-core/topic/patch_rootfs_run_postinst/107227142 
# for a required fix of IMAGE_FEATURES += "read-only-rootfs read-only-rootfs-delayed-postinsts").
pkg_postinst_ontarget:${PN} () {
    for script in ${datadir}/elepi/quest/hooks/setup/*; do
        if [ -x "${script}" ]; then
            "${script}"
        fi
    done
}

pkg_prerm:${PN} () {
    for script in ${datadir}/elepi/quest/hooks/cleanup/*; do
        if [ -x "${script}" ]; then
            "${script}"
        fi
    done
}

FILES:${PN} += " \
    ${datadir}/elepi/quest/* \
"