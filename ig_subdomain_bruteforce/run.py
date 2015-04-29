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

        results = set()
        subs = set()

        # generate subs
        symbols = string.lowercase + string.digits

        # get combinations
        while minimal_len <= maximal_len:
            map(lambda x: subs.add(''.join(list(x))), itertools.combinations_with_replacement(symbols, minimal_len))
            minimal_len += 1

        # use permutations
        permutations = set()
        for item in subs:
            map(lambda x: permutations.add(''.join(list(x))), itertools.permutations(item))

        subs.update(permutations)

        # search really subdomains
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

        for sub in subs:
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
