#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from pwgrep import colors


def colorize_match(match):
    """
    Colorizes matches in a line
    :param match: regex match to be marked
    :return: colorized line
    """
    return '{}{}{}'.format(colors.ConsoleColors.MATCH, match.group(),
                           colors.ConsoleColors.ENDC)


def colorize_filename(filename):
    """
    Colorizes filename
    :param filename: filename to be colorized
    :return string: colorized filename
    """
    return '{}{}{}'.format(colors.ConsoleColors.FILE, filename,
                           colors.ConsoleColors.ENDC)


def format_printline(filename, line, regex, color):
    """
    Colorizes a given string as a 'match'
    :param filename: filename with match
    :param line: matched line
    :param regex: regular expression used for search/colorization
    :param color: if result shall be colorized
    :return: filename, line
    """
    line = line.strip()
    if color:
        filename = colorize_filename(filename)
        line = regex.sub(colorize_match, line)
    return filename, line


def print_binary_match(filename):
    """
    Prints info for a match in a binary file
    :param filename: filename to be printed
    :return:
    """
    print('Binary file {} matches'.format(filename))


def print_text_match(filename, line, regex, color, no_filename):
    """
    Prints info for a match in a textual file
    :param filename: filename to be printed
    :param line: (matched) line to be printed
    :param regex: regex to be printed/marked
    :param color: output in color
    :param no_filename: if the filename printing shall be suppressed
    """
    filename, line = format_printline(filename, line, regex, color)
    if no_filename:
        print(line)
    else:
        print('{}:{}'.format(filename, line))


def print_loop_warning(filename):
    """
    Prints warning for a recursive directory loop
    :param filename: filename to be printed
    :return:
    """
    print('pwgrep: warning: {}: recursive directory loop'.format(filename),
          file=sys.stderr)
