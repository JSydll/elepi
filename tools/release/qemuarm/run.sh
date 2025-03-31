#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
readonly SCRIPT_DIR

readonly REQUIREMENTS_SPEC="requirements.txt"
readonly RELEASE_CONTENTS="adventure-image.qcow2 bootenv.img u-boot.bin"

function print_help() {
    cat <<EOF
Options:
    --discard-changes   Do not persist changes in the bootenv and adventure-image image files.
    --ssh-port          Port exported by QEMU to ssh into the emulated device.
    -h|--help           Print this help.       
EOF
}

# Sanity checks
for file in ${RELEASE_CONTENTS}; do
  if [ ! -f "${SCRIPT_DIR}/${file}" ]; then
    echo "Could not find all files expected to be found in the release - are you running in the unpacked directory?"
    exit 1
  fi
done

while read -r pkg; do
  if ! command -v ${pkg} &>/dev/null; then
    echo "Missing dependency (${pkg})! Please install all packages from the ${REQUIREMENTS_SPEC}." 
    exit 2
  fi
done < "${SCRIPT_DIR}/${REQUIREMENTS_SPEC}"

# Argument parsing
EXPOSED_SSH_PORT="2222"

while [[ $# -gt 0 ]]; do
  case $1 in
    --ssh-port)
      EXPOSED_SSH_PORT="$2"
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
  shift
done

# Start the emulation
qemu-system-aarch64 \
    -device virtio-net-pci,netdev=net0,mac=52:54:00:12:35:02 \
    -netdev user,id=net0,hostfwd=tcp:127.0.0.1:${EXPOSED_SSH_PORT}-:22 \
    -object rng-random,filename=/dev/urandom,id=rng0 \
    -device virtio-rng-pci,rng=rng0 \
    -drive id=disk0,file=${SCRIPT_DIR}/adventure-image.qcow2,if=none,format=qcow2 \
    -device virtio-blk-device,drive=disk0 \
    -drive if=pflash,format=raw,index=1,file=${SCRIPT_DIR}/bootenv.img \
    -machine virt -cpu cortex-a57 -smp 4 -m 3G \
    -serial mon:stdio -serial null \
    -nographic \
    -device virtio-gpu-pci \
    -bios ${SCRIPT_DIR}/u-boot.bin
