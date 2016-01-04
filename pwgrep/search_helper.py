#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys


def lines_from_file(filename):
    """
    Tries to read each line for a given file. Prints Error messages on IOErrors
    :param filename: filename to be read
    :return line_number, line: (yields) line number, line of file to be read
    """
    try:
        file_object = open(filename, 'r')
        for line_nr, line in enumerate(file_object):
            yield line_nr, line
    except IOError:
        if os.path.exists(filename):
            print ('pwgrep: {}: Permission denied'.format(filename))
        else:
            print ('pwgrep: {}: No such file or directory'.format(filename))


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
    for _, line in lines_from_file(filename):
        if invert_match != bool(regex.search(line)):
            return True
    return False
