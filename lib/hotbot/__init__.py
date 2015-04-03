# -*- coding: utf-8 -*-
import re
import requests
from BeautifulSoup import BeautifulSoup


class HotbotParser(object):
    """
    Class for parsing of results of search
    """
    HOST = 'http://www.hotbot.com'
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
        tags = soup.findAll('li', attrs={'class': 'result'})
        for tag in tags:
            self.results.update(
                [filter(lambda x: x[0] == 'href', tag.find('a').attrs)[0][1]])

    def _extract_keyvol(self, soup):
        """
        Extract keyvol by regexp from js
        :param soup:
        :return:
        """
        js = soup.find('script').text
        return re.findall(r'[a-f0-9]{20}', js)[0]

    def process(self):
        """
        Get results by target from source
        :return:
        """
        s = requests.Session()
        soup = BeautifulSoup(s.get(self.HOST, headers=self.headers).content)
        keyvol = self._extract_keyvol(soup.find('div', attrs={'class': 'hpSearchHolder'}))
        params = {
            'q': self.target,
            'keyvol': keyvol}

        req = s.get(
            self.HOST + '/search/web',
            headers=self.headers,
            params=params)
        soup = BeautifulSoup(req.content)
        self._collect_results_from_soup(soup)

        pn = 1
        while True:
            pn += 1
            params['keyvol'] = self._extract_keyvol(soup.find('header'))
            params['pn'] = '%s' % pn

            req = s.get(
                self.HOST + '/search/web',
                headers=self.headers,
                params=params)
            soup = BeautifulSoup(req.content)

            if soup.find('a', attrs={'class': 'noResults'}):
                break

            self._collect_results_from_soup(soup)

        return self.results