#!/usr/bin/env python3
"""
Commandline application to control the elePi adventure.

Interacts with the privileged dbus service to perform
actual commands.
"""

import argparse
import textwrap

from pydbus import SystemBus as DBus

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Application to interact with the current elePi adventure.")
        
    command_parsers = parser.add_subparsers(dest="command")
    command_parsers.add_parser(
        "info", help="Show information about the current quest.")
    command_parsers.add_parser("hint",
                               help="Show the next hint for the current quest.")
    command_parsers.add_parser(
        "reset", help="Reset the state of the device to begin the quest again.")

    solve_parser = command_parsers.add_parser("solve",
                                              help=("Solve the current quest by providing a hex code."
                                                    "If correct, the next quest will be initiated."))
    solve_parser.add_argument(
        "solution_code", type=str, help="The solution code for the current quest.")

    args = parser.parse_args()

    bus = DBus()
    elepictl = bus.get('org.elepi.elepictl')

    if args.command == "info":
        print(elepictl.info())

    elif args.command == "hint":
        print(elepictl.hint())

    elif args.command == "reset":
        print(textwrap.dedent("""
        Resetting the state of the current quest...
        Note that any changes not belonging to the quest might stay around.
        """))
        if elepictl.reset_quest():
            print("Done! You can start tinkering again.")

    elif args.command == "solve":
        success, msg = elepictl.verify_quest(args.solution_code)
        print(msg)
        if success:
            # TODO: Decide whether the return code should be checked here
            _, msg = elepictl.complete_quest()
            print(msg)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
