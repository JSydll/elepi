#!/bin/bash

echo "First elePi quest solution code fragment: $(cat /proc/kfragments)" > /dev/kmsg 

# todo: Refactor this script to request the other code fragments
# from the kfrag module (echo "wake" > /proc/kfragments)