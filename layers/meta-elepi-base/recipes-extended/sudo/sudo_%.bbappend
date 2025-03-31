# By default, the elepi user available in elepi-adventure-images has no root privileges.
#
# To allow per-quest elevation of privileges, we add a sudoers.d directory to the quest,
# enabling it to set privileges individually.

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://sudoers.d/elepi.in \
"

do_configure:append() {
    sed -e "s|@@ELEPI_USER@@|${ELEPI_USER}|" "${UNPACKDIR}/sudoers.d/elepi.in" > "${WORKDIR}/elepi.sudoers"
}

do_install:append() {
    install -m 0644 ${WORKDIR}/elepi.sudoers ${D}${sysconfdir}/sudoers.d/elepi
}