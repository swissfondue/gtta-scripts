# -*- coding: utf-8 -*-
import requests
from socket import gethostbyname
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Domain_BGP(Task):
    """
    Search records in BGP
    """

    def main(self, *args):
        """
        Main function
        """
        results = []

        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except:
                return

        soup = BeautifulSoup(
            requests.get(
                'http://bgp.he.net/ip/%s' % self.ip,
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content)

        div = soup.find('div', attrs={'id': 'dns'})

        if not div:
            return

        for tag in div.findAll('a'):
            result = tag.text

            if result not in results:
                results.append(result)
                self._write_result(result)

    def test(self):
        """
        Test function
        """
        self.host = "clariant"
        self.main()
        self.ip = "83.150.1.145"
        self.main()
        self.host = "clariant.com"
        self.main()

execute_task(IG_Domain_BGP)
