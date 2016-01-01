import pwgrep.file_helper


def test_file_is_binary():
    assert pwgrep.file_helper.file_is_binary('data/simple/helloworld') == True


def test_file_is_text():
    assert pwgrep.file_helper.file_is_binary('data/simple/zen_of_python.txt')\
           == False

