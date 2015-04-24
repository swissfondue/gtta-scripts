# -*- coding: utf-8 -*-
from time import sleep
from emailgrabber import CommonIGEmailParser


class GoogleParser(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'https://www.google.com'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('h3', attrs={'class': 'r'})
        for tag in tags:
            url_raw = tag.a.get('href')
            if not '/url?' in url_raw:
                continue
            lsplit = url_raw.split('q=')[1]
            rsplit = lsplit.split('&')[0]
            self.results.add(rsplit)

    def process(self, *args):
        """
        Get results by target from source
        :return:
        """

        path = '/search'

        params = {
            'q': self.target,
            'num': '20',
            'filter': 0}
        soup = self._get_soup(path=path, params=params)

        self._collect_results_from_soup(soup)

        start = 0

        while start < 1001:
            sleep(3)

            start += 20
            params['start'] = str(start)
            soup = self._get_soup(path=path, params=params)

            self._collect_results_from_soup(soup)

        return self.results