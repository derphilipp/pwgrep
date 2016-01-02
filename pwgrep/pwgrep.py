#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import re
import string
import sys
import signal

import file_helper
import command_parser
import version


def build_regex(regex, ignore_case=False):
    if ignore_case:
        return re.compile(regex, flags=re.IGNORECASE)
    return re.compile(regex)


def lines_from_file(filename):
    try:
        file = open(filename, 'r')
        for linenr, line in enumerate(file):
            yield linenr, line
    except IOError:
        print ('pwgrep: {}: Permission denied'.format(filename))


def search_in_text_file(filename, regex, invert_search):
    for linenr, line in lines_from_file(filename):
        if invert_search != bool(regex.search(line)):
            yield linenr, line


def search_in_binary_file(filename, regex, invert_search):
    for _, line in lines_from_file(filename):
        if invert_search != bool(regex.search(line)):
            return True
    return False


def filelist(startpoint):
    # TODO Build in recursion etc.
    for element in startpoint:
        yield element


def display_version():
    print("Version {}".format(version.VERSION))


def print_match(filename, line, regex, do_not_display_filename=False,
                file_is_binary=False):
    # TODO: Print in colors
    # TODO: Print binary files differently

    if file_is_binary:
        print('Binary file {} matches'.format(filename))
    elif do_not_display_filename:
        print(string.strip(line))
    else:
        print('{}:{}'.format(filename, string.strip(line)))


def main(args):
    p = command_parser.CommandParser(args)
    regex = build_regex(p.options.PATTERN[0], p.options.ignore_case)
    any_match = False
    for file in filelist(p.options.PATH):
        if file_helper.file_is_binary(file):
            if search_in_binary_file(file, regex, p.options.invert_match):
                any_match = True
                print_match(file, None, regex, p.options.no_filename,
                            file_is_binary=True)
        else:
            for linenr, line in search_in_text_file(file, regex,
                                                    p.options.invert_match):
                any_match = True
                print_match(file, line, regex, p.options.no_filename,
                            file_is_binary=False)

    if any_match:
        return 0
    else:
        return 1


def signal_terminal_handler(signal, frame):
    # TODO: Test all this
    print 'got SIGTERM'
    sys.exit(123)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_terminal_handler)

    try:
        result = main(sys.argv)
    except KeyboardInterrupt:
        sys.exit(1)

    sys.exit(result)
