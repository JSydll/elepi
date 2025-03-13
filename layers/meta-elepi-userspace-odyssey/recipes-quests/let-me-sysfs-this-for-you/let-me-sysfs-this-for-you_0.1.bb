inherit elepi-quest

QUEST_HINTS_DIR = ""

SRC_URI += " \
    file://solution.hex \
"

# For the first spike, simply deploy the solution to somewhere in the system.
do_install() {
    install -d ${D}${datadir}
    install -m 0644 ${WORKDIR}/solution.hex ${D}${datadir}/solution.hex
}

FILES:${PN} += "${datadir}/solution.hex"