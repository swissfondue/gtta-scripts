# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class DuckDuckGo(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = "https://duckduckgo.com/html/"

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll("a", attrs={"class": "large"})
        
        for tag in tags:
            yield tag.get("href")

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        return soup.find("input", attrs={"value": "Next"})

    def process(self):
        """
        Get results by target from source
        :return:
        """
        data = {
            "q": self.target,
            "kl": "us-en",
            "b": ""
        }

        soup = self._get_soup(data=data, use_post=True)
        self._collect_results_from_soup(soup)

        next_link = self._extract_next_link(soup)
        del data["b"]

        while next_link:
            for tag in next_link.parent.findAll("input", attrs={"type": "hidden"}):
                data[tag.get("name")] = tag.get("value")

            soup = self._get_soup(data=data, use_post=True)

            for result in self._collect_results_from_soup(soup):
                yield result

            next_link = self._extract_next_link(soup)
