#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys

from pwgrep import command_parser_text
from pwgrep import version


class CommandParser(object):
    def __init__(self, args):
        self._parser = argparse.ArgumentParser(prog='pwgrep', add_help=False)

        recursion_group = self._parser.add_mutually_exclusive_group()

        recursion_group.add_argument(
            '-R', '--dereference-recursive',
            action='store_true',
            help=command_parser_text.DEREFERENCE_RECURSIVE
        )
        recursion_group.add_argument(
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
            type=self.validate_color,
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
            action='version', version='pwgrep {}'.format(version.VERSION)
        )
        self._parser.add_argument(
            '--help',
            action='help', help=command_parser_text.HELP
        )
        self.options = self._parser.parse_args(args)

    @staticmethod
    def validate_color(value):
        if value not in ['always', 'never', 'auto']:
            raise argparse.ArgumentTypeError("{} is not a valid color "
                                             "option".format(value))
        return value

    @property
    def color(self):
        if self.options.color is None or self.options.color == 'never':
            return False
        if self.options.color == 'always':
            return True
        # can only be 'auto' at this point
        return os.isatty(sys.stdout.fileno())
