# -*- coding: utf-8 -*-
"""
$Id: google_search_email.py,v 1.19 2013/02/07 11:13:49 dee Exp $
"""

import json
import urllib
import re
import sys
sys.path.append('pythonlib')
from gtta import Task, execute_task

class GoogleSearchAPI(object):
    """
    API Access Notice: https://developers.google.com/errors/
    Note: The Google Search and Language APIs shown to the right have been
    officially deprecated. They will continue to work as per our deprecation 
    policy, but the number of requests you may make per day will be limited. 
    Please visit the documentation for each API for further details and 
    alternatives.

    @author: d@d.kiev.ua
    @return: Stores JSON results in self.results
    """
    def __init__(self,**kwargs):
        self.query = kwargs['q'] or kwargs['query']
        self.results = []
        self._fetch()

    def _fetch(self):
        def map_func(data):
            self.results.append(data)

        for scope in ['web','blogs']:
            self.query_url = 'http://ajax.googleapis.com/ajax/services/search/%s?v=1.0&q=%s' % (
                scope,self.query
            )
            search_response = urllib.urlopen(self.query_url)
            search_results = search_response.read()
            results = json.loads(search_results)
            if not 200 == results['responseStatus']:
                raise NoDataReturned(json.dumps(results))
            map(map_func,results['responseData']['results'])
            for page in results['responseData']['cursor']['pages']:
                if 1 == page['label']: continue
                next_page_url = '{0}&start={1}'.format(self.query_url,page['start'])
                search_response = urllib.urlopen(next_page_url)
                search_results = search_response.read()
                results = json.loads(search_results)
                map(map_func,results['responseData']['results'])


class GoogleSearchForEmails(GoogleSearchAPI):
    """
    Search for emails in  Google AJAX API search results for specified query

    @author: d@d.kiev.ua
    """
    def __init__(self,**kwargs):
        self._results = []
        def map_func(data):
            re_match = re_email.match(json.dumps(data))
            if re_match:
                self._results.append(data)
        super(GoogleSearchForEmails,self).__init__(**kwargs)
        re_email = re.compile(r'(.+\@%s)' % self.query)
        map(map_func,self.results)
        self.results = self._results

class GoogleSearchForEmailsTask(Task):
    """
    GTTA check to search for emails in Google results
    """
    TIMEOUT=120
    def main(self,*args,**kwargs):
        s = GoogleSearchForEmails(q=self.host)
        if len(s.results):
            self._write_result('FOUND %s:\n\n%s' % (
                len(s.results),
                json.dumps(s.results,sort_keys=True,indent=4)
            ))
        else:
            self._write_result('GOOGLE SHOWS NO EMAIL IN RESULTS FOR "@%s"' % self.host)

execute_task(GoogleSearchForEmailsTask)

