#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import os
import sys
import re

#from pwgrep import commandparsertext
import commandparsertext
from version import VERSION


# [-R|-r] [-h] [-i] [-v] [-o] [--color[=(never|always|auto)] PATTERN [PATH ..]


class CommandParser(object):
    def __init__(self, args):
        self._parser = argparse.ArgumentParser(add_help=False)

        self._parser.add_argument(
            '-R', '--dereference-recursive',
            action='store_true',
            help=commandparsertext.DEREFERENCE_RECURSIVE
        )
        self._parser.add_argument(
            '-r', '--recursive',
            action='store_true',
            help=commandparsertext.RECURSIVE)
        self._parser.add_argument(
            '-h', '--no-filename',
            action='store_true',
            help=commandparsertext.NO_FILENAME
        )
        self._parser.add_argument(
            '-i', '-y', '--ignore-case',
            action='store_true',
            help=commandparsertext.IGNORE_CASE
        )
        self._parser.add_argument(
            '-v', '--invert-match',
            action='store_true',
            help=commandparsertext.INVERT_MATCH
        )

        self._parser.add_argument(
            '-o', '--only-matching',
            action='store_true',
            help=commandparsertext.ONLY_MATCHING
        )

        self._parser.add_argument(
            '--color', nargs='?', default='never',
            help=commandparsertext.COLOR
        )

        self._parser.add_argument(
            'PATTERN',
            metavar='PATTERN', type=str, nargs=1,
            help=commandparsertext.PATTERN
        )
        self._parser.add_argument(
            'PATH',
            metavar='PATH', type=str, nargs='*',
            help=commandparsertext.PATH
        )
        self._parser.add_argument(
            '--version',
            action='version', version='%(prog)s {}'.format(VERSION)
        )
        self._parser.add_argument(
            '--help',
            action='help', help=commandparsertext.HELP
        )
        self.options = self._parser.parse_args()

    @property
    def color(self):
        if self.args.color is None or self.args.color == 'never':
            return False
        if self.args.color == 'always':
            return True
        if self.args.color == 'auto':
            return os.isatty(sys.stdout.fileno())
        # TODO More userfriendly error handling
        raise ValueError(
            'Invalid type of color "{}" set'.format(self.args.color))


def lines_from_file(filename):
    try:
        file = open(filename, 'r')
        for linenr, line in enumerate(file):
            yield linenr, line
    except IOError:
        # TODO: Specify what happens here
        pass

def search_in_file(filename, regex):
    for linenr, line in lines_from_file(filename):
        if regex.search(line):
            yield linenr, line

def search_files(list_of_files):
    for file in list_of_files:
        search_in_file(list_of_files, regex)


def filelist(startpoint):
    # TODO Build in recursion etc.
    for element in startpoint:
        yield element

def display_version():
    print("Version {}".format(VERSION))

def main(args):
    p = CommandParser(args)
    print(p.options)
    # TODO: Check flags for options
    regex = re.compile(p.options.PATTERN[0])
    for file in filelist(p.options.PATH):
        for linenr, line in search_in_file(file, regex):
            print (linenr+1)


if __name__ == "__main__":
    main(sys.argv)
