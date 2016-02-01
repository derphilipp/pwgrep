class SearchResult(object):
    def __init__(self, line_number, line, filename=None):
        self.line_number = line_number
        self.line = line
        self.filename = filename

