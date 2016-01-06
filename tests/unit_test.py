#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from pwgrep import file_helper


def test_file_is_binary():
    assert file_helper.file_is_binary('tests/data/simpte/helloworld')


def test_file_is_text():
    assert not file_helper.file_is_binary(
        'tests/data/simple/zen_of_python.txt')


def test_file_is_directory():
    assert file_helper.file_is_directory('tests/data/simple')


def test_file_is_not_directory():
    assert not file_helper.file_is_directory(
        'tests/data/simple/helloworld')
