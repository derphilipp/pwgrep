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
                file_is_binary=False, color=False):
    """
    Prints matches from files
    :param filename: filename of match
    :param line: complete line of match
    :param regex: regular expression used
    :param no_filename: if printing of filename shall be suppressed
    :param file_is_binary: if file is binary
    :param color: if output shall be colorized
    :return:
    """
    if file_is_binary:
        printer_helper.print_binary_match(filename)
    else:
        printer_helper.print_text_match(filename, line, regex, color,
                                        no_filename)


def search_in_file(filename, regex, invert_match, no_filename, color):
    """
    Searches and prints matches of a given file
    :param filename: filename to be searched in
    :param regex: regular expression for search
    :param invert_match: if matches shall be inverted
    :param no_filename: if printing of filename shall be suppressed
    :param color: if output shall be colorized
    :return:
    """
    match_occurred = False
    if file_helper.file_is_binary(filename):
        if search_helper.search_in_binary_file(filename, regex, invert_match):
            match_occurred = True
            print_match(filename, None, regex, no_filename,
                        True, color)
    else:
        for line_number, line in \
                search_helper.search_in_text_file(filename, regex,
                                                  invert_match):
            match_occurred = True
            print_match(filename, line, regex, no_filename,
                        False, color)
    return match_occurred


def process_stdin(regex, invert_match=False, color=False):
    """
    Processes grep operation on stdin
    :param regex: Regex used for matching
    :param invert_match: If match result shall be inversed
    :param color: If output shall be colored
    :return: If any match occurred
    """
    match_occurred = False
    for line_nr, line in search_helper.search_in_stdin(regex, invert_match):
        match_occurred = True
        print_match('', line, regex, True, False, color)
    return match_occurred


def process_commandline(files, regex, invert_match=False, color=False,
                        recursive=False, dereference_recursive=False,
                        no_filename=False):
    """
    Processes grep operation on stdin
    :param files: Files to be processed
    :param regex: Regex used for matching
    :param invert_match: If match result shall be inversed
    :param color: If output shall be colored
    :param recursive: If recursion shall be used on directories
    :param dereference_recursive: If recursion shall be used on directories,
    following symlinks
    :param no_filename: If printing of filename shall be suppressed
    :return: If any match occurred
    """
    match_occurred = False
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
                        match_occurred = True

        else:
            if search_in_file(file, regex, invert_match,
                              no_filename, color):
                match_occurred = True
    return match_occurred


def main(args):
    """
    Processes input  and performs grep operations
    :param args: command line parameters (except [0], i.e. program name)
    :return: if any match was found in file
    """
    p = command_parser.CommandParser(args)

    regex_flags = 0
    if p.options.ignore_case:
        regex_flags |= re.IGNORECASE
    regex = re.compile(p.options.PATTERN[0], regex_flags)

    if not p.options.PATH:
        return process_stdin(regex, p.options.invert_match, p.color)
    else:
        return process_commandline(p.options.PATH,
                                   regex,
                                   p.options.invert_match,
                                   p.color,
                                   p.options.recursive,
                                   p.options.dereference_recursive,
                                   p.options.no_filename)


def signal_terminal_handler(signal_nr, frame):
    """
    Handler for signals; Quits program with correct exit code
    :param signal_nr: signal nr of received signal
    :param frame: -
    :return:
    """
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
