#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from pwgrep.colors import ConsoleColors
from pwgrep.search_result import TextSearchResult, BinarySearchResult, StdinSearchResult


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
            self.COLOR_MATCH = ConsoleColors.MATCH
            self.COLOR_FILE = ConsoleColors.FILE
            self.COLOR_ENDC = ConsoleColors.ENDC
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
        if isinstance(result, TextSearchResult):
            self.print_single_match(result)
        elif isinstance(result, BinarySearchResult):
            self.print_binary_match(result)
        elif isinstance(result, StdinSearchResult):
            self.print_stdin_match(result)
        else:
            assert False, "Invalid type to print: {}".format(type(result))

