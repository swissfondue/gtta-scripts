# -*- coding: utf-8 -*-
from emailgrabber import CommonIGEmailParser


class Lexxe(CommonIGEmailParser):
    """
    Class for parsing of results of search
    """
    HOST = "http://www.lexxe.com/ct"

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        tags = soup.findAll("span", attrs={"class": "resLink"})

        for tag in tags:
            yield tag.text

    def _extract_next_link(self, soup):
        """
        Exctract next link
        :param soup:
        :return:
        """
        next_link = None
        paginator = soup.find("ul", attrs={"id": "pageNav"})

        if paginator:
            current = filter(lambda x: not x.a, paginator.findAll("li"))[0]
            next_link = current.nextSibling

        return next_link

    def process(self):
        """
        Get results by target from source
        :return:
        """
        soup = self._get_soup(params={
            "sstring": self.target,
            "src": "hp"
        })

        self._collect_results_from_soup(soup)
        next_link = self._extract_next_link(soup)

        while next_link:
            try:
                next_url = next_link.a.get("href")
            except:
                break

            soup = self._get_soup(path=next_url)

            for result in self._collect_results_from_soup(soup):
                yield result

            next_link = self._extract_next_link(soup)
