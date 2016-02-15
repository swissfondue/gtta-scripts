# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class Omgili(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = "http://omgili.com"

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll("article")

        for tag in tags:
            try:
                yield tag.a.get("href")
            except:
                continue

    def process(self):
        """
        Get results by target from source
        :return:
        """
        soup = self._get_soup(path="/search", params={
            "siteType": "",
            "q": self.target
        })

        for result in self._collect_results_from_soup(soup):
            yield result
