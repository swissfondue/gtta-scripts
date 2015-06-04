# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class Yandex(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'https://www.yandex.com'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('h2', attrs={'class': 'serp-item__title'})
        for tag in tags:
            try:
                self.results.add(tag.a.get('href'))
            except:
                continue

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        next_span = filter(lambda x: x.text == 'Next', soup.findAll('span', attrs={'class': 'button__text'}))
        next_link = next_span[0].parent if next_span else None
        return next_link

    def process(self):
        """
        Get results by target from source
        :return:
        """
        path = '/yandsearch?lr=87&text=%s' % self.target

        soup = self._get_soup(path=path)
        self._collect_results_from_soup(soup)

        next_link = self._extract_next_link(soup)

        while next_link:
            next_url = next_link.get('href')

            soup = self._get_soup(path=next_url)
            self._collect_results_from_soup(soup)

            next_link = self._extract_next_link(soup)

        return self.results