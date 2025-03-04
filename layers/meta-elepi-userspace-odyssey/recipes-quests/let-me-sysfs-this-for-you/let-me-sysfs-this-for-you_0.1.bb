inherit elepi-quest

QUEST_DESCRIPTION = "Enable a kernel module that exposes a sysfs (to be queried for the solution)"
QUEST_HINT_FILES  = ""

SRC_URI = " \
    file://verification.key \
    file://solution.hex \
"

# For the first spike, simply deploy the solution to somewhere in the system.
do_install() {
    install -d ${D}${datadir}
    install -m 0644 ${WORKDIR}/solution.hex ${D}${datadir}/solution.hex
}

FILES:${PN} += "${datadir}/solution.hex"