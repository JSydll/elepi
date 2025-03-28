SUMMARY     = "Provides the elepictl application used to work on the embedded linux learning quests."
DESCRIPTION = "The elepictl application provides information on the currently active quest, such as \
               the quest description and hints, is used to verify the solution of the quest and \
               activates the next quest on successful completion."
HOMEPAGE    = "https://github.com/JSydll/elepi"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# This might be set to a local source path during development. Make sure to set S appropriately.
PYTHON_SOURCES = "git://github.com/JSydll/elepi.git;protocol=https;branch=main;subpath=src/elepictl"

SRC_URI = " \
    ${PYTHON_SOURCES} \
    \
    file://dbus/org.elepi.elepictl.conf \
    file://systemd/elepid.service \
    file://solution.token \
"
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/elepictl"

inherit setuptools3 systemd

RDEPENDS:${PN} = " \
    python3-core \
    python3-json \
    python3-pydbus \
    \
    dnf \
    openssl \
    xxd \
"

do_install:append() {
    install -d ${D}${datadir}/elepi/adventure
    install -m 0640 ${WORKDIR}/solution.token ${D}${datadir}/elepi/adventure/

    install -d ${D}${datadir}/dbus-1/system.d
    install -m 0640 ${WORKDIR}/dbus/org.elepi.elepictl.conf ${D}${datadir}/dbus-1/system.d/

    install -d ${D}${systemd_system_unitdir}
    install -m 0640 ${WORKDIR}/systemd/elepid.service ${D}${systemd_system_unitdir}/
}

SYSTEMD_SERVICE:${PN} = "elepid.service"

FILES:${PN} += " \
    ${datadir}/elepi/adventure/solution.token \
    ${datadir}/dbus-1/system.d/org.elepi.elepictl.conf \
    ${systemd_system_unitdir}/elepid.service \
"