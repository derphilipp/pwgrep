#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import os
import sys

import command_parser_text
import version


class CommandParser(object):

    def __init__(self, args):
        self._parser = argparse.ArgumentParser(add_help=False)

        self._parser.add_argument(
            '-R', '--dereference-recursive',
            action='store_true',
            help=command_parser_text.DEREFERENCE_RECURSIVE
        )
        self._parser.add_argument(
            '-r', '--recursive',
            action='store_true',
            help=command_parser_text.RECURSIVE)
        self._parser.add_argument(
            '-h', '--no-filename',
            action='store_true',
            help=command_parser_text.NO_FILENAME
        )
        self._parser.add_argument(
            '-i', '-y', '--ignore-case',
            action='store_true',
            help=command_parser_text.IGNORE_CASE
        )
        self._parser.add_argument(
            '-v', '--invert-match',
            action='store_true',
            help=command_parser_text.INVERT_MATCH
        )

        self._parser.add_argument(
            '-o', '--only-matching',
            action='store_true',
            help=command_parser_text.ONLY_MATCHING
        )

        self._parser.add_argument(
            '--color', nargs='?', default='never',
            help=command_parser_text.COLOR
        )

        self._parser.add_argument(
            'PATTERN',
            metavar='PATTERN', type=str, nargs=1,
            help=command_parser_text.PATTERN
        )
        self._parser.add_argument(
            'PATH',
            metavar='PATH', type=str, nargs='*',
            help=command_parser_text.PATH
        )
        self._parser.add_argument(
            '--version',
            action='version', version='%(prog)s {}'.format(version.VERSION)
        )
        self._parser.add_argument(
            '--help',
            action='help', help=command_parser_text.HELP
        )
        self.options = self._parser.parse_args(args[1:])

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
