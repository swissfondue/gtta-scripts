# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Network_BGP(Task):
    """
    Searching records in BGP
    """
    target = ''

    def _add_valid_result(self, text):
        """
        Filter by '.' (not AS and not IPv6)
        """
        if '.' in text:
            self._write_result(text)

    def _search_by_keyword(self, raw):
        """
        Search by keyword
        """
        div = raw.find('div', attrs={'id': 'search'})

        for tag in div.findAll('a'):
            self._add_valid_result(tag.text)

    def _search_by_ip(self, raw):
        """
        Search by ip
        """
        div = raw.find('div', attrs={'id': 'ipinfo'})

        for tag in div.findAll('td', attrs={'class': 'nowrap'}):
            self._add_valid_result(tag.find('a').text)

    def _search_by_domain(self, raw):
        """
        Search by domain
        """
        div = raw.find('div', attrs={'id': 'dns'})

        for dnshead in div.findAll('div', attrs={'class': 'dnshead'}):
            if dnshead.text == 'A Records':
                dnsdata = dnshead.nextSibling.nextSibling
                self._add_valid_result(dnsdata.find('a').text)

    def main(self, *args):
        """
        Main function
        """
        soup = BeautifulSoup(
            requests.get(
                'http://bgp.he.net/search',
                params={'search[search]': self.target, 'commit': 'Search'},
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content
        )

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