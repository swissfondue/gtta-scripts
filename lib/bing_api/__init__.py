# -*- coding: utf-8 -*-
import base64
from emailgrabber import CommonIGEmailParser


class BingAPIParser(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'https://api.datamarket.azure.com/Bing/SearchWeb/Web'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('d:url')
        for tag in tags:
            self.results.add(tag.text)

    def process(self, account_key):
        """
        Get results by target from source
        :return:
        """
        params = {'Query': self.target}

        keys = '%s:%s' % (account_key[0], account_key[0])
        encoded = base64.b64encode(keys)
        self.headers.update({'Authorization': 'Basic %s' % encoded})

        soup = self._get_soup(params=params)
        self._collect_results_from_soup(soup)

        skip = 0

        while True:
            skip += 50
            params['$skip'] = skip

            soup = self._get_soup(params=params)
            self._collect_results_from_soup(soup)

            if not soup.find('d:url'):
                break

        return self.results