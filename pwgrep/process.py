from pwgrep import file_helper
from pwgrep import printer_helper
from pwgrep import search_helper
from pwgrep import search_result

import sys


class RegexSearcher(object):

    def __init__(self, regexes):
        self.regexes = regexes

    def search_line_txt(self, line):
        result = []
        for m in self.regexes.regex_txt.finditer(line):
            result.append([m.start(), m.end()])
        return result


class SearchStdin(object):

    def __init__(self, regexes, invert_match=False):
        """
        Search for regex in stdin.

        :param regexes:              regex to search with
        :param invert_match:         if match should be inverted
                                    (i.e. non-matches shall match)
        """
        self.regexes = regexes
        self.invert_match = invert_match
        self.rs = RegexSearcher(self.regexes)

    def __iter__(self):
        for line_nr, line in enumerate(sys.stdin):
            match = self.rs.search_line_txt(line)
            if match:
                yield search_result.StdinSearchResult(
                        line_number=line_nr,
                        match=match, line=line)


class Grepper(object):

    def __init__(self, commandline_parser_results):
        self.commandline_parser_results = commandline_parser_results
        self.options = self.commandline_parser_results.options

        self.match_occurred = False

    def grep_stdin(self):
        """
        Process grep operation on stdin.

        :return: If any match occurred
        """

        searcher = SearchStdin(
            self.commandline_parser_results.regexes,
            self.commandline_parser_results.options.invert_match)

        for result in searcher:
            # printer_helper.print_match('', result.match,
            #                           self.commandline_parser_results.
            #                           regexes.regex_txt,
            #                           True, False,
            #                           self.commandline_parser_results.color
            #                           )
            yield result

    def grep_files_from_commandline(self):
        """
        Process grep operation on files specified via commandline.

        following symlinks
        :return: If any match occurred
        """
        # rs = RegexSearcher(self.commandline_parser_results.regexes)

        for file_name in self.commandline_parser_results.options.PATH:
            if file_helper.file_is_directory(file_name):
                if not (self.options.dereference_recursive or
                        self.options.recursive):
                    printer_helper.print_is_directory(file_name)
                else:
                    for filename in file_helper.files_from_directory_recursive(
                        file_name,
                        self.options.dereference_recursive
                    ):
                        for match in search_helper.search_in_file(
                            filename,
                            self.commandline_parser_results.regexes,
                            self.commandline_parser_results.
                            options.invert_match,
                            self.commandline_parser_results.print_filename,
                            self.commandline_parser_results.color
                        ):
                            yield match
            else:
                for match in search_helper.search_in_file(
                    file_name,
                    self.commandline_parser_results.regexes,
                    self.commandline_parser_results.options.invert_match,
                    self.commandline_parser_results.options.no_filename,
                    self.commandline_parser_results.color
                ):
                    yield match
