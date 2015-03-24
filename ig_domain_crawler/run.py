# -*- coding: utf-8 -*-

from core.crawler import LinkCrawler
from core import Task, execute_task


class IG_Domain_Craw(Task):
    """
    Search domains from page by url, using crawler.py
    """
    domains = set()

    def collect_unique_urls(self, url):
        """
        Callback function for crawler
        """
        proto_domain = url.split('//')
        domain = proto_domain[1].split('/')[0]

        if domain not in self.domains:
            self._write_result(domain)
            self.domains.add(domain)

    def main(self, *args):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.ext_link_callback = self.collect_unique_urls

        if not self.proto:
            self.proto = 'http'

        link_crawler.process(self.proto + '://' + self.host + '/')

    def test(self):
        """
        Test function
        """
        self.proto = "http"
        self.host = "google.com"
        self.main()

execute_task(IG_Domain_Craw)
