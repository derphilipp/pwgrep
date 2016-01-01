#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import subprocess


def caller(directory, command):
    proc=subprocess.Popen('../../../pwgrep/pwgrep.py {}'.format(command),
                     cwd=r'./tests/data/{}'.format(directory),
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


def helper_test_match(directory, command, stdout_shall, stderr_shall, return_code_shall):
    return_code_is, stdout_is, stderr_is = caller(directory, command)
    assert stderr_is.decode("utf-8") == (stderr_shall)
    assert stdout_is.decode("utf-8") == (stdout_shall)
    assert return_code_is == (return_code_shall)


# Basic Search
def test_text_match():
    helper_test_match('simple', 'Zen *', 'zen_of_python.txt:The Zen of '
                                         'Python, by Tim Peters\n', '', 0)


def test_binary_match():
    helper_test_match('simple', 'Hello *', 'Binary file helloworld '
                                           'matches\n', '', 0)


def test_no_match():
    helper_test_match('simple', 'ThisIsNeverFound *', '', '', 1)


# No display of filename
def test_text_match_no_filename():
    helper_test_match('simple', '-h Zen *', 'The Zen of Python, by Tim '
                                            'Peters\n', '', 0)


def test_binary_match_no_filename():
    helper_test_match('simple', '-h Hello *', 'Binary file helloworld '
                                              'matches\n', '', 0)


# Ignore case
def test_text_match_ignore_case():
    helper_test_match('simple', '-i zEN *', 'zen_of_python.txt:The Zen of '
                                            'Python, by Tim Peters\n', '', 0)


def test_binary_match_ignore_case():
    helper_test_match('simple', '-i hElLo *', 'Binary file helloworld '
                                              'matches\n', '', 0)