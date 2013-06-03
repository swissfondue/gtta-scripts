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

    def collect_unique_urls_filter_docs(self, url):
        """
        Using as callback function for crawler, which collect unique urls and outputting documents link
        """
        if url not in self.urls_set:
            if (url[-4:].lower() in self.DOC_TYPES) or (url[-5:].lower() in self.DOC_TYPES):
                self._write_result(url)

            self.urls_set.add(url)
            self._check_stop()

    def main(self):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.nonhtml_callback = self.collect_unique_urls_filter_docs

        if not self.proto:
            self.proto = 'http'

        if self.host:
            target = self.proto + '://' + self.host + '/'
        else:
            target = self.proto + '://' + self.ip + '/'

        link_crawler.process(target)  # Starting recursive process of link crawling on target

        self._check_stop()

        if not self.produced_output:
            self._write_result('No documents found.')

execute_task(Doc_Craw)
