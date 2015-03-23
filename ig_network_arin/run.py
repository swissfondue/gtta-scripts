# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Network_Arin(Task):
    """
    Searching networks in Arin
    """
    target = ''

    def _extract_networks_from_customer(self, customer):
        """
        Extract networks from customer
        """
        soup = BeautifulSoup(
            requests.get(
                'http://whois.arin.net/rest/customer/%s' % customer,
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content)

        for tag in soup.findAll('netref'):
            tag.attrMap = {}

            for attr in tag.attrs:
                tag.attrMap[attr[0]] = attr[1]

            text = '%s-%s' % (tag.attrMap['startaddress'], tag.attrMap['endaddress'])

            yield text

    def main(self, *args):
        """
        Main function
        """
        results = []

        soup = BeautifulSoup(
            requests.post(
                'http://whois.arin.net/ui/query.do',
                headers={'User-Agent': 'Mozilla/5.0'},
                params={
                    'xslt': 'http://whois.arin.net/ui/arin.xsl',
                    'flushCache': 'false',
                    'queryinput': self.target,
                    'whoisSubmitButton': ''
                }
            ).content)

        for th in soup.findAll('th', attrs={'colspan': '2'}):
            if th.text == 'Customers':
                next_str = th.parent.nextSibling.nextSibling.findAll('a')[0]

                while True:
                    for result in self._extract_networks_from_customer(next_str.text):
                        if result not in results:
                            results.append(result)
                            self._write_result(result)

                    try:
                        next_str = next_str.parent.parent.nextSibling.nextSibling.findAll('a')[0]
                    except:
                        break

            elif th.text == 'Networks':
                next_str = th.parent.nextSibling.nextSibling.findAll('td')[1]

                while True:
                    text = next_str.text
                    result = text.replace(" ", "")

                    if result not in results:
                        results.append(result)
                        self._write_result(result)

                    try:
                        next_str = next_str.parent.nextSibling.nextSibling.findAll('td')[1]
                    except:
                        break

    def test(self):
        """
        Test function
        """
        self.target = "google"
        self.main()

execute_task(IG_Network_Arin)
