import pytest
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

def test_text_match():
    """ggrep Zen *"""
    code, result, err = caller('simple', 'Zen *')
    assert err == ''
    assert result == 'zen_of_python.txt:The Zen of Python, by Tim Peters\n'
    assert code == 0


def test_binary_match():
    """ggrep Hello *"""
    code, result, err = caller('simple', 'Hello *')
    assert err == ''
    assert result == 'Binary file helloworld matches\n'
    assert code == 0


def test_no_match():
    """ggrep Hello *"""
    code, result, err = caller('simple', 'ThisIsNeverFound *')
    assert err == ''
    assert result == ''
    assert code == 1


def test_text_match_no_filename():
    """ggrep -h Zen *"""
    code, result, err = caller('simple', '-h Zen *')
    assert err == ''
    assert result == 'The Zen of Python, by Tim Peters\n'
    assert code == 0


def test_binary_match_no_filename():
    """ggrep -h Zen *"""
    code, result, err = caller('simple', '-h Hello *')
    assert err == ''
    assert result == 'Binary file helloworld matches\n'
    assert code == 0
