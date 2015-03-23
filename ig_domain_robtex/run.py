# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Domain_Robtex(Task):
    """
    Search records in Robtex
    """
    target = ''

    def main(self, *args):
        """
        Main function
        """
        results = []

        soup = BeautifulSoup(
            requests.get(
                'https://www.robtex.com/q/y?q=%s' % self.target,
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content
        )

        div = soup.find('div', attrs={'id': 'datawhois'})

        for tag in div.findAll('h2'):
            result = tag.find('a').text

            if result not in results:
                results.append(result)
                self._write_result(result)

    def test(self):
        """
        Test function
        """
        self.target = "clariant"
        self.main()

execute_task(IG_Domain_Robtex)
