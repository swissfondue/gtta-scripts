# -*- coding: utf-8 -*-
import requests
import socket
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task
from core.error import InvalidTarget

__author__ = 'user'


class IG_Domain_BGP(Task):
    """
    Searching records in BGP
    """
    target = ''

    def _is_ip_v4(self, address):
        """
        Check adress format is IPv4
        """
        try:
            socket.inet_aton(address)
            result = True
        except socket.error:
            result = False
        return result

    def _search_by_ip(self, ip, res):
        """
        Searching by ip
        """
        soup = BeautifulSoup(
            requests.get(
                'http://bgp.he.net/ip/%s' % ip,
                headers={'User-Agent': 'Mozilla/5.0'}
            ).content)
        div = soup.find('div', attrs={'id': 'dns'})
        for tag in div.findAll('a'):
            res.append(tag.text)
            self._write_result(tag.text)

    def main(self, *args):
        """
        Main function
        """
        if not self.target:
            raise InvalidTarget('No target specified.')

        self._check_stop()
        self._write_result('target = "%s"' % self.target)
        results = []

        if self._is_ip_v4(self.target):
            self._search_by_ip(self.target, results)
        else:
            try:
                ip = socket.gethostbyname(self.target)
                self._search_by_ip(ip, results)
            except:
                pass

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

execute_task(IG_Domain_BGP)
