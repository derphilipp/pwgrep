#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sre_constants

import argparse

from pwgrep import commandline_parser_text
from pwgrep import version
from pwgrep.commandline_parser_result import CommandLineParserResult


class CommandLineParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(prog='pwgrep', add_help=False)

        recursion_group = self._parser.add_mutually_exclusive_group()

        recursion_group.add_argument(
            '-R', '--dereference-recursive',
            action='store_true',
            help=commandline_parser_text.DEREFERENCE_RECURSIVE
        )
        recursion_group.add_argument(
            '-r', '--recursive',
            action='store_true',
            help=commandline_parser_text.RECURSIVE)

        self._parser.add_argument(
            '-h', '--no-filename',
            action='store_true',
            help=commandline_parser_text.NO_FILENAME
        )
        self._parser.add_argument(
            '-i', '-y', '--ignore-case',
            action='store_true',
            help=commandline_parser_text.IGNORE_CASE
        )
        self._parser.add_argument(
            '-v', '--invert-match',
            action='store_true',
            help=commandline_parser_text.INVERT_MATCH
        )

        self._parser.add_argument(
            '-o', '--only-matching',
            action='store_true',
            help=commandline_parser_text.ONLY_MATCHING
        )

        self._parser.add_argument(
            '--color', nargs='?', default='never',
            type=self._evaluate_color,
            help=commandline_parser_text.COLOR
        )

        self._parser.add_argument(
            'PATTERN',
            metavar='PATTERN', nargs=1,
            type=self._evaluate_regex,
            help=commandline_parser_text.PATTERN
        )
        self._parser.add_argument(
            'PATH',
            metavar='PATH', type=str, nargs='*',
            help=commandline_parser_text.PATH
        )
        self._parser.add_argument(
            '--version',
            action='version', version='pwgrep {}'.format(version.VERSION)
        )
        self._parser.add_argument(
            '--help',
            action='help', help=commandline_parser_text.HELP
        )

    @staticmethod
    def _evaluate_color(value):
        if value not in ['always', 'never', 'auto']:
            raise argparse.ArgumentTypeError("{} is not a valid color "
                                             "option".format(value))
        return value

    @staticmethod
    def _evaluate_regex(regex):
        """
        Evaluate if given regex is valid

        :param regex:
        :return: Value of regex
        """
        try:
            re.compile(regex)
        except sre_constants.error as e:
            raise argparse.ArgumentTypeError("{} is an invalid "
                                             "regular expression: '{}'"
                                             .format(regex, e.args[0]))
        return regex

    def parse(self, args):
        """
        Parse provided input arguments.

        :param args: Command line arguments / input strings for parser
        :return: CommandLineParameterResult containing resulting options
        """
        return CommandLineParserResult(self._parser.parse_args(args))
