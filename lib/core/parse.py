# -*- coding: utf-8 -*-
"""
Simple parsers
"""


class LineByLineParser(object):
    """
    Simple line-by-line text parser.
    """

    def __init__(self):
        self._patterns = {}

    def register_pattern(self, pattern, key, parser=lambda x: x):
        """
        Register @pattern (and optional @parser) for @key.
        If parsed line contains the pattern, rightmost part of line
        will be stored as value for @key in resulting dict
        """
        assert isinstance(pattern, basestring)
        self._patterns[pattern] = (key, parser)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            key, parser = key.start, key.stop
        else:
            parser = lambda x: x
        self.register_pattern(key, value, parser)

    def parse(self, lines):
        """
        Parse @lines and return dict with values
        """
        res = {}
        if self._patterns:
            for line in lines:
                for pattern, (key, parser) in self._patterns.iteritems():
                    pos = line.find(pattern)
                    if pos >= 0:
                        res[key] = parser(line[pos + len(pattern):].strip())
                        continue
        return res
