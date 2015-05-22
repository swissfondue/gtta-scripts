# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup


class Exalead(object):
    """
    Class for parsing of results of search
    """
    HOST = 'http://www.exalead.com'
    headers = {'User-Agent': 'Mozilla/5.0'}
    results = set()

    def __init__(self, target):
        """
        Init function
        :param target:
        :return:
        """
        self.target = target

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('a', attrs={'class': 'title'})

        for tag in tags:
            self.results.update([filter(lambda x: x[0] == 'href', tag.attrs)[0][1]])

    def process(self):
        """
        Get results by target from source
        :return:
        """
        s = requests.Session()

        req = s.get(self.HOST + '/search/web/results/', headers=self.headers, params={'q': self.target})
        soup = BeautifulSoup(req.content)
        self._collect_results_from_soup(soup)

        tag_to_next = soup.find('a', attrs={'title': 'Go to the next page'})

        while tag_to_next:
            next_url = filter(lambda x: x[0] == 'href', tag_to_next.attrs)[0][1]

            req = s.get(self.HOST + next_url, headers=self.headers)
            soup = BeautifulSoup(req.content)
            self._collect_results_from_soup(soup)

            tag_to_next = soup.find('a', attrs={'title': 'Go to the next page'})

        return self.results
