inherit module

inherit elepi-quest

SRC_URI += " \
    file://kernel-module/ \
    \
    file://prerm.sh \
"

QUEST_PRERM_SCRIPTS = "prerm.sh"

S = "${WORKDIR}/kernel-module"