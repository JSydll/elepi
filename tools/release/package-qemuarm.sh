#!/bin/bash -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
readonly SCRIPT_DIR

if [ $# -lt 1 ]; then
    echo "Please provide the adventure image name to package."
    exit 1
fi
ADVENTURE_IMAGE_NAME="$1"
OUTPUT_DIR="$2"
DO_CLEAN="$3"

readonly BUILD_ARTIFACTS="${SCRIPT_DIR}/../../work/build/tmp/deploy/images/qemuarm64"
readonly ADVENTURE_IMAGE_ALIAS="adventure-image.qcow2"
readonly PACKAGE_NAME="${ADVENTURE_IMAGE_NAME//-image}-qemuarm.tar.bz2"

STAGING_DIR="$(mktemp -d)"
ARCHIVE_DIR="${STAGING_DIR}/archive"
mkdir "${ARCHIVE_DIR}"

cp "${SCRIPT_DIR}"/qemuarm/*        "${ARCHIVE_DIR}"/
cp "${BUILD_ARTIFACTS}"/bootenv.img "${ARCHIVE_DIR}"/
cp "${BUILD_ARTIFACTS}"/u-boot.bin  "${ARCHIVE_DIR}"/

cp "${BUILD_ARTIFACTS}/${ADVENTURE_IMAGE_NAME}"-qemuarm64.rootfs.wic.qcow2 \
   "${ARCHIVE_DIR}/${ADVENTURE_IMAGE_ALIAS}"

tar -acf "${STAGING_DIR}/${PACKAGE_NAME}" -C "${ARCHIVE_DIR}" . 

if [ ! -d "${OUTPUT_DIR}" ]; then
    echo "No (valid) output directory path specified - you can find the package in ${STAGING_DIR}."
    exit 0
fi

cp "${STAGING_DIR}/${PACKAGE_NAME}" "${OUTPUT_DIR}"

if [ -n "${DO_CLEAN}" ]; then
    rm -rfd "${STAGING_DIR}"
    exit 0
fi
echo "Kept staging dir ${STAGING_DIR}. Please remove manually or let the next reboot do this."
