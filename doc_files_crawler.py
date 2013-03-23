# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from crawler import LinkCrawler
from gtta import Task, execute_task


class Doc_Craw(Task):
    """
    GET document files from page by url, using crawler.py
    """

    urls_set = set()

    DOC_TYPES = ('.xls', '.xlsx', '.doc', '.docx', '.pdf', '.odt', '.txt', '.rtf')

    def collect_unique_urls(self, url):
        """
        Using as callback function for crawler
        """
        self.urls_set.add(url)

    def main(self):
        """
        Main function
        """
        link_crawler = LinkCrawler()

        link_crawler.stop_callback = self._check_stop
        link_crawler.redirect_callback = lambda x: False

        link_crawler.ext_link_callback = self.collect_unique_urls
        link_crawler.nonhtml_callback = self.collect_unique_urls
        link_crawler.error_callback = self.collect_unique_urls

        if not self.proto:
            self.proto = 'http'

        if self.host:
            target = self.proto + '://' + self.host + '/'

        else:
            target = self.proto + '://' + self.ip + '/'

        link_crawler.process(target)

        self._check_stop()

        for curr_link in self.urls_set:
            if (curr_link[-4:] in self.DOC_TYPES) or (curr_link[-5:] in self.DOC_TYPES):
                self._write_result(curr_link)

        if not self.produced_output:
            self._write_result('No link to any documents found')



execute_task(Doc_Craw)
