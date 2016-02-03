from pwgrep import file_helper
from pwgrep import printer_helper
from pwgrep import search_helper
from pwgrep import search_result

import sys


class Grepper(object):

    def __init__(self, commandline_parser_results):
        self.commandline_parser_results = commandline_parser_results
        self.regex_searcher = search_helper.RegexSearcher(
            self.commandline_parser_results.regexes,
            invert_match=self.commandline_parser_results.invert_match)

    def grep_stdin(self):
        """
        Process grep operation on stdin.

        :return: If any match occurred
        """

        for result in self.regex_searcher.search_in_stdin():
            yield result

    def handle_directory(self, file_name):
        if not self.commandline_parser_results.recursion_any:
            printer_helper.print_is_directory(file_name)
        else:
            for filename in file_helper.files_from_directory_recursive(
                file_name,
                    self.commandline_parser_results.dereference_recursive):
                for match in self.regex_searcher.search_in_file(filename):
                    yield match

    def grep_files_from_commandline(self):
        """
        Process grep operation on files specified via commandline.

        following symlinks
        :return: If any match occurred
        """

        for file_name in self.commandline_parser_results.PATH:
            if file_helper.file_is_directory(file_name):
                for match in self.handle_directory(file_name):
                    yield match
            else:
                for match in self.regex_searcher.search_in_file(file_name):
                    yield match

    def grep(self):
        if self.commandline_parser_results.PATH:
            for result in self.grep_files_from_commandline():
                yield result

        for result in self.grep_stdin():
            yield result
