#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import mimetypes
import os

import file_walker


def file_is_binary(filename):
    type, _ = mimetypes.guess_type(filename)
    return type is None or not type.startswith('text')


def file_is_directory(filename):
    return os.path.isdir(filename)


def recurse(directory, deference_recursive=False):
    files = file_walker.symlink_walker(directory,
                                       deference_recursive=deference_recursive)
    for f in files:
        yield f
