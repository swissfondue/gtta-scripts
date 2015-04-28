# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from mojeek import MojeekParser
from emailgrabber import parse_soup


class IG_Email_Mojeek(Task):
    """
    Search emails in pages from source
    """
    results = set()
    TEST_TIMEOUT = 60 * 60

    def main(self, *args):
        """
        Main function
        """
        if self.ip:
            return

        urls = MojeekParser('"@%s"' % self.target).process()

        while urls:
            try:
                req = requests.get(urls.pop(), headers={'User-Agent': 'Mozilla/5.0'})

                if not 'text/html' in req.headers['content-type']:
                    continue

                soup = BeautifulSoup(req.content)

            except:
                continue

            for email in parse_soup(soup):
                if email not in self.results:
                    self._write_result(email)
                    self.results.add(email)

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Mojeek)
