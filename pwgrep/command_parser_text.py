#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

IGNORE_CASE = u'Ignore case distinctions, so that characters that differ only' \
    u' in case match each other. Although this is straightforward when ' \
    u'letters differ in case only via lowercase-uppercase pairs, the behavior' \
    u' is unspecified in other situations.  For example, uppercase “S” has an '\
    u'unusual lowercase counterpart “ſ” (Unicode character U+017F, '\
    u'LATIN SMALL LETTER LONG S) in many locales, and it isunspecified ' \
    u'whether this unusual character matches “S” or “s” even though ' \
    u'uppercasing it yields “S”. Another example: the lowercase German letter' \
    u' “ß” (U+00DF, LATIN SMALL LETTER SHARP S) is normally capitalized as ' \
    u'the two-character string “SS” but it does not match “SS”, and it might ' \
    u'not match the uppercase letter “ẞ” (U+1E9E, LATIN CAPITAL LETTER SHARP ' \
    u'S) even though lowercasing the latter yields the former. ‘-y’ is an ' \
    u'obsolete synonym that is provided for compatibility.' \
    u'("-i" is specified by POSIX.)'

DEREFERENCE_RECURSIVE = u'For each directory operand, read and process all ' \
    u'files in that directory, recursively, following all symbolic links.'

RECURSIVE = u'For each directory operand, read and process all files in that ' \
            u'directory, recursively. ' \
            u'Follow symbolic links on the command line, but skip symlinks ' \
            u'that are encountered recursively.'\
            u'Note that if no file operand is given, grep searches the ' \
            u'working directory.' \
            u'This is the same as the ‘--directories=recurse’ option.'

NO_FILENAME = u'Suppress the prefixing of file names on output. This is the ' \
              u'default when there is only one file '\
              u'(or only standard input) to search.'

INVERT_MATCH = u'Invert the sense of matching, to select non-matching ' \
               u'lines.  (‘-v’ is specified by POSIX.)'

ONLY_MATCHING = u'Print only the matched (non-empty) parts of matching ' \
                u'lines, with each such part on a separate output line.'

COLOR = u'Mark up the matching text. '\
        u'The possible values of when can be "never", "always" or "auto".'

PATTERN = u'Pattern to search for'
PATH = u'Path(s) to search in'
HELP = u'Displays this help page'
