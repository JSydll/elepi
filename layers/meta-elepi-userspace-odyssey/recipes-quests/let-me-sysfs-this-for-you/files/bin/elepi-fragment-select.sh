#!/bin/bash
#
# Allows everyone having sudo rights for this wrapper to write
# to the root-owned sysfs entry. This avoids more permissive configurations.

if [[ ${EUID} -ne 0 ]]; then
    echo "This must be executed with root privileges!"
    exit 1
fi

echo "$1" > /sys/kernel/elepi/select

