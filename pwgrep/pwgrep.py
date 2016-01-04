#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import re
import signal
import sys

import command_parser
import file_helper
import printer_helper
import search_helper


def print_match(filename, line, regex, no_filename=False,
                file_is_binary=False, color=False, print_only_match=False):
    if file_is_binary:
        printer_helper.print_binary_match(filename)
    else:
        printer_helper.print_text_match(filename, line, regex, color,
                                        no_filename)


def search_in_file(filename, regex, invert_match, no_filename, color):
    any_match = False
    if file_helper.file_is_binary(filename):
        if search_helper.search_in_binary_file(filename, regex, invert_match):
            any_match = True
            print_match(filename, None, regex, no_filename,
                        True, color)
    else:
        for linenr, line in search_helper.search_in_text_file(filename,
                                                              regex,
                                                              invert_match):
            any_match = True
            print_match(filename, line, regex, no_filename,
                        False, color)
    return any_match


def progress_stdin(regex, invert_match=False, color=False):
    any_match = False
    for line_nr, line in search_helper.search_in_stdin(regex, invert_match):
        any_match = True
        print_match('', line, regex, True, False, color)
    return any_match


def progress_commandline(files, regex, invert_match=False, color=False,
                         recursive=False, dereference_recursive=False,
                         no_filename=False):
    any_match = False
    for file in files:
        if file_helper.file_is_directory(file):
            if not (dereference_recursive or recursive):
                print('pwgrep: {}: is a directory'.format(file))
            else:
                for filename in file_helper.recurse(file,
                                                    dereference_recursive):

                    if search_in_file(filename, regex,
                                      invert_match,
                                      no_filename, color):
                        any_match = True

        else:
            if search_in_file(file, regex, invert_match,
                              no_filename, color):
                any_match = True
    return any_match


def main(args):
    p = command_parser.CommandParser(args)

    regex_flags = 0
    if p.options.ignore_case:
        regex_flags |= re.IGNORECASE

    regex = re.compile(p.options.PATTERN[0], regex_flags)

    if not p.options.PATH:
        return progress_stdin(regex, p.options.invert_match, p.color)
    else:
        return progress_commandline(p.options.PATH, regex,
                                    p.options.invert_match,
                                    p.color,
                                    p.options.recursive,
                                    p.options.dereference_recursive,
                                    p.options.no_filename)


def signal_terminal_handler(signal_nr, frame):
    sys.exit(128 + signal_nr)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_terminal_handler)

    try:
        any_match = main(sys.argv)
    except KeyboardInterrupt:
        sys.exit(1)

    if any_match:
        sys.exit(0)
    sys.exit(1)
