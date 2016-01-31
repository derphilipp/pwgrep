#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys

from pwgrep import commandline_parser
from pwgrep import process


def run(args):
    """
    Process input  and performs grep operations.

    :param args: command line parameters (except [0], i.e. program name)
    :return: if any match was found in file
    """
    parser_result = commandline_parser.CommandLineParser().parse(args)
    grepper = process.Grepper(parser_result)

    any_match = False
    if not parser_result.options.PATH:
        for match in grepper.grep_stdin():
            any_match = True
    else:
        for match in grepper.grep_files_from_commandline():
            any_match = True
    return any_match


def signal_terminal_handler(signal_nr, _):
    """
    Handler for signals; Quits program with correct exit code.

    :param signal_nr: signal nr of received signal
    :param _: frame, unused
    :return:
    """
    sys.exit(128 + signal_nr)


def main(args=sys.argv[1:]):
    """
    Main loop of program; Processes args; quits towards system with exit code.

    :param args: Command line parameters
    :return:
    """
    signal.signal(signal.SIGTERM, signal_terminal_handler)

    try:
        any_match = run(args)
    except KeyboardInterrupt:
        sys.exit(1)

    if any_match:
        sys.exit(0)
    sys.exit(1)


if __name__ == '__main__':
    main()
