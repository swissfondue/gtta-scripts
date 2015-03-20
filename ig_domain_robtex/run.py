# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from core.error import InvalidTarget

__author__ = 'user'


class IG_Domain_Robtex(Task):
    """
    Searching records in Robtex
    """
    target = ''

    def main(self, *args):
        """
        Main function
        """
        if not self.target:
            raise InvalidTarget('No target specified.')

        self._check_stop()
        results = []

        soup = BeautifulSoup(
            requests.get(
                'https://www.robtex.com/q/y?q=%s' % self.target,
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content)
        div = soup.find('div', attrs={'id': 'datawhois'})
        for tag in div.findAll('h2'):
            text = tag.find('a').text
            results.append(text)
            self._write_result(text)

        self._check_stop()

        if len(results) == 0:
            self._write_result('No Robtex records.')

    def test(self):
        """
        Test function
        """
        self.target = "clariant"
        self.main()

execute_task(IG_Domain_Robtex)
