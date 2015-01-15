# -*- coding: utf-8 -*-
"""
 Get other domains possibly owned by client

  1. from Google
  2. http://www.namedroppers.org/link.html

 Queries each opt and parses for target hostname

 d@d.kiev.ua $Id: websearch_client_domains.py,v 1.2 2013/02/17 10:59:55 dee Exp $
"""

import urllib2
import re
import time
from core import Task, execute_task

PARSE_GOOGLE_PAGES = 10


class WebSearch(object):
    """
    Web search routines for GTTA
    query_prefix    : e.g. 'allinurl', DEFAULT: no prefx
    query           : search query, REQUIRED
    depth           : how many result pages should be traversed, DEFAULT: 1

    @kwargs: query_prefix
    @kwargs: query
    @kwargs: depth
    @return: list in self.results
    """
    def __init__(self,**kwargs):
        self.query = kwargs['q'] or kwargs['query']
        self.query_prefix = kwargs['query_prefix'] or None
        self.pages_depth = kwargs['depth'] or 1

        self.results = []
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #self._Google()
        
        # Namedroppers expect hostname without TLD
        # TODO: here we assuming that query is a hostname
        # otherwise querystring will be cut after first appearing dot '.'
        self.ND_query = self.query.split('.')[0]
        self._Namedroppers()

    def _fetch(self,URL):
        """
        @return: page content as string
        """
        data = self.opener.open(URL)
        data_content = data.read()

        return data_content

    def _parse(self,data,regexp):
        data_striped = data
        match = regexp.findall(data_striped)

        def process_match(data):
            if not data in self.results:
                self.results.append(data)
        map(process_match,match)

    def _Google(self):
        """
        fetch Google search pages
        """
        if self.query_prefix:
            search_query = '%s:%s' % (self.query_prefix,self.query)
        else:
            search_query = self.query

        request_uri = '/search?hl=en&lr=&ie=UTF-8' \
            '&q=%s&sa=N&filter=0' % (
                urllib2.quote(search_query),
            )

        data = self._fetch('http://www.google.com%s' % request_uri)
        regexp = re.compile(r'<h3.+?href="/url\?q=(.*?%s.*?)&' % self.query,re.I)
        self._parse(data,regexp)

        # follow next 10 pages (100 results in total)
        for page in range(10, self.pages_depth * 10, 10):
            # make sure we're not too frequent, to avoid abuse detection
            time.sleep(5)
            request_uri = '/search?hl=en&lr=&ie=UTF-8' \
                '&q=%s&sa=N&start=%s&filter=0' % (
                    urllib2.quote(search_query),
                    page,
                )
            data = self._fetch('http://www.google.com%s' % request_uri)
            self._parse(data,regexp)
            
        # refine results:
        filtered_results = []
        re_filter = re.compile(r'(.*%s.*)' % self.host,re.I)

        def filter_results(data):
            match = re_filter.search(data.replace('http://','').
                replace('https://','').split('/')[0])
            if match:
                if not match.group(1) in filtered_results:
                    filtered_results.append(match.group(1))
        map(filter_results,self.results)
        self.results = filtered_results

    def _Namedroppers(self):
        """
        http://www.namedroppers.com/cgi-bin/query?
        http://www.namedroppers.org/cgi-bin/query?keys=netprotect
        """
        request_uri = '/cgi-bin/query?keys=%s' % self.ND_query
        data = self._fetch('http://www.namedroppers.org%s' % request_uri)

        # now quickly and simply parse results for matching hostname:
        regexp_ND = re.compile(r'who\/(.+?)"',re.I)
        self._parse(data,regexp_ND)

        # now lets parse some following pages...
        regexp = re.compile(r'cgi-bin\/query\?p=(\d+?)&',re.I)
        match = regexp.findall(data)
        pages = []

        def process_page(data):
            if not data in pages:
                pages.append(data)
                request_uri = '/cgi-bin/query?p=%s&k=%s' % (
                    data,
                    self.ND_query
                )
                data = self._fetch('http://www.namedroppers.org%s' % request_uri)
                self._parse(data, regexp_ND)

        # parse pages
        map(process_page,match)


class WebSearchClientDomains(Task):
    """
    Web search task
    """
    TIMEOUT = 120

    def main(self,*args,**kwargs):
        """
        Main function
        """
        host = '%s://%s' % (self.proto or 'http', self.host)

        s = WebSearch(
            q=host,
            query_prefix='allinurl',
            depth=PARSE_GOOGLE_PAGES
        )

        def print_results(data):
            self._write_result(data)

        map(print_results,s.results)

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(WebSearchClientDomains)
