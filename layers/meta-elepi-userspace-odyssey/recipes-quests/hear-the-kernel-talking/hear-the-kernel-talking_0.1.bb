# Note: Inheriting module must come first to avoid QA issues
inherit module
inherit systemd

inherit elepi-quest

SRC_URI += " \
    file://kernel-module/ \
    \
    file://sysctl.d/printk.conf \
    file://bin/honeypot.sh \
    file://systemd/honeypot.service \
"

RDEPENDS:${PN}  += "bash"

S = "${UNPACKDIR}/kernel-module"

do_install:append() {
    install -d ${D}${sysconfdir}/sysctl.d
    install -m 0644 ${UNPACKDIR}/sysctl.d/printk.conf ${D}${sysconfdir}/sysctl.d/
    
    install -d ${D}${bindir}
    # Note: The script contains a todo marker on purpose, to provide a breadcrumb to follow. 
    install -m 0755 ${UNPACKDIR}/bin/honeypot.sh ${D}${bindir}/
    # For the sake of simplicity, we use a system service here (as systemd.bbclass can
    # only enable those by default).
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${UNPACKDIR}/systemd/honeypot.service ${D}${systemd_system_unitdir}/
}

SYSTEMD_SERVICE:${PN} = "honeypot.service"

FILES:${PN} += " \
    ${sysconfdir}/sysctl.d/printk.conf \
    ${bindir}/honeypot.sh \
    ${systemd_system_unitdir}/honeypot.service \
"