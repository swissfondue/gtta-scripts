# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class OmgiliParser(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'http://omgili.com'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('article')
        for tag in tags:
            self.results.add(tag.a.get('href'))

    def process(self):
        """
        Get results by target from source
        :return:
        """
        path = '/search?siteType=&q=%s' % self.target

        soup = self._get_soup(path=path)
        self._collect_results_from_soup(soup)

        return self.results