#!/bin/sh
# Explicit kernel module activation to support runtime package
modprobe kfrag
# Account for the service being activated before this script is executed
systemctl is-failed honeypot &> /dev/null || systemctl --no-block restart honeypot