#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import mimetypes


def file_is_binary(filename):
    type, _ = mimetypes.guess_type(filename)
    return type is None or not type.startswith('text')
