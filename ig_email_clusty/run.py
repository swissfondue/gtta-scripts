# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from clusty import ClustyParser
from emailgrabber import parse_soup


class IG_Email_Clusty(Task):
    """
    Search emails in pages from Clusty
    """
    results = set()

    def main(self, *args):
        """
        Main function
        """
        if self.ip:
            return

        urls = ClustyParser('"@%s"' % self.target).process()

        for url in urls:
            try:
                req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(req.content)
            except:
                continue
            self.results.update(parse_soup(soup))

        map(lambda x: self._write_result(x), self.results)

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Clusty)
