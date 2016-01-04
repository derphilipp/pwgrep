#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from ..pwgrep import file_helper
#import pwgrep
print(__name__)

def test_file_is_binary():
    print(__name__)
    assert file_helper.file_is_binary('data/simple/helloworld') == True


def test_file_is_text():
    assert file_helper.file_is_binary('data/simple/zen_of_python.txt')\
           == False

