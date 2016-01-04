#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pytest


import file_helper
#from pwgrep import file_helper


def test_file_is_binary():
    print(__name__)
    assert file_helper.file_is_binary('data/simple/helloworld') == True


def test_file_is_text():
    assert file_helper.file_is_binary('data/simple/zen_of_python.txt')\
           == False

