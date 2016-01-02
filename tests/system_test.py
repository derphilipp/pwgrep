#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pytest
import subprocess
import os


def caller(directory, command):
    proc=subprocess.Popen('../../../pwgrep/pwgrep.py {}'.format(command),
                     cwd=directory,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)
    proc.wait()
    stdout, stderr = proc.communicate()
    code=proc.returncode
    #output = proc.stdout.read()
    #error_output = proc.stderr.read()
    return code, stdout,stderr


#  0 -- Keine Fehler und mindestens ein Match
#  1 -- Fehler oder kein Match
#  128 + X -- Killed by signal X

simpledir = r'./tests/data/simple'

def helper_test_match(directory, command, stdout_shall, stderr_shall, return_code_shall):
    return_code_is, stdout_is, stderr_is = caller(directory, command)
    assert stderr_is.decode("utf-8") == (stderr_shall)
    assert stdout_is.decode("utf-8") == (stdout_shall)
    assert return_code_is == (return_code_shall)


# Basic Search
def test_text_match():
    helper_test_match(simpledir, 'Zen *', 'zen_of_python.txt:The Zen of '
                                         'Python, by Tim Peters\n', '', 0)


def test_binary_match():
    helper_test_match(simpledir, 'Hello *', 'Binary file helloworld '
                                           'matches\n', '', 0)


def test_no_match():
    helper_test_match(simpledir, 'ThisIsNeverFound *', '', '', 1)


# No display of filename
def test_text_match_no_filename():
    helper_test_match(simpledir, '-h Zen *', 'The Zen of Python, by Tim '
                                            'Peters\n', '', 0)


def test_binary_match_no_filename():
    helper_test_match(simpledir, '-h Hello *', 'Binary file helloworld '
                                              'matches\n', '', 0)


# Ignore case
def test_text_match_ignore_case():
    helper_test_match(simpledir, '-i zEN *', 'zen_of_python.txt:The Zen of '
                                            'Python, by Tim Peters\n', '', 0)


def test_binary_match_ignore_case():
    helper_test_match(simpledir, '-i hElLo *', 'Binary file helloworld '
                      'matches\n', '', 0)


# io error, file not readable
def test_file_not_readable(tmpdir):
    file = tmpdir.join('unreadable.txt')
    file.write('This file is not readable')
    file.chmod(0)
    filename = str(file)
    helper_test_match(simpledir, 'readable {}'.format(filename),
                      'pwgrep: {}: Permission denied\n'.format(filename), '', 1)


# inverse search
def test_inverse_l():
    expected_stdout = """Binary file helloworld matches
zen_of_python.txt:The Zen of Python, by Tim Peters
zen_of_python.txt:
zen_of_python.txt:Sparse is better than dense.
zen_of_python.txt:In the face of ambiguity, refuse the temptation to guess.
zen_of_python.txt:Now is better than never.
"""
    helper_test_match(simpledir, '-v l *', expected_stdout, '', 0)


def test_inverse_h():
    expected_stdout = """Binary file helloworld matches
zen_of_python.txt:
zen_of_python.txt:Readability counts.
zen_of_python.txt:Unless explicitly silenced.
"""
    helper_test_match(simpledir, '-v h *', expected_stdout, '', 0)
