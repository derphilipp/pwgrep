class SearchResult(object):
    def __init__(self,
                 line_number=None,
                 before_match_text=None,
                 match_text=None,
                 after_match_text=None,
                 filename=None
                 ):

        self.line_number = line_number
        self.before_match_text = before_match_text
        self.match_text = match_text
        self.after_match_text = after_match_text
        self.filename = filename
