#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SearchResult(object):

    def __init__(self):
        pass


class FileSearchResult(object):

    def __init__(self, filename=None):
        super(FileSearchResult, self).__init__()
        self.filename = filename
        assert(self.filename is not None)


class BinarySearchResult(FileSearchResult):

    def __init__(self, filename=None):
        super(BinarySearchResult, self).__init__(filename)
        self.match = True


class TextSearchResult(FileSearchResult):

    def __init__(self, line_number=None, line=None, match=None, filename=None):
        super(TextSearchResult, self).__init__(filename)
        self.line_number = line_number
        self.match = match
        self.line = line
        assert(self.line_number is not None)
        assert(self.line is not None)


class StdinSearchResult(SearchResult):

    def __init__(self, line_number=None, line=None, match=None):
        super(StdinSearchResult, self).__init__()
        self.line_number = line_number
        self.match = match
        self.line = line
        assert(self.line is not None)
        assert(self.line_number is not None)
