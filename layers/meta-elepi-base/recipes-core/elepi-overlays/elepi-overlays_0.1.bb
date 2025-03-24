SUMMARY     = "Sets up overlays for parts of the system that may be manipulated by elePi quests."
DESCRIPTION = "The approach is to setup the overlays in a rather broad scope, as this eases up \
               implementation of the individual quests."

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit overlayfs

# Allow writing to /usr/lib, /usr/bin and /usr/share
OVERLAYFS_WRITABLE_PATHS[data] = " \
    ${libdir} \
    ${bindir} \
    ${datadir} \
"

# TODO: Deploy overlay cleanup script + postinst_ontarget hook to be executed on first boot 
# (i.e. after update, which then only needs to clean the /etc/rpm-postinsts.d whiteouts).