#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import subprocess


def caller(directory, command, stdin=None):
    proc=subprocess.Popen('../../../pwgrep/pwgrep.py {}'.format(command),
                     cwd=directory,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True,
                     stdin=subprocess.PIPE)
    #if stdin:
        #proc.stdin.write(stdin)
        #proc.stdin.flush()
        #proc.stdin.close()
    #proc.wait()
    if stdin:
        stdout, stderr = proc.communicate(stdin)#, timeout=TEST_TIMEOUT)
    else:
        stdout, stderr = proc.communicate()#, timeout=TEST_TIMEOUT)

    code=proc.returncode
    return code, stdout,stderr

simpledir = r'./tests/data/simple'


def helper_test_match(directory, command, stdout_shall, stderr_shall,
                      return_code_shall, stdin=None):
    return_code_is, stdout_is, stderr_is = caller(directory, command, stdin)
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

# io error, file does not exist
def test_file_does_not_exist(tmpdir):
    helper_test_match(simpledir, 'search does_not_exist',
                      'pwgrep: does_not_exist: No such file or directory\n',
                      '', 1)

# directory

def test_file_is_directory(tmpdir):
    filename = str(tmpdir)
    helper_test_match(simpledir, 'directory {}'.format(filename),
                      'pwgrep: {}: is a directory\n'.format(filename),
                      '', 1)


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


# --info
def test_version():
    # argparse prints '--version' to stderr due to compatibility reasons
    helper_test_match(simpledir, '--version', '', 'pwgrep.py 0.0.1\n', 0)


# color output
def test_color_simple():
    expected_stdout=r'[96mzen_of_python.txt[0m:The [1m[91mZen[0m of Python, ' \
               'by Tim Peters\n'
    helper_test_match(simpledir, '--color=always Zen *', expected_stdout, '', 0)


def test_color_readability():
    expected_stdout=r'[96mzen_of_python.txt[0m:[1m[91mReadability[0m ' \
                     r'counts.'+'\n'
    helper_test_match(simpledir, '--color=always Readability *',
                          expected_stdout, '', 0)


def test_color_no_color():
    expected_stdout='zen_of_python.txt:The Zen of Python, by Tim Peters\n'
    helper_test_match(simpledir, '--color=never Zen *', expected_stdout, '', 0)


def test_color_auto_color():
    expected_stdout='zen_of_python.txt:The Zen of Python, by Tim Peters\n'
    helper_test_match(simpledir, '--color=auto Zen *', expected_stdout, '', 0)


def test_color_wrong_option():
    # argparse exits with exit code 2 ('incorrect usage')
    expected_stderr="""usage: pwgrep.py [-R] [-r] [-h] [-i] [-v] [-o] [--color [COLOR]] [--version]
                 [--help]
                 PATTERN [PATH [PATH ...]]
pwgrep.py: error: argument --color: unrecognized is not a valid color option
"""
    helper_test_match(simpledir, '--color=unrecognized foo *',
                          '', expected_stderr, 2)

# stdin
def test_stdin_l():
    stdin = b"""Hello
    World
    how
    are
    you?
    """
    helper_test_match(simpledir, 'l', 'Hello\nWorld\n', '', 0, stdin)

def test_stdin_year():
    stdin = b"""Happy New
    Year 2016
    to all of you
    """
    helper_test_match(simpledir, 'Year', 'Year 2016\n', '', 0, stdin)


