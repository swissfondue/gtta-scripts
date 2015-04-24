# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from exalead import ExaleadParser
from emailgrabber import parse_soup


class IG_Email_Exalead(Task):
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

        urls = ExaleadParser('"@%s"' % self.target).process()

        while urls:
            try:
                req = requests.get(urls.pop(), headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(req.content)
            except:
                continue
            self.results.update(parse_soup(soup))

        self._write_result('\n'.join(self.results))

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Exalead)
