# -*- coding: utf-8 -*-

from core.crawler import LinkCrawler
from core import Task, execute_task


class IG_Domain_Craw(Task):
    """
    Search domains from page by url, using crawler.py
    """
    urls_set = set()

    def collect_unique_urls(self, url):
        """
        Using as callback function for crawler
        """
        proto_domain = url.split('//')
        domain = proto_domain[1].split('/')[0]
        self.urls_set.add(domain)

    def main(self, *args):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.ext_link_callback = self.collect_unique_urls

        if not self.proto:
            self.proto = 'http'

        target = self.proto + '://' + self.host + '/'

        link_crawler.process(target)  # Starting recursive process of link crawling on target
        self._check_stop()

        for url in self.urls_set:
            self._write_result(url)

    def test(self):
        """
        Test function
        """
        self.proto = "http"
        self.host = "google.com"
        self.main()

execute_task(IG_Domain_Craw)
