#!/usr/bin/env python
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


def colorize_filename(file_name):
    """
    Colorizes filename
    :param file_name: filename to be colorized
    :return string: colorized filename
    """
    return '{}{}{}'.format(colors.ConsoleColors.FILE, file_name,
                           colors.ConsoleColors.ENDC)


def format_printline(file_name, line, regex, color):
    """
    Colorizes a given string as a 'match'
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
    Prints info for a match in a binary file
    :param file_name: filename to be printed
    :return:
    """
    print('Binary file {} matches'.format(file_name))


def print_text_match(file_name, line, regex, color, no_filename):
    """
    Prints info for a match in a textual file
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
    Prints warning for a recursive directory loop
    :param file_name: filename to be printed
    :return:
    """
    print('pwgrep: warning: {}: recursive directory loop'.format(file_name),
          file=sys.stderr)


def print_is_directory(dir_name):
    """
    Prints warning for trying to search a directory without recursion
    :param dir_name: directoryname to be printed
    :return:
    """
    print('pwgrep: {}: is a directory'.format(dir_name))


def print_match(filename, line, regex, no_filename=False,
                file_is_binary=False, color=False):
    """
    Prints matches from files
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
