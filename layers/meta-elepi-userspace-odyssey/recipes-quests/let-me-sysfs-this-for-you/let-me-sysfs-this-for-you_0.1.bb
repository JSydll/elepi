inherit module

inherit elepi-quest

SRC_URI += " \
    file://kernel-module/ \
    file://bin/elepi-fragment-select.sh \
    \
    file://prerm.sh \
"

RDEPENDS:${PN} = "bash"

QUEST_PRERM_SCRIPTS = "prerm.sh"
QUEST_SUDO_PERMISSIONS = "NOPASSWD: /usr/sbin/modprobe, /usr/bin/elepi-fragment-select"

S = "${WORKDIR}/kernel-module"

do_install:append() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/bin/elepi-fragment-select.sh ${D}${bindir}/elepi-fragment-select
}

FILES:${PN} += " \
    ${bindir}/elepi-fragment-select \
"