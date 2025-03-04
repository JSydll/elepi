
inherit elepi-quest

QUEST_DESCRIPTION = "Reveal a file shadowed in an underlay"
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