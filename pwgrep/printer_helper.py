#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from pwgrep import colors
from pwgrep import search_result


class ResultPrinter(object):

    def __init__(
        self,
        colorize=False,
        print_filename=True,
            invert_match=False):
        self.colorize = colorize
        self.print_filename = print_filename
        self.invert_match = invert_match
        if self.colorize:
            self.COLOR_MATCH = colors.ConsoleColors.MATCH
            self.COLOR_FILE = colors.ConsoleColors.FILE
            self.COLOR_ENDC = colors.ConsoleColors.ENDC
        else:
            self.COLOR_MATCH = ""
            self.COLOR_FILE = ""
            self.COLOR_ENDC = ""

    def _print_filename(self, filename):
        if self.print_filename:
            print('{}{}{}:'.format(self.COLOR_FILE,
                                   filename,
                                   self.COLOR_ENDC), end="")

    def print_any_match(self, search_result):
        pos = 0
        for fr, to in search_result.match:
            if pos < to:
                print(search_result.line[pos:fr], end="")
            print("{}{}{}".format(self.COLOR_MATCH, search_result.line[fr:to],
                                  self.COLOR_ENDC), end="")
            pos = to
        print(search_result.line[pos:], end="")

    def print_single_match(self, search_result):
        if not search_result.match and self.invert_match:
            self._print_filename(search_result.filename)
            print(search_result.line, end="")
        elif search_result.match and not self.invert_match:
            self._print_filename(search_result.filename)
            self.print_any_match(search_result)

    def print_binary_match(self, search_result):
        print('Binary file {} matches'.format(search_result.filename))

    def print_stdin_match(self, search_result):
        self.print_any_match(search_result)

    def print_result(self, result):
        if isinstance(result, search_result.TextSearchResult):
            self.print_single_match(result)
        elif isinstance(result, search_result.BinarySearchResult):
            self.print_binary_match(result)
        elif isinstance(result, search_result.StdinSearchResult):
            self.print_stdin_match(result)
        else:
            print(type(result))
            assert(False)


def colorize_match(match):
    """
    Colorize matches in a line.

    :param match: regex match to be marked
    :return: colorized line
    """
    return '{}{}{}'.format(colors.ConsoleColors.MATCH, match.group(),
                           colors.ConsoleColors.ENDC)


def colorize_filename(file_name):
    """
    Colorize filename.

    :param file_name: filename to be colorized
    :return string: colorized filename
    """
    return '{}{}{}'.format(colors.ConsoleColors.FILE, file_name,
                           colors.ConsoleColors.ENDC)


def format_printline(file_name, line, regex, color):
    """
    Colorize a given string as a 'match'.

    :param file_name: filename with match
    :param line: matched line
    :param regex: regular expression used for search/colorization
    :param color: if result shall be colorized
    :return: filename, line
    """
    line = line.strip()
    if color:
        file_name = colorize_filename(file_name)
        line = regex.sub(colorize_match, line)
    return file_name, line


def print_binary_match(file_name):
    """
    Print info for a match in a binary file.

    :param file_name: filename to be printed
    :return:
    """
    print('Binary file {} matches'.format(file_name))


def print_text_match(file_name, line, regex, color, no_filename):
    """
    Print info for a match in a textual file.

    :param file_name: filename to be printed
    :param line: (matched) line to be printed
    :param regex: regex to be printed/marked
    :param color: output in color
    :param no_filename: if the filename printing shall be suppressed
    """
    file_name, line = format_printline(file_name, line, regex, color)
    if no_filename:
        print(line)
    else:
        print('{}:{}'.format(file_name, line))


def print_loop_warning(file_name):
    """
    Print warning for a recursive directory loop.

    :param file_name: filename to be printed
    :return:
    """
    print('pwgrep: warning: {}: recursive directory loop'.format(file_name),
          file=sys.stderr)


def print_is_directory(dir_name):
    """
    Print warning for trying to search a directory without recursion.

    :param dir_name: directoryname to be printed
    :return:
    """
    print('pwgrep: {}: is a directory'.format(dir_name))


def print_match(filename, line, regex, no_filename=False,
                file_is_binary=False, color=False):
    """
    Print matches from files.

    :param filename: filename of match
    :param line: complete line of match
    :param regex: regular expression used
    :param no_filename: if printing of filename shall be suppressed
    :param file_is_binary: if file is binary
    :param color: if output shall be colorized
    :return:
    """
    if file_is_binary:
        print_binary_match(filename)
    else:
        print_text_match(filename, line, regex, color, no_filename)
