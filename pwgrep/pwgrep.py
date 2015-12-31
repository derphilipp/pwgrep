#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import os
import argparse

from version import VERSION


# [-R|-r] [-h] [-i] [-v] [-o] [--color[=(never|always|auto)] PATTERN [PATH ..]
class CommandParser(object):
    def __init__(self, args):
        self._parser = argparse.ArgumentParser(add_help=False)

        self._parser.add_argument(
            '-R','--dereference-recursive',
            action='store_true',
            help='For each directory operand, read and process all files in that directory, recursively, following all symbolic links.'
        )
        self._parser.add_argument(
            '-r', '--recursive',
            action='store_true',
            help='For each directory operand, read and process all files in that directory, recursively.  Follow symbolic links on the command line, but skip symlinks that are encountered recursively.  Note that if no file operand is given, grep searches the working directory. This is the same as the ‘--directories=recurse’ option.'
            )
        self._parser.add_argument(
                '-h', '--no-filename',
                action='store_true',
                help='Suppress the prefixing of file names on output. This is the default when there is only one file (or only standard input) to search.'
            )
        self._parser.add_argument(
                '-i', '-y', '--ignore-case',
                action='store_true',
                help='Ignore case distinctions, so that characters that differ only in case match each other. Although this is straightforward when letters differ in case only via lowercase-uppercase pairs, the behavior is unspecified in other situations.  For example, uppercase “S” has an unusual lowercase counterpart “ſ” (Unicode character U+017F, LATIN SMALL LETTER LONG S) in many locales, and it is unspecified whether this unusual character matches “S” or “s” even though uppercasing it yields “S”.  Another example: the lowercase German letter “ß” (U+00DF, LATIN SMALL LETTER SHARP S) is normally capitalized as the two-character string “SS” but it does not match “SS”, and it might not match the uppercase letter “ẞ” (U+1E9E, LATIN CAPITAL LETTER SHARP S) even though lowercasing the latter yields the former. ‘-y’ is an obsolete synonym that is provided for compatibility. ("-i" is specified by POSIX.))'
                )
        self._parser.add_argument(
                '-v', '--invert-match',
                action='store_true',
                help='Invert the sense of matching, to select non-matching lines.  (‘-v’ is specified by POSIX.)'
                )


        self._parser.add_argument('-o', '--only-matching',
                                  action='store_true',
                                  help='Print only the matched (non-empty) parts of matching lines, with each such part on a separate output line.')


        self._parser.add_argument('--color', nargs='?', default='never',
                                  help='Mark up the matching text.  The possible values of when can be "never", "always" or "auto".')

        self._parser.add_argument('PATTERN',
                                  metavar='PATTERN', type=str, nargs=1,
                                  help='Pattern to search for')
        self._parser.add_argument('PATH',
                                  metavar='PATH', type=str, nargs='*',
                                  help='Path(s) to search in')
        self._parser.add_argument('--version', action='version', version='%(prog)s {}'.format(VERSION))
        self._parser.add_argument('--help', action='help', help='Displays this help page')
        self.options = self._parser.parse_args()

    @property
    def color(self):
        if self.args.color is None or self.args.color == 'never':
            return False
        if self.args.color == 'always':
            return True
        if self.args.color == 'auto':
            return os.isatty(sys.stdout.fileno())
        # TODO More userfriendly error handling
        raise ValueError('Invalid type of color "{}" set'.format(self.args.color))





def display_version():
    print("Version {}".format(VERSION))


if __name__ == "__main__":
    p = CommandParser(sys.argv)
    print(p.options)
