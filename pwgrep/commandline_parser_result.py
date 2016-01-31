import os
import sys


class CommandLineParserResult(object):
    def __init__(self, options):
        self.options = options

    @property
    def color(self):
        if self.options.color is None or self.options.color == 'never':
            return False
        if self.options.color == 'always':
            return True
        # can only be 'auto' at this point
        return os.isatty(sys.stdout.fileno())
