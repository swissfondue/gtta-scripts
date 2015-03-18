# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from core.error import InvalidTarget


class IG_Network_BGP(Task):
    """
    Searching records in BGP
    """
    target = ''

    def _valid_res_add(self, text, results):
        """
        Filtering by '.' (not AS and not IPv6)
        """
        if '.' in text:
            self._write_result(text)
            results.append(text)

    def _search_by_keyword(self, raw, res):
        """
        Searching by keyword
        """
        div = raw.find('div', attrs={'id': 'search'})
        for tag in div.findAll('a'):
            self._valid_res_add(tag.text, res)

    def _search_by_ip(self, raw, res):
        """
        Searching by ip
        """
        div = raw.find('div', attrs={'id': 'ipinfo'})
        for tag in div.findAll('td', attrs={'class': 'nowrap'}):
            self._valid_res_add(tag.find('a').text, res)

    def _search_by_domain(self, raw, res):
        """
        Searching by domain
        """
        div = raw.find('div', attrs={'id': 'dns'})
        for dnshead in div.findAll('div', attrs={'class': 'dnshead'}):
            if dnshead.text == 'A Records':
                dnsdata = dnshead.nextSibling.nextSibling
                self._valid_res_add(dnsdata.find('a').text, res)

    def main(self, *args):
        """
        Main function
        """
        if not self.target:
            raise InvalidTarget('No target specified.')

        self._check_stop()
        self._write_result('target = "%s"' % self.target)
        results = []

        soup = BeautifulSoup(
            requests.get(
                'http://bgp.he.net/search',
                params={'search[search]': self.target, 'commit': 'Search'},
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content)
        first_tabmenuli_id = soup.find('li', attrs={'class': 'tabmenuli'}).attrMap['id']

        if first_tabmenuli_id == 'tab_search':
            self._search_by_keyword(soup, results)
        if first_tabmenuli_id == 'tab_ipinfo':
            self._search_by_ip(soup, results)
        if first_tabmenuli_id == 'tab_dns':
            self._search_by_domain(soup, results)

        self._check_stop()

        if len(results) == 0:
            self._write_result('No BGP records.')

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