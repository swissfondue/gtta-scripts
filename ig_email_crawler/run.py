# -*- coding: utf-8 -*-
from emailgrabber import parse_soup
from BeautifulSoup import BeautifulSoup
from core.crawler import LinkCrawler
from core import Task, execute_task


class IG_Email_Crawler(Task):
    """
    Search emails from page by url, using crawler.py
    """
    emails = []

    def collect_unique_emails(self, raw):
        """
        Callback function for crawler
        """
        url, content = raw['url'], raw['content']
        soup = BeautifulSoup(content)
        for email in parse_soup(soup):
            email = email.lower()
            if email not in self.emails:
                self._write_result(email)
                self.emails.append(email)

    def main(self, *args):
        """
        Main function
        """
        link_crawler = LinkCrawler()
        link_crawler.stop_callback = self._check_stop
        link_crawler.link_content_callback = self.collect_unique_emails

        if not self.proto:
            self.proto = 'http'

        link_crawler.process(self.proto + '://' + self.host + '/')

    def test(self):
        """
        Test function
        """
        self.proto = "http"
        self.host = "www.clariant.com"
        self.main()

execute_task(IG_Email_Crawler)
