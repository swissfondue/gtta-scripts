# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class Lixam(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'http://lixam.de/search-results.php'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('div', attrs={'class': 'searchresultsblocks'})
        for tag in tags:
            self.results.add(tag.a.get('href'))

    def process(self):
        """
        Get results by target from source
        :return:
        """
        params = {'suche': self.target}

        soup = self._get_soup(params=params)
        self._collect_results_from_soup(soup)

        return self.results