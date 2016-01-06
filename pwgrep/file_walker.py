#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import collections

from pwgrep import printer_helper

WalkedDir = collections.namedtuple("WalkedDir", "path subdirs files depth")


def symlink_walker(directory, deference_recursive=False, onerror=None):
    """
    Wrapper around os.walk that recognizes symlink loops

    Heavily inspired by Nick Coghlans walking algorithm
    https://code.activestate.com/recipes/577913-selective-directory-walking/

    :param directory: Directory to start in
    :param deference_recursive: If symlinks shall be followed
    :param onerror: Error handler of os.walk
    :return: yields full filename of traversed files
    """
    if deference_recursive:
        absolute_root_path = os.path.abspath(os.path.realpath(directory))

    for path, walk_subdirs, files in os.walk(directory, topdown=True,
                                             onerror=onerror,
                                             followlinks=deference_recursive):
        # Recognize infinite symlink loops
        if deference_recursive and os.path.islink(path):
            # After following a symbolic link, we check if we refer
            # to a parent directory. If yes: We have an infinite loop
            relative_path = os.path.relpath(path, directory)
            nominal_path = os.path.join(absolute_root_path, relative_path)
            real_path = os.path.abspath(os.path.realpath(path))
            path_fragments = zip(nominal_path.split(os.path.sep),
                                 real_path.split(os.path.sep))
            for nominal, real in path_fragments:
                if nominal != real:
                    break
            else:
                printer_helper.print_loop_warning(path)
                walk_subdirs[:] = []
                continue
        subdirs = walk_subdirs[:]
        for f in files:
            yield os.path.join(path, f)
        walk_subdirs[:] = subdirs
