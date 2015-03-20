# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from core.error import InvalidTarget

__author__ = 'user'


class IG_Network_Arin(Task):
    """
    Searching networks in Arin
    """
    target = ''

    def _extract_networks_from_customer(self, customer, results):
        """
        Extracting networks from customer
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
            text = '%s - %s' % (tag.attrMap['startaddress'], tag.attrMap['endaddress'])
            if not text in results:
                results.append(text)
                self._write_result(text)

    def main(self, *args):
        """
        Main function
        """
        if not self.target:
            raise InvalidTarget('No target specified.')

        self._check_stop()

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
                    self._extract_networks_from_customer(next_str.text, results)
                    try:
                        next_str = next_str.parent.parent.nextSibling.nextSibling.findAll('a')[0]
                    except:
                        break
            elif th.text == 'Networks':
                next_str = th.parent.nextSibling.nextSibling.findAll('td')[1]
                while True:
                    text = next_str.text
                    if not text in results:
                        results.append(text)
                        self._write_result(text)
                    try:
                        next_str = next_str.parent.nextSibling.nextSibling.findAll('td')[1]
                    except:
                        break

        self._check_stop()

        if len(results) == 0:
            self._write_result('No Arin records.')

    def test(self):
        """
        Test function
        """
        self.target = "google"
        self.main()

execute_task(IG_Network_Arin)

