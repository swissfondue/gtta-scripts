# -*- coding: utf-8 -*-
import re
import requests
from BeautifulSoup import BeautifulSoup
from core import Task


class CommonIGEmailTask(Task):
    """
    Common abstract class for ig_email parsers
    """
    results = set()
    parser = None
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    TEST_TIMEOUT = 2 * 60

    def _wrapped_target(self):
        """
        Wrapping target
        """
        return "\"@%s\"" % self.target

    def main(self, *args):
        """
        Main function
        """
        requests.packages.urllib3.disable_warnings()

        if not self.parser:
            self._write_result("Parser not found.")
            return

        if self.ip:
            return

        for url in self.parser(self._wrapped_target()).process(*args):
            try:
                req = requests.get(url, headers=self.HEADERS, verify=False)

                if "text/html" not in req.headers["content-type"]:
                    continue
                    
                soup = BeautifulSoup(req.content)

                for email in parse_soup(soup):
                    if email not in self.results:
                        self._write_result(email)
                        self.results.add(email)

            except Exception as e:
                continue


class CommonIGEmailParser(object):
    """
    Abstract class for parsing of results of search
    """
    HOST = ""
    req_source = requests.Session()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8,ru;q=0.6,de;q=0.4,fr;q=0.2",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"
    }
    results = set()

    def __init__(self, target):
        """
        Init function
        :param target:
        :return:
        """
        requests.packages.urllib3.disable_warnings()
        self.target = target

    def _get_soup(self, path="", use_post=False, **kwargs):
        """
        Request and souping
        :param path:
        :param use_post:
        :param kwargs:
        :return:
        """
        req_method = self.req_source.get

        if use_post:
            req_method = self.req_source.post

        req = req_method(
            "%s%s" % (self.HOST, path),
            headers=self.headers,
            verify=False,
            **kwargs
        )

        return BeautifulSoup(req.content)

    def _extract_next_link(self, soup):
        """
        Exctract some tag containing link to next page
        :param soup:
        :return:
        """
        return

    def _collect_results_from_soup(self, soup):
        """
        Collect search results from soup
        :param soup:
        :return:
        """
        pass

    def process(self, *args):
        """
        Get results by target from "self.HOST"
        :return:
        """
        pass


def parse_soup(soup):
    """
    Method return collected from soup emails
    :param soup:
    :return:
    """
    emails = set()
    pattern = re.compile(r"(\w+[\w\.-]*@(?:(?:\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(?:(?:[a-zA-Z0-9\-]+\.)+)(?:[a-zA-Z]{2,6})))")

    # looking at links
    for a in soup.findAll("a"):
        href = a.get("href")
        if not href or "mailto:" not in href:
            continue

        emails.update(pattern.findall(href))

    # looking at text
    for text in filter(lambda x: "@" in x, soup.findAll(text=True)):
        emails.update(pattern.findall(text))

    # do lowercase
    emails = [e.lower() for e in emails]

    # exclude trash
    emails = filter(lambda x: x[x.rindex(".") + 1:] not in ["gif", "jpg", "jpeg", "png"], emails)

    return emails
