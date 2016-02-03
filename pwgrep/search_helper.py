#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pwgrep import file_helper
from pwgrep import search_result


class RegexSearcher(object):

    def __init__(self, regexes, invert_match):
        self.regexes = regexes
        self.invert_match = invert_match

    def search_in_text_line(self, line):
        result = []
        for m in self.regexes.regex_txt.finditer(line):
            result.append([m.start(), m.end()])
        if len(result) == 0:
            return None
        return result

    def search_in_text_file(self, filename):
        for line_nr, line in lines_in_file(filename):
            # rs = RegexSearcher(regex)
            result = self.search_in_text_line(line)
            yield line_nr, line, result

    def search_in_binary_file(self, filename):
        with open(filename, 'rb+') as file_object:
            for _, line in enumerate(file_object):
                if self.invert_match != bool(self.regexes.regex_bin.search(line)):
                    return True
            return False

    def search_in_file(self, filename):  # , invert_match, no_filename, color):
        if not file_exists_and_readable(filename):
            return

        if file_helper.file_is_binary(filename):
            if self.search_in_binary_file(filename):
                yield search_result.BinarySearchResult(filename=filename)
        else:
            for line_nr, line, result in self.search_in_text_file(filename):
                yield search_result.TextSearchResult(line_number=line_nr,
                                                     line=line,
                                                     match=result,
                                                     filename=filename)

    def search_in_stdin(self):
        for line_nr, line in enumerate(sys.stdin):
            result = self.search_in_text_line(line)
            if result:
                yield search_result.StdinSearchResult(
                    line_number=line_nr,
                    match=result, line=line)


def lines_in_file(filename):
    """
    Try to read each line for a given file. Print Error messages on IOErrors.

    :param filename: filename to be read
    :return line_number, line: (yields) line number, line of file to be read
    """
    with open(filename, 'rU') as file_object:
        for line_nr, line in enumerate(file_object):
            yield line_nr, line


def file_exists_and_readable(filename):
    if not os.path.exists(filename):
        print('pwgrep: {}: No such file or directory'.format(filename))
        return False
    if not os.access(filename, os.R_OK):
        print('pwgrep: {}: Permission denied'.format(filename))
        return False
    return True
