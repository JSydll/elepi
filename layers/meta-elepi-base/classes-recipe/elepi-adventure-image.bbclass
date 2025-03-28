SUMMARY     = "Base class for creating an adventure image."
DESCRIPTION = "Each adventure image contains the control application to follow the installed quests \
               as well as the predefined sequence of quests contained in the adventure."

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"


QUESTS_LIST[doc] = "List of quests belonging to this adventure. \
                    Important: The order matters and will be used to enforce the sequence \
                    in which the quests need to be solved."

ADVENTURE_META_FILE = "meta.json"
ADVENTURE_META_DATA = ""

inherit core-image
inherit extrausers

# Setup /etc overlay for read-only rootfs
OVERLAYFS_ETC_MOUNT_POINT = "/data"
OVERLAYFS_ETC_FSTYPE = "ext4"
# Note: Account for legacy (msdos) partition table
OVERLAYFS_ETC_DEVICE = "/dev/mmcblk0p5"
OVERLAYFS_ETC_USE_ORIG_INIT_NAME = "0"

# Setup unprivileged user
EXTRA_USERS_PARAMS:append = " \
    groupadd --gid ${ELEPI_GID} ${ELEPI_GROUP}; \
    useradd --uid ${ELEPI_UID} --groups sudo,${ELEPI_GROUP} \
        --home-dir /home/${ELEPI_USER} --shell /usr/bin/sh \
        --password '${ELEPI_PASSWORD}' ${ELEPI_USER}; \
"

# Populate image contents
IMAGE_FEATURES += " \
    read-only-rootfs \
    read-only-rootfs-delayed-postinsts \
    overlayfs-etc \
    package-management \
"

IMAGE_INSTALL = " \
    packagegroup-core-boot \
    ${CORE_IMAGE_EXTRA_INSTALL} \
    \
    sudo \
    rauc \
    \
    elepi-overlays \
    elepictl \
"

IMAGE_FSTYPES:remove = " ext3 ext4"
IMAGE_FSTYPES:append = " squashfs"

WKS_FILE = "dual-ro-rootfs-raspberrypi.wks.in"

python __anonymous() {
    # As bitbake variable expansion does not support quoted strings well,
    # the json data is escaped with '@' characters to be replaced later.
    # Given this function is executed during parsing and the image's directory
    # structure is not yet established, the json data can also not be dumped
    # directly to a file.
    import json
    
    quests_list = d.getVar('QUESTS_LIST')
    if not quests_list:
        bb.fatal('QUESTS_LIST variable is empty. Please provide a list of quests.')
    quests = quests_list.split()

    image_pkgs = d.getVar('IMAGE_INSTALL').split()
        
    quest_package_tasks = []
    adventure_meta = {
        '@name@': '@' + d.getVar('PN') + '@',
        '@quests@': []
    }

    # Install only the dependencies of the selected quests but prepare the collection of
    # the actual quest packages to be deployed for runtime installation.
    for quest in quests:
        image_pkgs.append(quest + "-deps")
        quest_package_tasks.append(quest + ':do_package_write_rpm')
        adventure_meta['@quests@'].append({'@name@': '@' + quest + '@', '@solved@': False})
    
    # The first quest can already be deployed
    image_pkgs.append(quests[0])

    d.setVar('IMAGE_INSTALL', ' '.join(image_pkgs))
    d.setVar('QUEST_PACKAGE_TASKS', ' '.join(quest_package_tasks))
    d.setVar('ADVENTURE_META_DATA', json.dumps(adventure_meta, indent=4))
}

do_deploy_adventure_data() {
    install -d -m 0600 ${IMAGE_ROOTFS}${datadir}/elepi/adventure/quests

    for quest in ${QUESTS_LIST}; do
        find ${DEPLOY_DIR_RPM} -type f -name "${quest}-[0-9]*.rpm" -exec cp {} ${IMAGE_ROOTFS}${datadir}/elepi/adventure/quests/${quest}.rpm ';'
    done

    echo "${ADVENTURE_META_DATA}" | sed 's/@/"/g' > ${IMAGE_ROOTFS}${datadir}/elepi/adventure/${ADVENTURE_META_FILE}
}
do_deploy_adventure_data[depends] = "${QUEST_PACKAGE_TASKS}"

# The adventure data needs to be deployed before creating specific image types (such as wic).
IMAGE_PREPROCESS_COMMAND += "do_deploy_adventure_data;"


