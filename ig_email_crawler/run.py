# -*- coding: utf-8 -*-
import re
from BeautifulSoup import BeautifulSoup
from core.crawler import LinkCrawler
from core import Task, execute_task


class IG_Email_Craw(Task):
    """
    Search emails from page by url, using crawler.py
    """
    emails = set()

    def add_emails(self, emails):
        """
        Add collected emails
        """
        for email in emails:
            if email not in self.emails:
                self._write_result(email)
                self.emails.add(email)

    def collect_unique_emails(self, raw):
        """
        Callback function for crawler
        """
        url, content = raw['url'], raw['content']
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            for attr in a.attrs:
                if attr[0] == 'href':
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+', attr[1])
                    if emails:
                        self.add_emails(emails)
                    break
        for text in filter(lambda x: '@' in x, soup.findAll(text=True)):
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
            self.add_emails(emails)

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

execute_task(IG_Email_Craw)
