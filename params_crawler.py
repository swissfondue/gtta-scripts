# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from urlparse import urlsplit, parse_qs
import re
from HTMLParser import HTMLParser

from crawler import LinkCrawler
from gtta import Task, execute_task


class FormsParser(HTMLParser):

    form_attributes = dict()

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        at = dict(attrs)
        if tag == 'form':
            self.form_attributes = dict()
            self.form_attributes['action'] = at['action']
            self.form_attributes['inputs'] = []
        if tag == 'input':
            self.form_attributes['inputs'].append(at)


class Params_Craw(Task):
    """
    Complete parameters from forms and urls, using crawler.py
    """

    urls_set = set()
    forms_urls_set = set()
    form_parser = FormsParser()

    FORM_PATTERN = '(?i)<form([^>]+)>(.+?)</form>'
    INPUT_PATTERN = '(?i)<input(.+?)>'

    def collect_unique_urls(self, url):
        """
        Using as callback function for crawler
        """
        self.urls_set.add(url)

    def collect_params(self, url):
        """ Collecting params from link """

        if url not in self.urls_set:
            splitted_url = urlsplit(url)
            query_params = parse_qs(splitted_url[3])
            if query_params:
                self._write_result(splitted_url[0] + '://' + splitted_url[1] + splitted_url[2])
                #self._write_result(url)  # Need to know format: up or this
                for key, value in query_params.items():
                    self._write_result('\t' + key + '=' + value[0])
                    self._check_stop()
            self.collect_unique_urls(url)

    def collect_form_params(self, page):
        """ If we have on page form, then outputting that form url and params from there"""

        if page['url'] not in self.forms_urls_set:
            self.forms_urls_set.add(page['url'])

            for item in re.finditer(self.FORM_PATTERN, page['content'], re.S):  # Iterate all forms in page content
                self._check_stop()

                self.form_parser.feed(item.group(0))  # Parsing form action and inputs params with Form_Parser
                form_attributes = self.form_parser.form_attributes
                self._write_result('form action: ' + form_attributes['action'])

                for input_params in form_attributes['inputs']:  # Iterating all inputs attributes
                    self._check_stop()
                    input_params_formatted = ''

                    for key, value in input_params.items():
                        self._check_stop()
                        input_params_formatted += (key + '=' + value + ',')

                    self._write_result('\t' + input_params_formatted)

    def main(self):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.link_callback = self.collect_params
        link_crawler.link_content_callback = self.collect_form_params

        if not self.proto:
            self.proto = 'http'

        if self.host:
            target = self.proto + '://' + self.host + '/'

        else:
            target = self.proto + '://' + self.ip + '/'

        link_crawler.process(target)  # Starting recursive process of link crawling on target

        self._check_stop()

        if not self.produced_output:
            self._write_result('No link to any documents found')


execute_task(Params_Craw)