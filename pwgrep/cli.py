#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import signal
import sys

from pwgrep import command_parser
from pwgrep import process


def run(args):
    """
    Processes input  and performs grep operations
    :param args: command line parameters (except [0], i.e. program name)
    :return: if any match was found in file
    """
    parser = command_parser.CommandParser(args)

    regex_flags = 0
    if parser.options.ignore_case:
        regex_flags |= re.IGNORECASE
    regex_txt = re.compile(parser.options.PATTERN[0], regex_flags)
    regex_bin = re.compile(str.encode(parser.options.PATTERN[0]),
                           regex_flags)

    if not parser.options.PATH:
        return process.process_stdin(regex_txt, parser.options.invert_match,
                                     parser.color)
    else:
        return process.process_commandline(parser.options.PATH,
                                           regex_txt,
                                           regex_bin,
                                           parser.options.invert_match,
                                           parser.color,
                                           parser.options.recursive,
                                           parser.options.dereference_recursive,
                                           parser.options.no_filename)


def signal_terminal_handler(signal_nr, frame):
    """
    Handler for signals; Quits program with correct exit code
    :param signal_nr: signal nr of received signal
    :param frame: -
    :return:
    """
    sys.exit(128 + signal_nr)


def main(args=sys.argv[1:]):
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
