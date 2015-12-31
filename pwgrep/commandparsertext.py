IGNORE_CASE = '''Ignore case distinctions, so that characters that differ only in case match each other.
    Although this is straightforward when letters differ in case only via lowercase-uppercase pairs,
            the behavior is unspecified in other situations.  For example, uppercase “S” has an unusual lowercase
            counterpart “ſ” (Unicode character U+017F, LATIN SMALL LETTER LONG S) in many locales, and it is
            unspecified whether this unusual character matches “S” or “s” even though uppercasing it yields “S”.
            Another example: the lowercase German letter “ß” (U+00DF, LATIN SMALL LETTER SHARP S) is normally
            capitalized as the two-character string “SS” but it does not match “SS”, and it might not match the
            uppercase letter “ẞ” (U+1E9E, LATIN CAPITAL LETTER SHARP S) even though lowercasing the latter yields
            the former. ‘-y’ is an obsolete synonym that is provided for compatibility.
            ("-i" is specified by POSIX.))'''

DEREFERENCE_RECURSIVE = 'For each directory operand, read and process all files in that directory, \
                  recursively, following all symbolic links.'

RECURSIVE = 'For each directory operand, read and process all files in that directory, recursively.\
            Follow symbolic links on the command line, but skip symlinks that are encountered recursively.\
            Note that if no file operand is given, grep searches the working directory. \
            This is the same as the ‘--directories=recurse’ option.'

NO_FILENAME = 'Suppress the prefixing of file names on output. This is the default when there is only one file \
            (or only standard input) to search.'

INVERT_MATCH = 'Invert the sense of matching, to select non-matching lines.  (‘-v’ is specified by POSIX.)'

ONLY_MATCHING = 'Print only the matched (non-empty) parts of matching lines, \
                                  with each such part on a separate output line.'

COLOR = 'Mark up the matching text. \
       The possible values of when can be "never", "always" or "auto".'
PATTERN = 'Pattern to search for'
PATH = 'Path(s) to search in'
HELP = 'Displays this help page'
