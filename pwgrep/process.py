from pwgrep import file_helper
from pwgrep import printer_helper
from pwgrep import search_helper


def process_stdin(regex, invert_match=False, color=False):
    """
    Processes grep operation on stdin
    :param regex: Regex used for matching text
    :param invert_match: If match result shall be inversed
    :param color: If output shall be colored
    :return: If any match occurred
    """
    match_occurred = False
    for _, line in search_helper.search_in_stdin(regex, invert_match):
        match_occurred = True
        printer_helper.print_match('', line, regex, True, False, color)
    return match_occurred


def process_commandline(files, regex_txt, regex_bin, invert_match=False,
                        color=False,
                        recursive=False, dereference_recursive=False,
                        no_filename=False):
    """
    Processes grep operation on stdin
    :param files: Files to be processed
    :param regex_txt: Regex used for matching text
    :param regex_bin: Regex used for matching binary
    :param invert_match: If match result shall be inversed
    :param color: If output shall be colored
    :param recursive: If recursion shall be used on directories
    :param dereference_recursive: If recursion shall be used on directories,
    following symlinks
    :param no_filename: If printing of filename shall be suppressed
    :return: If any match occurred
    """
    match_occurred = False
    for file_name in files:
        if file_helper.file_is_directory(file_name):
            if not (dereference_recursive or recursive):
                printer_helper.print_is_directory(file_name)
            else:
                for filename in file_helper.recurse(file_name,
                                                    dereference_recursive):

                    if search_helper.search_in_file(filename, regex_txt,
                                                    regex_bin,
                                                    invert_match,
                                                    no_filename, color):
                        match_occurred = True
        else:
            if search_helper.search_in_file(file_name, regex_txt, regex_bin,
                                            invert_match,
                                            no_filename, color):
                match_occurred = True
    return match_occurred
