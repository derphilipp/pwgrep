#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mimetypes
import os

from pwgrep import file_walker


def file_is_binary(filename):
    file_type, _ = mimetypes.guess_type(filename)
    return file_type is None or not file_type.startswith('text')


def file_is_directory(filename):
    return os.path.isdir(filename)


def get_all_files_from_directory(directory, deference_recursive=False):
    files = file_walker.symlink_walker(directory,
                                       deference_recursive=deference_recursive)
    for file_name in files:
        yield file_name
