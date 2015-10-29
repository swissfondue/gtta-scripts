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

    def _generate_subdomains(self, level, current_value=""):
        """Recursive subdomain generator"""
        for char in string.lowercase + string.digits:
            new_value = current_value + char

            if level > 0:
                for item in self._generate_subdomains(level - 1, new_value):
                    yield item

            else:
                yield new_value

    def generate_subdomains(self, min_len, max_len):
        """Subdomains generator"""
        while min_len <= max_len:
            for subdomain in self._generate_subdomains(min_len - 1):
                yield subdomain

            min_len += 1

    def main(self, min_len=(1,), max_len=(3,)):
        """
        Main function
        """
        min_len = min_len[0]
        max_len = max_len[0]

        if min_len > max_len:
            self._write_result("Min length should be less or equal to max length.")
            return

        if not self.host:
            return

        if self.host.startswith("www."):
            self.host = self.host[4:]

        # collect nameservers
        r = Resolver()
        r.lifetime = self.DNS_TIMEOUT

        name_servers = r.query(self.host, "NS")
        name_servers = map(lambda x: str(x), name_servers)

        ns_list = []

        for name_server in name_servers:
            if name_server[-1] == ".":
                name_server = name_server[:-1]

            ns_list.append(gethostbyname(name_server))

        r = Resolver()
        r.lifetime = self.DNS_TIMEOUT
        r.nameservers = ns_list

        results = set()

        for sub in self.generate_subdomains(min_len, max_len):
            domain = "%s.%s" % (sub, self.host)

            for record in ("A", "CNAME"):
                try:
                    records = r.query(domain, record)

                    if records:
                        if sub not in results:
                            results.add(sub)
                            self._write_result(domain)

                        break

                except Exception:
                    pass

    def test(self):
        """
        Test function
        """
        self.host = "clariant.com"
        self.main([1], [2])

execute_task(IG_Subdomain_Bruteforce)
