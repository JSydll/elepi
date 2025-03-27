FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

do_install:append() {
    rm ${D}${sysconfdir}/motd
}