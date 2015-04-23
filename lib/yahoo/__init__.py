# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser
import urlparse


class YahooParser(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'https://search.yahoo.com'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('h3', attrs={'class': 'title'})
        for tag in tags:
            if not tag.a:
                continue
            url = tag.a.get('href')
            try:
                left_split = url.split('/RU=')[1]
                right_split = left_split.split('/')[0]
                url = urlparse.parse_qs("x=%s" % right_split)["x"][0]
            except:
                pass
            self.results.add(url)

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        next_link = soup.find('a', attrs={'class': 'next'})
        return next_link

    def process(self):
        """
        Get results by target from source
        :return:
        """
        soup = self._get_soup(path='/search', params={'p': self.target})
        self._collect_results_from_soup(soup)

        next_link = self._extract_next_link(soup)

        while next_link:
            next_url = next_link.get('href').replace(self.HOST, '')

            soup = self._get_soup(path=next_url)
            self._collect_results_from_soup(soup)

            next_link = self._extract_next_link(soup)

        return self.results