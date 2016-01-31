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
        self.options = options
        self.regexes = RegexContainer(
            self.options.PATTERN[0],
            self.options.ignore_case
        )

    @property
    def color(self):
        """
        Should output be displayed in color.

        :return: If color should be used
        """
        if self.options.color is None or self.options.color == 'never':
            return False
        if self.options.color == 'always':
            return True
        # can only be 'auto' at this point
        return os.isatty(sys.stdout.fileno())
