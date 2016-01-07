#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pwgrep import file_helper
from pwgrep import printer_helper


def lines_from_file(filename):
    """
    Tries to read each line for a given file. Prints Error messages on IOErrors
    :param filename: filename to be read
    :return line_number, line: (yields) line number, line of file to be read
    """
    try:
        with open(filename, 'rU') as file_object:
            for line_nr, line in enumerate(file_object):
                yield line_nr, line
    except IOError:
        if os.path.exists(filename):
            print ('pwgrep: {}: Permission denied'.format(filename))
        else:
            print ('pwgrep: {}: No such file or directory'.format(filename))


def search_in_text_file(filename, regex, invert_match):
    """
    Searches for regex in a textual file
    :param filename : file to be searched in
    :param regex: regex to search with
    :param invert_match: if match should be inverted (i.e. non-matches shall
    match)
    :return int, string: matched line number, matched line
    """
    for line_nr, line in lines_from_file(filename):
        if invert_match != bool(regex.search(line)):
            yield line_nr, line


def search_in_binary_file(filename, regex, invert_match):
    """
    Searches for regex in a binary file
    :param filename: file to be searched in
    :param regex: regex to search with
    :param invert_match: if match should be inverted
                         (i.e. non-matches shall match)
    :return match_was_found: if a match was found
    """
    try:
        with open(filename, 'rb+') as file_object:
            for _, line in enumerate(file_object):
                if invert_match != bool(regex.search(line)):
                    return True
            return False
    except IOError:
        if os.path.exists(filename):
            print ('pwgrep: {}: Permission denied'.format(filename))
        else:
            print ('pwgrep: {}: No such file or directory'.format(filename))


def search_in_file(filename, regex_txt, regex_bin, invert_match, no_filename,
                   color):
    """
    Searches and prints matches of a given file
    :param filename: filename to be searched in
    :param regex_txt: Regex used for matching text
    :param regex_bin: Regex used for matching binary
    :param invert_match: if matches shall be inverted
    :param no_filename: if printing of filename shall be suppressed
    :param color: if output shall be colorized
    :return:
    """
    match_occurred = False
    if file_helper.file_is_binary(filename):
        if search_in_binary_file(filename, regex_bin, invert_match):
            match_occurred = True
            printer_helper.print_match(filename, None, None, no_filename,
                                       True, color)
    else:
        for _, line in search_in_text_file(filename, regex_txt, invert_match):
            match_occurred = True
            printer_helper.print_match(filename, line, regex_txt, no_filename,
                                       False, color)
    return match_occurred


def search_in_stdin(regex, invert_match):
    """
    Searches for regex in stdin
    :param regex:                regex to search with
    :param invert_match:         if match should be inverted
                                (i.e. non-matches shall match)
    :return line_number, line: (yields) matched line number, matched line
    """
    for line_nr, line in enumerate(sys.stdin):
        if invert_match != bool(regex.search(line)):
            yield line_nr, line
