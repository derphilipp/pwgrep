#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import mimetypes
import os


def file_is_binary(filename):
    type, _ = mimetypes.guess_type(filename)
    return type is None or not type.startswith('text')


def file_is_directory(filename):
    return os.path.isdir(filename)
