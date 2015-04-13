# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class BingParser(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'http://www.bing.com'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('div', attrs={'class': 'b_title'})
        for tag in tags:
            self.results.add(tag.a.get('href'))

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        next_link = soup.find('a', attrs={'class': 'sb_pagN'})
        return next_link

    def process(self):
        """
        Get results by target from source
        :return:
        """
        path = '/search'
        params = {
            'q': self.target,
            'go': 'Отправить',
            'qs': 'bs',
            'form': 'QBRE'
        }

        soup = self._get_soup(path=path, params=params)
        self._collect_results_from_soup(soup)

        next_link = self._extract_next_link(soup)

        while next_link:
            next_url = next_link.get('href')

            soup = self._get_soup(path=next_url)
            self._collect_results_from_soup(soup)

            next_link = self._extract_next_link(soup)

        return self.results