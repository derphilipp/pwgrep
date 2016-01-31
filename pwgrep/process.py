from pwgrep import file_helper
from pwgrep import printer_helper
from pwgrep import search_helper


def grep_stdin(regexes, invert_match=False, color=False):
    """
    Process grep operation on stdin.

    :param regexes: Regexes used for matching text
    :param invert_match: If match result shall be inversed
    :param color: If output shall be colored
    :return: If any match occurred
    """
    match_occurred = False
    for _, line in search_helper.search_in_stdin(
        regexes.regex_txt, invert_match
    ):
        match_occurred = True
        printer_helper.print_match('', line, regexes.regex_txt,
                                   True, False, color)
    return match_occurred


def grep_files_from_commandline(files, regexes,
                                invert_match=False,
                                color=False,
                                recursive=False, dereference_recursive=False,
                                no_filename=False):
    """
    Process grep operation on files specified via commandline.

    :param files: Files to be processed
    :param regexes: Regex container, containing binary and textual regex
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
                for filename in file_helper.files_from_directory_recursive(
                    file_name,
                    dereference_recursive
                ):

                    if search_helper.search_in_file(filename, regexes,
                                                    invert_match,
                                                    no_filename, color):
                        match_occurred = True
        else:
            if search_helper.search_in_file(file_name, regexes,
                                            invert_match,
                                            no_filename, color):
                match_occurred = True
    return match_occurred
