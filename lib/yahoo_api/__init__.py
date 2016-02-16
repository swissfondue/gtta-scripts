# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1
from emailgrabber import CommonIGEmailParser
from urllib import urlencode


class YahooAPI(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = "https://yboss.yahooapis.com/ysearch/web"

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        error = soup.find("yahoo:error")

        if error:
            description = error.find("yahoo:description")

            if description:
                raise RuntimeError(description.text)
            else:
                raise RuntimeError("Unknown Yahoo API error.")

        tags = soup.findAll("clickurl")

        for tag in tags:
            yield tag.text

    def process(self, *args):
        """
        Get results by target from source
        :return:
        """
        if not args or len(args) < 2 or not args[0] or not args[0][0] or not args[1] or not args[1][0]:
            raise ValueError("Yahoo API key and client secret are required.")

        oauth = OAuth1(args[0][0], client_secret=args[1][0])
        params = {"format": "xml", "count": "50", "q": self.target.replace(":", "%3A").replace(" ", "%20")}
        soup = self._get_soup(params=params, auth=oauth)
        self._collect_results_from_soup(soup)

        skip = 0

        while True:
            skip += 50
            params["start"] = skip
            soup = self._get_soup(params=params, auth=oauth)

            for result in self._collect_results_from_soup(soup):
                yield result

            if not soup.find("clickurl"):
                break
