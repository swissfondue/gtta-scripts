# -*- coding: utf-8 -*-
from time import sleep
from emailgrabber import CommonIGEmailParser


class Google(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'https://www.google.com'
    SEARCH_LIMIT = 1000
    SEARCH_OFFSET = 100

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('h3', attrs={'class': 'r'})

        for tag in tags:
            try:
                url_raw = tag.a.get('href')

                if not '/url?' in url_raw:
                    continue

                lsplit = url_raw.split('q=')[1]
                rsplit = lsplit.split('&')[0]

            except:
                continue

            self.results.add(rsplit)

    def process(self, *args):
        """
        Get results by target from source
        :return:
        """

        path = '/search'

        params = {
            'q': self.target,
            'num': str(self.SEARCH_OFFSET),
            'filter': 0
        }

        soup = self._get_soup(path=path, params=params)
        self._collect_results_from_soup(soup)

        start = 0

        while start <= self.SEARCH_LIMIT:
            sleep(3)
            start += self.SEARCH_OFFSET
            params['start'] = str(start)
            soup = self._get_soup(path=path, params=params)

            self._collect_results_from_soup(soup)

        return self.results
