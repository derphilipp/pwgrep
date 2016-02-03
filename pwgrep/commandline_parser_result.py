"""CommandLineParser Result"""

import os
import re
import sys


class RegexContainer(object):

    """ Container class to store textual and binary regex."""

    def __init__(self, regex_text, ignore_case):
        """
        Initialize Regex container.

        :param regex_txt: Regex for matches in text-files
        :param regex_bin: Regex for matches in binary files
        :return:
        """

        regex_flags = 0
        if ignore_case:
            regex_flags |= re.IGNORECASE
        self.regex_txt = re.compile(regex_text, regex_flags)
        self.regex_bin = re.compile(str.encode(regex_text), regex_flags)


class CommandLineParserResult(object):

    """Result of Command Line Parser."""

    def __init__(self, options):
        """
        Create instance of CommandLineParserResult.

        :param options: CommandLineParameter options
        :return:
        """
        self._options = options
        self.regexes = RegexContainer(
            self._options.PATTERN[0],
            self._options.ignore_case
        )

    @property
    def color(self):
        """
        Should output be displayed in color.

        :return: If color should be used
        """
        if self._options.color is None or self._options.color == 'never':
            return False
        if self._options.color == 'always':
            return True
        # can only be 'auto' at this point
        return os.isatty(sys.stdout.fileno())

    @property
    def recursion_any(self):
        return self.dereference_recursive or self.normal_recursive

    @property
    def dereference_recursive(self):
        return self._options.dereference_recursive

    @property
    def normal_recursive(self):
        return self._options.recursive

    @property
    def print_filename(self):
        if self._options.no_filename:
            return False
        if len(self._options.PATH) == 1 and not self.recursion_any:
            return False
        return True

    @property
    def PATH(self):
        return self._options.PATH

    @property
    def invert_match(self):
        return self._options.invert_match
