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
from Queue import Queue
from threading import Thread

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

    MULTITHREADED = True

    def __init__(self, **kwargs):
        self.main(self, **kwargs)

    def main(self, **kwargs):
        query = None
        query_prefix = None
        pages_depth = None
        results = None
        opener = None
        ND_query = None

        def fetch(URL):
            """
            @return: page content as string
            """
            data = opener.open(URL)
            data_content = data.read()

            return data_content

        def parse(data,regexp):
            data_striped = data
            match = regexp.findall(data_striped)

            def process_match(data):
                if not data in results:
                    results.append(data)
            map(process_match,match)

        def Google():
            """
            fetch Google search pages
            """
            if query_prefix:
                search_query = '%s:%s' % (query_prefix, query)
            else:
                search_query = query

            request_uri = '/search?hl=en&lr=&ie=UTF-8' \
                '&q=%s&sa=N&filter=0' % (
                    urllib2.quote(search_query),
                )

            data = fetch('http://www.google.com%s' % request_uri)
            regexp = re.compile(r'<h3.+?href="/url\?q=(.*?%s.*?)&' % query,re.I)
            parse(data,regexp)

            # follow next 10 pages (100 results in total)
            for page in range(10, pages_depth * 10, 10):
                # make sure we're not too frequent, to avoid abuse detection
                time.sleep(5)
                request_uri = '/search?hl=en&lr=&ie=UTF-8' \
                    '&q=%s&sa=N&start=%s&filter=0' % (
                        urllib2.quote(search_query),
                        page,
                    )
                data = fetch('http://www.google.com%s' % request_uri)
                parse(data,regexp)

            # refine results:
            filtered_results = []
            re_filter = re.compile(r'(.*%s.*)' % query, re.I)

            def filter_results(data):
                match = re_filter.search(data.replace('http://','').
                    replace('https://','').split('/')[0])
                if match:
                    if not match.group(1) in filtered_results:
                        filtered_results.append(match.group(1))

            map(filter_results, results)
            results = filtered_results

        def Namedroppers():
            """
            http://www.namedroppers.com/cgi-bin/query?
            http://www.namedroppers.org/cgi-bin/query?keys=netprotect
            """
            request_uri = '/cgi-bin/query?keys=%s' % ND_query
            data = fetch('http://www.namedroppers.org%s' % request_uri)

            # now quickly and simply parse results for matching hostname:
            regexp_ND = re.compile(r'who\/(.+?)"',re.I)
            parse(data,regexp_ND)

            # now lets parse some following pages...
            regexp = re.compile(r'cgi-bin\/query\?p=(\d+?)&',re.I)
            match = regexp.findall(data)
            pages = []

            def process_page(data):
                if not data in pages:
                    pages.append(data)
                    request_uri = '/cgi-bin/query?p=%s&k=%s' % (
                        data,
                        ND_query
                    )
                    data = fetch('http://www.namedroppers.org%s' % request_uri)
                    parse(data, regexp_ND)

            # parse pages
            map(process_page,match)

        query = kwargs['q'] or kwargs['query']
        query_prefix = kwargs['query_prefix'] or None
        pages_depth = kwargs['depth'] or 1

        results = []
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        ND_query = query.split('.')[0]
        Namedroppers()


class WebSearchClientDomains(Task):
    """
    Web search task
    """

    def main(self,*args,**kwargs):
        """
        Main function
        """
        def worker():
            while True:
                target = self.queue.get()
                host = '%s://%s' % (self.proto or 'http', target)
                self._write_result(host)

                s = WebSearch(
                    q=host,
                    query_prefix='allinurl',
                    depth=PARSE_GOOGLE_PAGES
                )

                def print_results(data):
                    self.lock.acquire()

                    self._write_result(data)

                    self.lock.release()

                map(print_results,s.results)

                self.queue.task_done()

        # Targets queue
        self.queue = Queue()

        for _ in range(self.THREADS_COUNT):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        for target in self.targets:
            self.queue.put(target)

        self.queue.join()

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(WebSearchClientDomains)
