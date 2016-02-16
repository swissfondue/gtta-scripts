# -*- coding: utf-8 -*-

import requests
from time import sleep
from emailgrabber import CommonIGEmailParser


class Mojeek(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = "https://www.mojeek.com"

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll("a", attrs={"class": "ob"})
        for tag in tags:
            self.results.add(tag.get("href"))

    def process(self):
        """
        Get results by target from source
        :return:
        """
        params = {"q": self.target}
        path="/search"
        soup = self._get_soup(path=path, params=params)
        self._collect_results_from_soup(soup)

        pagination_links = soup.find("div", attrs={"class": "pagination"})
        pagination_hrefs = pagination_links.findAll("a") if pagination_links else []
        next_link = filter(lambda x: x.text == "Next", pagination_hrefs)

        while next_link:
            next_url = next_link[0].get("href")
            soup = self._get_soup(path=next_url)

            pagination_links = soup.find("div", attrs={"class": "pagination"})
            pagination_hrefs = pagination_links.findAll("a") if pagination_links else []

            if not filter(lambda x: x.text == "Prev", pagination_hrefs):
                break

            self._collect_results_from_soup(soup)
            next_link = filter(lambda x: x.text == "Next", pagination_hrefs)

            sleep(5)

        return self.results
