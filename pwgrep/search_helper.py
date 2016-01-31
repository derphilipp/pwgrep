#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pwgrep import file_helper
from pwgrep import printer_helper


def lines_in_file(filename):
    """
    Try to read each line for a given file. Print Error messages on IOErrors.

    :param filename: filename to be read
    :return line_number, line: (yields) line number, line of file to be read
    """
    with open(filename, 'rU') as file_object:
        for line_nr, line in enumerate(file_object):
            yield line_nr, line


def results_in_text_file(filename, regex, invert_match):
    """
    Search for regex in a textual file.

    :param filename : file to be searched in
    :param regex: regex to search with
    :param invert_match: if match should be inverted (i.e. non-matches shall
    match)
    :return int, string: matched line number, matched line
    """
    for line_nr, line in lines_in_file(filename):
        if invert_match != bool(regex.search(line)):
            yield line_nr, line


def results_in_binary_file(filename, regex, invert_match):
    """
    Search for regex in a binary file.

    :param filename: file to be searched in
    :param regex: regex to search with
    :param invert_match: if match should be inverted
                         (i.e. non-matches shall match)
    :return match_was_found: if a match was found
    """
    with open(filename, 'rb+') as file_object:
        for _, line in enumerate(file_object):
            if invert_match != bool(regex.search(line)):
                return True
        return False


def file_exists_and_readable(filename):
    if not os.path.exists(filename):
        print ('pwgrep: {}: No such file or directory'.format(filename))
        return False
    if not os.access(filename, os.R_OK):
        print('pwgrep: {}: Permission denied'.format(filename))
        return False
    return True


def search_in_file(filename, regexes, invert_match, no_filename,
                   color):
    """
    Search and print matches of a given file.

    :param filename: filename to be searched in
    :param regexes: Regexes for binary and textual regex
    :param invert_match: if matches shall be inverted
    :param no_filename: if printing of filename shall be suppressed
    :param color: if output shall be colorized
    :return:
    """
    if not file_exists_and_readable(filename):
        return

    # match_occurred = False
    if file_helper.file_is_binary(filename):
        if results_in_binary_file(filename, regexes.regex_bin, invert_match):
            # match_occurred = True
            printer_helper.print_match(filename, None, None, no_filename,
                                       True, color)
            yield filename
    else:
        for _, line in results_in_text_file(filename,
                                            regexes.regex_txt,
                                            invert_match):
            # match_occurred = True
            printer_helper.print_match(filename, line, regexes.regex_txt,
                                       no_filename,
                                       False, color)
            yield filename, line
            # return match_occurred
