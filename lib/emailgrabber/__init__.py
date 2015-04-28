# -*- coding: utf-8 -*-
import re
import requests
from BeautifulSoup import BeautifulSoup
from core import Task


class CommonIGEmailTask(Task):
    """
    Common abstract class for ig_email parsers
    """
    results = set()
    parser = None
    headers = {'User-Agent': 'Mozilla/5.0'}
    TEST_TIMEOUT = 60 * 60

    def _wrapped_target(self):
        """
        Wrapping target
        """
        return '"@%s"' % self.target

    def main(self, *args):
        """
        Main function
        """
        if not self.parser:
            self._write_result('It requires a "self.parser".')
            return

        if self.ip:
            return

        urls = self.parser(self._wrapped_target()).process(*args)

        while urls:
            try:
                req = requests.get(urls.pop(), headers=self.headers)
                if not 'text/html' in req.headers['content-type']:
                    continue
                soup = BeautifulSoup(req.content)
            except Exception as e:
                continue
            self.results.update(parse_soup(soup))

        self._write_result('\n'.join(self.results))


class CommonIGEmailParser(object):
    """
    Abstract class for parsing of results of search
    """
    HOST = ''
    req_source = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = set()

    def __init__(self, target):
        """
        Init function
        :param target:
        :return:
        """
        self.target = target

    def _get_soup(self, path='', params={}, data={}, use_post=False):
        """
        Request and souping
        :param path:
        :param params:
        :param data:
        :param use_post:
        :return:
        """
        req_method = self.req_source.get
        if use_post:
            req_method = self.req_source.post
        req = req_method(
            '%s%s' % (self.HOST, path),
            headers=self.headers,
            params=params,
            data=data)
        return BeautifulSoup(req.content)

    def _extract_next_link(self, soup):
        """
        Exctract some tag containing link to next page
        :param soup:
        :return:
        """
        return

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        pass

    def process(self, *args):
        """
        Get results by target from "self.HOST"
        :return:
        """
        pass


def parse_soup(soup):
    """
    Method return collected from soup emails
    :param soup:
    :return:
    """
    emails = set()
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+')

    # looking at links
    for a in soup.findAll('a'):
        try:
            href = filter(lambda x: x[0] == 'href', a.attrs)[0][1]
            emails.update(pattern.findall(href))
        except:
            continue

    # looking at text
    for text in filter(lambda x: '@' in x, soup.findAll(text=True)):
        emails.update(pattern.findall(text))

    return emails
