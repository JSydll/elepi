FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://boot.cmd.in.patch;patchdir=${WORKDIR} \
"