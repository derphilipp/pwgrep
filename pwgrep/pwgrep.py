#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import re
import string
import sys
import signal

import file_helper
import command_parser
import colors


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


def print_binary(filename):
    print('Binary file {} matches'.format(filename))


def replacement(match):
    return '{}{}{}'.format(colors.bcolors.MATCH, match.group(),
                           colors.bcolors.ENDC)


def format_printline(filename, line, regex, color):
    line = string.strip(line)
    if color:
        filename = colors.bcolors.CYAN + filename + colors.bcolors.ENDC
        line = regex.sub(replacement, line)
    return filename, line


def print_match(filename, line, regex, do_not_display_filename=False,
                file_is_binary=False, color=False, print_only_match=False):
    # TODO: Print in colors
    if file_is_binary:
        print_binary(filename)
        return

    filename, line = format_printline(filename, line, regex, color)
    if do_not_display_filename:
        print(line)
    else:
        print('{}:{}'.format(filename, line))


def main(args):
    p = command_parser.CommandParser(args)
    regex = build_regex(p.options.PATTERN[0], p.options.ignore_case)
    any_match = False
    for file in filelist(p.options.PATH):
        if file_helper.file_is_binary(file):
            if search_in_binary_file(file, regex, p.options.invert_match):
                any_match = True
                print_match(file, None, regex, p.options.no_filename,
                            True, p.color)
        else:
            for linenr, line in search_in_text_file(file, regex,
                                                    p.options.invert_match):
                any_match = True
                print_match(file, line, regex, p.options.no_filename,
                            False, p.color)

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
