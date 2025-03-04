#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

SOLUTION_TOKEN_PATH="${SCRIPT_DIR}/../../layers/meta-elepi-base/recipes-core/elepictl/files/solution.token"
WORKDIR="${SCRIPT_DIR}/../../work/quest-keys"

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <quest-name>"
    exit 1
fi

QUEST_NAME="$1"
KEY_LEN=2048

mkdir -p "${WORKDIR}"

# Create private and public keys
openssl genrsa -out "${WORKDIR}/${QUEST_NAME}.key" ${KEY_LEN}
openssl rsa -in "${WORKDIR}/${QUEST_NAME}.key" -pubout -out "${WORKDIR}/${QUEST_NAME}.verification.key"

# Create the solution signature (both binary and as hex representation)
echo "Creating solution signatures"
openssl dgst -sha512 -sign "${WORKDIR}/${QUEST_NAME}.key" -out "${WORKDIR}/${QUEST_NAME}-solution.sign" "${SOLUTION_TOKEN_PATH}"
xxd -p "${WORKDIR}/${QUEST_NAME}-solution.sign" "${WORKDIR}/${QUEST_NAME}-solution.hex"

# Verify the created signatures
openssl dgst -sha512 -verify "${WORKDIR}/${QUEST_NAME}.verification.key" -signature "${WORKDIR}/${QUEST_NAME}-solution.sign" "${SOLUTION_TOKEN_PATH}"
xxd -r -p "${WORKDIR}/${QUEST_NAME}-solution.hex" | openssl dgst -sha512 -verify "${WORKDIR}/${QUEST_NAME}.verification.key" -signature /dev/stdin "${SOLUTION_TOKEN_PATH}"