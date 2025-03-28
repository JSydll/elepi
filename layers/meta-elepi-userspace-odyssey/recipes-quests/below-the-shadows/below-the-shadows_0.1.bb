inherit cmake
inherit systemd

inherit elepi-quest

SRC_URI += " \
    file://sources/ \
    \
    file://configs/app.ini \
    file://configs/logging.ini \
    \
    file://systemd/weirdo.service \
"

QUEST_SUDO_PERMISSIONS = "NOPASSWD: /usr/bin/mount, /usr/bin/umount, /usr/bin/bash"

S = "${WORKDIR}/sources"

EXTRA_OECMAKE = ""

do_install:append() {
    install -d ${D}${datadir}/ole

    install -d ${D}${datadir}/ole/defaults
    install -m 0644 ${WORKDIR}/configs/app.ini ${D}${datadir}/ole/defaults/

    install -d ${D}${datadir}/ole/user
    install -d ${D}${datadir}/ole/user/required
    install -m 0666 ${WORKDIR}/configs/logging.ini ${D}${datadir}/ole/user/required/
    install -d -m 0777 ${D}${datadir}/ole/user/extra

    install -d ${D}${systemd_system_unitdir}
    install -m 0640 ${WORKDIR}/systemd/weirdo.service ${D}${systemd_system_unitdir}/
}

SYSTEMD_SERVICE:${PN} = "weirdo.service"

FILES:${PN} += " \
    ${datadir}/ole/* \
    ${systemd_system_unitdir}/weirdo.service \
"