# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class Yandex(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = "https://www.yandex.com"

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll("span", attrs={"class": "serp-url__item"})

        for tag in tags:
            try:
                yield tag.a.get("href")
            except:
                continue

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        links = soup.findAll("a", attrs={"class": "link link_ajax_yes pager__item pager__item_kind_next i-bem"})
        next_a = filter(lambda x: x.text == "next", links)
        next_link = next_a[0].get("href") if next_a else None

        return next_link

    def process(self):
        """
        Get results by target from source
        :return:
        """
        params = {
            "lr": "87",
            "text": self.target
        }

        soup = self._get_soup(path="/yandsearch", params=params)

        for result in self._collect_results_from_soup(soup):
            yield result

        next_link = self._extract_next_link(soup)

        while next_link:
            soup = self._get_soup(path=next_link, params=params)

            for result in self._collect_results_from_soup(soup):
                yield result

            next_link = self._extract_next_link(soup)
