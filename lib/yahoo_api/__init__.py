# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1
from emailgrabber import CommonIGEmailParser


class YahooAPI(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = 'https://yboss.yahooapis.com/ysearch/web'

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll('clickurl')
        for tag in tags:
            self.results.add(tag.text)

    def process(self, *args):
        """
        Get results by target from source
        :return:
        """
        if not args or len(args) < 2 or not args[0] or not args[0][0] or not args[1] or not args[1][0]:
            raise ValueError("Yahoo API key and client secret are required.")

        oauth = OAuth1(args[0][0], client_secret=args[1][0])
        params = {'format': 'xml', 'count': '50'}
        path = '?q=%s' % self.target.replace(' ', '%20').replace(':', '%3A')
        soup = self._get_soup(path=path, params=params, auth=oauth)
        self._collect_results_from_soup(soup)

        skip = 0

        while True:
            skip += 50
            params['start'] = skip

            soup = self._get_soup(params=params, auth=oauth)
            self._collect_results_from_soup(soup)

            if not soup.find('clickurl'):
                break

        return self.results