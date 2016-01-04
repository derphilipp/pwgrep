#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import mimetypes
import os


def file_is_binary(filename):
    type, _ = mimetypes.guess_type(filename)
    return type is None or not type.startswith('text')


def file_is_directory(filename):
    return os.path.isdir(filename)


def traverse_recursively(directory, deference_recursive=False):
    for root, dirs, files in os.walk(directory,
                                     followlinks=deference_recursive):
        for filename in files:
            yield os.path.join(root, filename)
