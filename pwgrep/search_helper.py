#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys


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


def search_in_stdin(regex, invert_match):
    for line_nr, line in enumerate(sys.stdin):
        if invert_match != bool(regex.search(line)):
            yield line_nr, line


def search_in_text_file(filename, regex, invert_match):
    for linline_nr, line in lines_from_file(filename):
        if invert_match != bool(regex.search(line)):
            yield linline_nr, line


def search_in_binary_file(filename, regex, invert_match):
    for _, line in lines_from_file(filename):
        if invert_match != bool(regex.search(line)):
            return True
    return False
