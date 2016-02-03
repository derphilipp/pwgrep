#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys

from pwgrep.commandline_parser import CommandLineParser
from pwgrep.result_printer import ResultPrinter
from pwgrep.grepper import Grepper


def run(args):
    """
    Process input  and performs grep operations.

    :param args: command line parameters (except [0], i.e. program name)
    :return: if any match was found in file
    """
    parser_result = CommandLineParser().parse(args)
    grepper = Grepper(parser_result)
    printer = ResultPrinter(
        colorize=parser_result.color,
        print_filename=parser_result.print_filename,
        invert_match=parser_result.invert_match
    )

    any_match = False
    for result in grepper.grep():
        printer.print_result(result)
        if result.match:
            any_match = True
    return any_match


def signal_terminal_handler(signal_nr, _): # pragma: no cover
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
    except KeyboardInterrupt: # pragma: no cover
        sys.exit(1)

    if any_match:
        sys.exit(0)
    sys.exit(1)


if __name__ == '__main__':
    main()
