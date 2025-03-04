#!/usr/bin/env python3

import argparse
from elepictl.elepictl import ElePiCtl


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Application to interact with the current elePi quest.")
        
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

    ctl = ElePiCtl()

    if args.command == "info":
        ctl.info()
    elif args.command == "hint":
        ctl.hint()
    elif args.command == "reset":
        ctl.reset()
    elif args.command == "solve":
        ctl.solve(args.solution_code)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
