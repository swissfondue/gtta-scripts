# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Network_BGP(Task):
    """
    Searching records in BGP
    """
    target = ''

    def _is_valid(self, text):
        """
        Filter by '.' (not AS and not IPv6)
        """
        return '.' in text

    def _search_by_keyword(self, raw):
        """
        Search by keyword
        """
        div = raw.find('div', attrs={'id': 'search'})
        results = []

        for tag in div.findAll('a'):
            result = tag.text

            if self._is_valid(result) and result not in results:
                results.append(result)
                self._write_result(result)

    def _search_by_ip(self, raw):
        """
        Search by ip
        """
        div = raw.find('div', attrs={'id': 'ipinfo'})
        results = []

        for tag in div.findAll('td', attrs={'class': 'nowrap'}):
            result = tag.find('a').text

            if self._is_valid(result) and result not in results:
                results.append(result)
                self._write_result(result)

    def _search_by_domain(self, raw):
        """
        Search by domain
        """
        div = raw.find('div', attrs={'id': 'dns'})
        results = []

        for dnshead in div.findAll('div', attrs={'class': 'dnshead'}):
            if dnshead.text == 'A Records':
                dnsdata = dnshead.nextSibling.nextSibling
                result = dnsdata.find('a').text

                if self._is_valid(result) and result not in results:
                    results.append(result)
                    self._write_result(result)

    def main(self, *args):
        """
        Main function
        """
        soup = BeautifulSoup(
            requests.get(
                'http://bgp.he.net/search',
                params={'search[search]': self.target, 'commit': 'Search'},
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content)

        first_tabmenuli_id = soup.find('li', attrs={'class': 'tabmenuli'}).attrMap['id']

        if first_tabmenuli_id == 'tab_search':
            self._search_by_keyword(soup)
        elif first_tabmenuli_id == 'tab_ipinfo':
            self._search_by_ip(soup)
        elif first_tabmenuli_id == 'tab_dns':
            self._search_by_domain(soup)

        self._check_stop()

    def test(self):
        """
        Test function
        """
        self.target = "clariant"
        self.main()
        self.target = "83.150.1.145"
        self.main()
        self.target = "clariant.com"
        self.main()

execute_task(IG_Network_BGP)