#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pytest
import subprocess
import sys


def caller(directory, command, stdin=None):
    proc = subprocess.Popen('pwgrep {}'.format(command),
                            cwd=directory,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            stdin=subprocess.PIPE)
    if stdin:
        stdout, stderr = proc.communicate(stdin)  # , timeout=TEST_TIMEOUT)
    else:
        stdout, stderr = proc.communicate()  # , timeout=TEST_TIMEOUT)

    code = proc.returncode
    return code, stdout, stderr


SIMPLEDIR = r'tests/data/simple'
TREEDIR = r'tests/data/tree'
SYMLINKDIR = r'tests/data/symlink'
INFINITE_RECURSION_LINK = r'tests/data/infinite_recursion'


def helper_test_match(directory, command, stdout_shall, stderr_shall,
                      return_code_shall, stdin=None):
    return_code_is, stdout_is, stderr_is = caller(directory, command, stdin)
    assert stderr_is.decode("utf-8") == stderr_shall
    assert stdout_is.decode("utf-8") == stdout_shall
    assert return_code_is == return_code_shall


# Basic Search
def test_text_match():
    helper_test_match(SIMPLEDIR, 'Zen *', 'zen_of_python.txt:The Zen of '
                                          'Python, by Tim Peters\n', '', 0)


def test_binary_match():
    helper_test_match(SIMPLEDIR, 'Hello *', 'Binary file helloworld '
                                            'matches\n', '', 0)


def test_no_match():
    helper_test_match(SIMPLEDIR, 'ThisIsNeverFound *', '', '', 1)


# No display of filename
def test_text_match_no_filename():
    helper_test_match(SIMPLEDIR, '-h Zen *', 'The Zen of Python, by Tim '
                                             'Peters\n', '', 0)


def test_binary_match_no_filename():
    helper_test_match(SIMPLEDIR, '-h Hello *', 'Binary file helloworld '
                                               'matches\n', '', 0)


# Ignore case
def test_text_match_ignore_case():
    helper_test_match(SIMPLEDIR, '-i zEN *', 'zen_of_python.txt:The Zen of '
                                             'Python, by Tim Peters\n', '', 0)


def test_binary_match_ignore_case():
    helper_test_match(SIMPLEDIR, '-i hElLo *', 'Binary file helloworld '
                                               'matches\n', '', 0)


# io error, file not readable
def test_file_not_readable(tmpdir):
    file_object = tmpdir.join('unreadable.txt')
    file_object.write('This file is not readable')
    file_object.chmod(0)
    filename = str(file_object)
    helper_test_match(SIMPLEDIR, 'readable {}'.format(filename),
                      'pwgrep: {}: Permission denied\n'.format(filename),
                      '', 1)


# io error, file does not exist
def test_file_does_not_exist():
    helper_test_match(SIMPLEDIR, 'search does_not_exist',
                      'pwgrep: does_not_exist: No such file or directory\n',
                      '', 1)


# directory

def test_file_is_directory(tmpdir):
    filename = str(tmpdir)
    helper_test_match(SIMPLEDIR, 'directory {}'.format(filename),
                      'pwgrep: {}: is a directory\n'.format(filename),
                      '', 1)


def test_current_dir_is_directory():
    helper_test_match(SIMPLEDIR, 'directory .',
                      'pwgrep: .: is a directory\n', '', 1)


# inverse search
def test_inverse_l():
    expected_stdout = """Binary file helloworld matches
zen_of_python.txt:The Zen of Python, by Tim Peters
zen_of_python.txt:
zen_of_python.txt:Sparse is better than dense.
zen_of_python.txt:In the face of ambiguity, refuse the temptation to guess.
zen_of_python.txt:Now is better than never.
"""
    helper_test_match(SIMPLEDIR, '-v l *', expected_stdout, '', 0)


def test_inverse_h():
    expected_stdout = """Binary file helloworld matches
zen_of_python.txt:
zen_of_python.txt:Readability counts.
zen_of_python.txt:Unless explicitly silenced.
"""
    helper_test_match(SIMPLEDIR, '-v h *', expected_stdout, '', 0)


# --info
@pytest.mark.skipif(sys.version_info < (3, 4),
                    reason="Before Python 3.4, --info writes to stderr")
def test_version_to_stdout():
    helper_test_match(SIMPLEDIR, '--version', 'pwgrep 0.0.1\n', '', 0)


@pytest.mark.skipif(not (sys.version_info < (3, 4)),
                    reason="On and after Python 3.4, --info writes to stdout")
def test_version_to_stderr():
    helper_test_match(SIMPLEDIR, '--version', '', 'pwgrep 0.0.1\n', 0)


# color output
def test_color_simple():
    expected_stdout = r'[96mzen_of_python.txt[0m:The [1m[91mZen[0m of ' \
                      'Python, by Tim Peters\n'
    helper_test_match(SIMPLEDIR, '--color=always Zen *',
                      expected_stdout, '', 0)


