#!/bin/bash

cat /proc/kfragments > /dev/klog 

# todo: Refactor this script to request the other code fragments
# from the kfrag.ko...