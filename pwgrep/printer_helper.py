#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import colors
import string


def colorize_match(match):
    return '{}{}{}'.format(colors.bcolors.MATCH, match.group(),
                           colors.bcolors.ENDC)


def format_printline(filename, line, regex, color):
    line = string.strip(line)
    if color:
        filename = colors.bcolors.CYAN + filename + colors.bcolors.ENDC
        line = regex.sub(colorize_match, line)
    return filename, line


def print_binary_match(filename):
    print('Binary file {} matches'.format(filename))


def print_text_match(filename, line, regex, color, no_filename):
    filename, line = format_printline(filename, line, regex, color)
    if no_filename:
        print(line)
    else:
        print('{}:{}'.format(filename, line))
