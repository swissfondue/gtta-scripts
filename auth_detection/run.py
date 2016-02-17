# -*- coding: utf-8 -*-

import re
from core.crawler import LinkCrawler
from core import Task, execute_task


class Auth_Craw(Task):
    """
    Searching auth link and form from page by url, using crawler.py
    """
    urls_set = set()

    FORM_PATTERN = "(?i)<form([^>]+)>(.+?)</form>"
    AUTH_WORDS = ("auth", "login", "access", "admin", "signin", "password")

    def collect_unique_urls(self, url):
        """
        Using as callback function for crawler
        """
        self.urls_set.add(url)

    def collect_401_url(self, url):
        """
        Searching 401 http status links
        """
        if url[:3] == "401" and url not in self.urls_set:
            self.urls_set.add(url)

        self._check_stop()

    def collect_login_urls(self, url):
        """ Searching login keywords in links """
        if url not in self.urls_set:
            if any(word in url.lower() for word in self.AUTH_WORDS):
                self.urls_set.add(url)

        self._check_stop()

    def collect_urls_login_forms(self, page):
        """ If we have on page form and form has any auth KEYWORD, then outputting that page url"""
        for item in re.finditer(self.FORM_PATTERN, page["content"], re.S):
            self._check_stop()

            if any(word in item.group(0).lower() for word in self.AUTH_WORDS):
                self.urls_set.add(page["url"])
                return

    def main(self, *args):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.link_callback = self.collect_login_urls
        link_crawler.link_content_callback = self.collect_urls_login_forms
        link_crawler.error_callback = self.collect_401_url

        if not self.proto:
            self.proto = "http"

        if not self.port:
            self.port = "80"

        target = self.proto + "://" + self.target + ":" + self.port + "/"

        link_crawler.process(target)  # Starting recursive process of link crawling on target
        self._check_stop()

        if self.urls_set:
            for url in self.urls_set:
                self._write_result(url)
        else:
            self._write_result("Login links not found.")

    def test(self):
        """
        Test function
        """
        self.port = "80"
        self.proto = "http"
        self.target = "gtta.demo.stellarbit.com"
        self.main()


execute_task(Auth_Craw)
