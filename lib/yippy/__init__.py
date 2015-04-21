# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup


class YippyParser(object):
    """
    Class for parsing of results of search
    """
    HOST = 'http://new.yippy.com'
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
        result_container = soup.find('div', attrs={'id': 'results-list-container'})
        if result_container:
            divs = result_container.findAll('div', attrs={'class': 'document-header'})
            for div in divs:
                self.results.update(
                    [filter(lambda x: x[0] == 'href', div.find('a').attrs)[0][1]])

    def process(self):
        """
        Get results by target from Clusty
        :return:
        """
        s = requests.Session()

        params = {
            'tb': 'sitesearch-all',
            'v:project': 'clusty-new',
            'query': self.target}
        req = s.get(
            self.HOST + '/search',
            headers=self.headers,
            params=params)

        soup = BeautifulSoup(req.content)
        self._collect_results_from_soup(soup)

        tag_to_next = soup.find('a', attrs={'class': 'listnext'})
        while tag_to_next:

            next_url = filter(lambda x: x[0] == 'href', tag_to_next.attrs)[0][1]
            req = s.get(
                self.HOST + next_url,
                headers=self.headers)
            soup = BeautifulSoup(req.content)
            self._collect_results_from_soup(soup)

            tag_to_next = soup.find('a', attrs={'class': 'listnext'})

        return self.results