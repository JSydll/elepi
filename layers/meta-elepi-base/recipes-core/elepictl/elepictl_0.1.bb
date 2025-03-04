SUMMARY     = "Provides the elepictl application used to work on the embedded linux learning quests."
DESCRIPTION = "The elepictl application provides information on the currently active quest, such as \
               the quest description and hints, is used to verify the solution of the quest and \
               activates the next quest on successful completion."
HOMEPAGE    = "https://github.com/JSydll/elepi"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    git://github.com/JSydll/elepi.git;protocol=https;branch=main;subpath=src/elepictl \
    file://solution.token \
"
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/elepictl"

inherit setuptools3

RDEPENDS:${PN} = " \
    python3-core \
    python3-json \
    \
    dnf \
    openssl \
    xxd \
"

do_install:append() {
    install -d ${D}${datadir}/elepi/adventure
    install -m 0644 ${WORKDIR}/solution.token ${D}${datadir}/elepi/adventure/solution.token
}

FILES:${PN} += " \
    ${datadir}/elepi/adventure/solution.token \
"