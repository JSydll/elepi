#!/bin/sh
# Unload the module from the kernel's memory
modprobe -r elepi_sysfs >/dev/null 2>&1 || true