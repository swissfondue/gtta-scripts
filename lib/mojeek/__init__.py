# -*- coding: utf-8 -*-
import requests
from time import sleep
from BeautifulSoup import BeautifulSoup


class Mojeek(object):
    """
    Class for parsing of results of search
    """
    HOST = 'https://www.mojeek.com'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6,de;q=0.4,fr;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
    }
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

        req = s.get(self.HOST + '/search', headers=self.HEADERS, params=params)
        soup = BeautifulSoup(req.content)
        self._collect_results_from_soup(soup)

        pagination_links = soup.find('div', attrs={'class': 'pagination'})
        pagination_hrefs = pagination_links.findAll('a') if pagination_links else []
        next_link = filter(lambda x: x.text == 'Next', pagination_hrefs)

        while next_link:
            next_url = next_link[0].get('href')
            req = s.get(self.HOST + next_url, headers=self.HEADERS)

            if req.status_code != 200:
                sleep(5)
                continue

            soup = BeautifulSoup(req.content)

            pagination_links = soup.find('div', attrs={'class': 'pagination'})
            pagination_hrefs = pagination_links.findAll('a') if pagination_links else []

            if not filter(lambda x: x.text == 'Prev', pagination_hrefs):
                break

            self._collect_results_from_soup(soup)
            next_link = filter(lambda x: x.text == 'Next', pagination_hrefs)

            sleep(5)

        return self.results
