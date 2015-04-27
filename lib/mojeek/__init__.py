# -*- coding: utf-8 -*-
import requests
from time import sleep
from BeautifulSoup import BeautifulSoup


class MojeekParser(object):
    """
    Class for parsing of results of search
    """
    HOST = 'https://www.mojeek.com'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'}
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
        tags = soup.findAll('a', attrs={'class': 'ob'})
        for tag in tags:
            self.results.add(tag.get('href'))

    def process(self):
        """
        Get results by target from source
        :return:
        """
        s = requests.Session()
        params = {'q': self.target}

        req = s.get(self.HOST + '/search', headers=self.headers, params=params)
        soup = BeautifulSoup(req.content)
        self._collect_results_from_soup(soup)

        pagination_links = soup.find('div', attrs={'class': 'pagination'}).findAll('a')
        next_link = filter(lambda x: x.text == 'Next', pagination_links)

        while next_link:
            next_url = next_link[0].get('href')
            req = s.get(self.HOST + next_url, headers=self.headers)

            if req.status_code != 200:
                sleep(1)
                continue

            soup = BeautifulSoup(req.content)
            pagination_links = soup.find('div', attrs={'class': 'pagination'}).findAll('a')

            if not filter(lambda x: x.text == 'Prev', pagination_links):
                break

            self._collect_results_from_soup(soup)
            next_link = filter(lambda x: x.text == 'Next', pagination_links)

        return self.results