def test_color_readability():
    expected_stdout = r'[96mzen_of_python.txt[0m:[1m[91mReadability[0m ' \
                      r'counts.' + '\n'
    helper_test_match(SIMPLEDIR, '--color=always Readability *',
                      expected_stdout, '', 0)


def test_color_no_color():
    expected_stdout = 'zen_of_python.txt:The Zen of Python, by Tim Peters\n'
    helper_test_match(SIMPLEDIR, '--color=never Zen *', expected_stdout, '', 0)


def test_color_auto_color():
    expected_stdout = 'zen_of_python.txt:The Zen of Python, by Tim Peters\n'
    helper_test_match(SIMPLEDIR, '--color=auto Zen *', expected_stdout, '', 0)


# Wrong options
def test_color_wrong_option():
    # argparse exits with exit code 2 ('incorrect usage')
    expected_stderr = """usage: pwgrep [-R | -r] [-h] [-i] [-v] [-o] [--color [COLOR]] [--version]
              [--help]
              PATTERN [PATH [PATH ...]]
pwgrep: error: argument --color: unrecognized is not a valid color option
"""
    helper_test_match(SIMPLEDIR, '--color=unrecognized foo *',
                      '', expected_stderr, 2)


def test_regex_wrong_option():
    expected_stderr = """usage: pwgrep [-R | -r] [-h] [-i] [-v] [-o] [--color [COLOR]] [--version]
              [--help]
              PATTERN [PATH [PATH ...]]
pwgrep: error: argument -r/--recursive: not allowed with argument -R/--dereference-recursive
"""
    helper_test_match(SIMPLEDIR, '-R -r Hello .', '', expected_stderr, 2)


@pytest.mark.skipif(sys.version_info >= (3, 5),
                    reason="Before Python 3.4, exception does not "
                           "print out position")
def test_regex_wrong_regex_1_py2():
    expected_stderr = """usage: pwgrep [-R | -r] [-h] [-i] [-v] [-o] [--color [COLOR]] [--version]
              [--help]
              PATTERN [PATH [PATH ...]]
pwgrep: error: argument PATTERN: * is an invalid regular expression: 'nothing to repeat'
"""
    helper_test_match(SIMPLEDIR, '\* Hello',
                      '', expected_stderr, 2)


@pytest.mark.skipif(sys.version_info < (3, 5),
                    reason="From Python 3 on, exception does not "
                           "print out position")
def test_regex_wrong_regex_1_py3():
    expected_stderr = """usage: pwgrep [-R | -r] [-h] [-i] [-v] [-o] [--color [COLOR]] [--version]
              [--help]
              PATTERN [PATH [PATH ...]]
pwgrep: error: argument PATTERN: * is an invalid regular expression: 'nothing to repeat at position 0'
"""
    helper_test_match(SIMPLEDIR, '\* Hello',
                      '', expected_stderr, 2)

# stdin
def test_stdin_l():
    stdin = b"""Hello
    World
    how
    are
    you?
    """
    helper_test_match(SIMPLEDIR, 'l', 'Hello\nWorld\n', '', 0, stdin)


def test_stdin_year():
    stdin = b"""Happy New
    Year 2016
    to all of you
    """
    helper_test_match(SIMPLEDIR, 'Year', 'Year 2016\n', '', 0, stdin)


# recursion
def test_recursion_text():
    helper_test_match(TREEDIR, '-R Zen .',
                      './B/A/B/zen_of_python.txt:The Zen of '
                      'Python, by Tim Peters\n', '', 0)


def test_recursion_binary():
    helper_test_match(TREEDIR, '-R ll .',
                      'Binary file ./A/helloworld matches\n', '', 0)


# Test symlinks
# Warning: These will fail on OS that do not
# support symlinks (for example FAT32)

# recursion
def test_symlink_follow_links():
    helper_test_match(SYMLINKDIR, '-R ll .',
                      'Binary file ./linked_tree/A/helloworld matches\n',
                      '', 0)


def test_symlink_do_not_follow_links():
    helper_test_match(SYMLINKDIR, '-r ll .', '', '', 1)


# infinite recursion tests
def test_infinite_symlink_do_not_follow_links():
    helper_test_match(INFINITE_RECURSION_LINK, '-r Zen .',
                      './outter/zen_of_python.txt:The Zen of Python, by Tim '
                      'Peters\n', '', 0)


def test_infinite_symlink_do_follow_links():
    helper_test_match(INFINITE_RECURSION_LINK, '-R Zen .',
                      './outter/zen_of_python.txt:The Zen of Python, by Tim '
                      'Peters\n',
                      'pwgrep: warning: ./outter/inner: recursive directory '
                      'loop\n',
                      0)
