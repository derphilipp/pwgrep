#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from pwgrep import file_helper


def test_file_is_binary():
    assert file_helper.file_is_binary('tests/data/simple/helloworld') == True


def test_file_is_text():
    assert file_helper.file_is_binary('tests/data/simple/zen_of_python.txt')\
           == False


def test_file_is_directory():
    assert file_helper.file_is_directory('tests/data/simple') == True


def test_file_is_not_directory():
    assert file_helper.file_is_directory('tests/data/simple/helloworld') == \
           False
