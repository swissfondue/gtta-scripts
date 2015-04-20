# -*- coding: utf-8 -*-
import requests
import urlparse
from BeautifulSoup import BeautifulSoup


class DogpileParser(object):
    """
    Class for parsing of results of searching in Dogpile.com
    """
    HOST = 'http://www.dogpile.com'
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
        web_results = soup.find('div', attrs={'id': 'webResults'})

        if web_results:
            links = web_results.findAll('a', attrs={'class': 'resultDisplayUrl'})

            for result in links:
                href = result.attrMap['href']
                cut_left = href.split('ru=')[1]
                cut_right = cut_left.split('&')[0]

                url = urlparse.parse_qs("x=%s" % cut_right)
                url = url["x"][0]

                if not url in self.results:
                    self.results.add(url)

    def process(self):
        """
        Get results by target from DogPile
        :return:
        """
        s = requests.Session()
        first_visit = s.get(self.HOST, headers=self.headers)
        soup = BeautifulSoup(first_visit.content)
        params = {
            'fcoid': soup.find('input', attrs={'name': 'fcoid'}).attrMap['value'],
            'fcop': 'topnav',
            'fpid': soup.find('input', attrs={'name': 'fpid'}).attrMap['value'],
            'q': self.target,
            'ql': ''
        }

        req = s.get(self.HOST + '/search/web', headers=self.headers, params=params)
        soup = BeautifulSoup(req.content)
        self._collect_results_from_soup(soup)

        link_to_next_page = soup\
            .find('div', attrs={'id': 'resultsPaginationBottom'})\
            .find('li', attrs={'class': 'paginationNext'})

        while link_to_next_page:
            tag = link_to_next_page.find('a')
            next_url = filter(lambda x: x[0] == 'href', tag.attrs)[0][1]

            req = s.get(self.HOST + next_url, headers=self.headers)
            soup = BeautifulSoup(req.content)
            self._collect_results_from_soup(soup)

            link_to_next_page = soup\
                .find('div', attrs={'id': 'resultsPaginationBottom'})\
                .find('li', attrs={'class': 'paginationNext'})

        return self.results
