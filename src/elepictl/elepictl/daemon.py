#!/usr/bin/env python3
"""
Background daemon to control the elePi adventure.

Exposes a dbus service to allow user interactions
without root privileges.
"""

from pydbus import SystemBus as DBus
from gi.repository import GLib

from elepictl.elepictl import ElePiCtl

def main() -> None:
    bus = DBus()
    bus.publish("org.elepi.elepictl", ElePiCtl())

    loop = GLib.MainLoop()
    loop.run()


if __name__ == "__main__":
    main()