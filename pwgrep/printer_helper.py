#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys


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
