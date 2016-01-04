#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import re
import string
import sys
import signal
import os

import file_helper
import command_parser
import colors


def build_regex(regex, ignore_case=False):
    if ignore_case:
        return re.compile(regex, flags=re.IGNORECASE)
    return re.compile(regex)


def lines_from_file(filename):
    try:
        file_object = open(filename, 'r')
        for line_nr, line in enumerate(file_object):
            yield line_nr, line
    except IOError:
        if os.path.exists(filename):
            print ('pwgrep: {}: Permission denied'.format(filename))
        else:
            print ('pwgrep: {}: No such file or directory'.format(filename))


def search_in_stdin(regex, invert_search):
    for line_nr, line in enumerate(sys.stdin):
        if invert_search != bool(regex.search(line)):
            yield line_nr, line


def search_in_text_file(filename, regex, invert_search):
    for linenr, line in lines_from_file(filename):
        if invert_search != bool(regex.search(line)):
            yield linenr, line


def search_in_binary_file(filename, regex, invert_search):
    for _, line in lines_from_file(filename):
        if invert_search != bool(regex.search(line)):
            return True
    return False


def print_binary(filename):
    print('Binary file {} matches'.format(filename))


def print_match(filename, line, regex, no_filename=False,
                file_is_binary=False, color=False, print_only_match=False):
    if file_is_binary:
        print_binary(filename)
        return

    filename, line = format_printline(filename, line, regex, color)
    if no_filename:
        print(line)
    else:
        print('{}:{}'.format(filename, line))


def colorize_match(match):
    return '{}{}{}'.format(colors.bcolors.MATCH, match.group(),
                           colors.bcolors.ENDC)


def format_printline(filename, line, regex, color):
    line = string.strip(line)
    if color:
        filename = colors.bcolors.CYAN + filename + colors.bcolors.ENDC
        line = regex.sub(colorize_match, line)
    return filename, line


def search_in_file(filename, regex, invert_match, no_filename,
                   color):
    any_match = False
    if file_helper.file_is_binary(filename):
        if search_in_binary_file(filename, regex, invert_match):
            any_match = True
            print_match(filename, None, regex, no_filename,
                        True, color)
    else:
        for linenr, line in search_in_text_file(filename, regex,
                                                invert_match):
            any_match = True
            print_match(filename, line, regex, no_filename,
                        False, color)
    return any_match


def progress_stdin(regex, invert_match=False, color=False):
    any_match = False
    for linenr, line in search_in_stdin(regex, invert_match):
        any_match = True
        print_match('', line, regex, True, False, color)
    return any_match


def progress_files(files, regex, invert_match=False, color=False,
                   recursive=False, dereference_recursive=False,
                   no_filename=False):
    any_match = False
    for file in files:
        if file_helper.file_is_directory(file):
            if not (dereference_recursive or recursive):
                print('pwgrep: {}: is a directory'.format(file))
            else:
                for filename in \
                    file_helper.traverse_recursively(
                        file,
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
    regex = build_regex(p.options.PATTERN[0], p.options.ignore_case)

    if not p.options.PATH:
        return progress_stdin(regex, p.options.invert_match, p.color)
    else:
        return progress_files(p.options.PATH, regex, p.options.invert_match,
                              p.color,
                              p.options.recursive,
                              p.options.dereference_recursive,
                              p.options.no_filename)


def signal_terminal_handler(signal_nr, frame):
    sys.exit(128 + signal_nr)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_terminal_handler)

    try:
        result = main(sys.argv)
    except KeyboardInterrupt:
        sys.exit(1)

    if result:
        sys.exit(0)
    sys.exit(1)
