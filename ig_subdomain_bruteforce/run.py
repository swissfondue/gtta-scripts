# -*- coding: utf-8 -*-
from socket import gethostbyname
from dns.resolver import Resolver
import string
import itertools
from core import Task, execute_task


class IG_Subdomain_Bruteforce(Task):
    """
    Get subdomains
    """
    TEST_TIMEOUT = 60 * 60

    # generate symbols for generating of subdomains
    symbols = string.lowercase + string.digits

    def recursion(self, lvl, store):
        """
        Recursively generator for 'yield'ing combinations of self.sybmols
        """
        for char in self.symbols:
            new_store = store + char

            if lvl > 0:
                for item in self.recursion(lvl - 1, new_store):
                    yield item
            else:
                yield new_store

    def mygen(self, min_l, max_l):
        """
        Subdomains generator. Using generator 'recursion'.
        """
        while min_l <= max_l:
            for generator in self.recursion(min_l - 1, ''):
                yield generator
            min_l += 1

    def main(self, *args):
        """
        Main function
        """
        minimal_len = args[0][0]
        maximal_len = args[1][0]
        if minimal_len > maximal_len:
            self._write_result('Incorrect min and max length.')
            return

        if not self.host:
            return

        if self.host.startswith("www."):
            self.host = self.host[4:]

        # collect NSs
        r = Resolver()
        r.lifetime = self.DNS_TIMEOUT

        name_servers = r.query(self.host, 'NS')
        name_servers = map(lambda x: str(x), name_servers)

        ns_list = []

        for name_server in name_servers:
            if name_server[-1] == '.':
                name_server = name_server[:-1]

            ns_list.append(gethostbyname(name_server))

        r = Resolver()
        r.lifetime = self.DNS_TIMEOUT
        r.nameservers = ns_list

        # search really subdomains
        results = set()

        for sub in self.mygen(minimal_len, maximal_len):
            domain = '%s.%s' % (sub, self.host)

            try:
                a_records = r.query(domain, 'A')
                if a_records:
                    if sub not in results:
                        results.add(sub)
                        self._write_result(sub)
                    continue
            except Exception as e:
                pass

            try:
                cname_records = r.query(domain, 'CNAME')
                if cname_records:
                    if sub not in results:
                        results.add(sub)
                        self._write_result(sub)
            except Exception as e:
                pass

    def test(self):
        """
        Test function
        """
        self.host = "clariant.com"
        self.main([1], [2])

execute_task(IG_Subdomain_Bruteforce)
