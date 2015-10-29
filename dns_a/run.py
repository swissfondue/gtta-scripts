# -*- coding: utf-8 -*-

from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Resolver
from dns.exception import DNSException, Timeout
from socket import gethostbyname
from core import Task, execute_task
from core.error import NoHostName

class DNS_A(Task):
    """
    Get DNS A records
    """
    MULTITHREADED = True
    TEST_TARGETS = ["google.com", "bing.com", "microsoft.com"]

    def main(self, *args):
        """
        Main function
        """
        if not self.host:
            raise NoHostName('No host name specified.')

        if self.host.startswith("www."):
            self.host = self.host[4:]

        results = []

        self._check_stop()

        try:
            # get all name servers
            r = Resolver()
            r.lifetime = self.DNS_TIMEOUT

            name_servers = r.query(self.host, 'NS')
            name_servers = map(lambda x: str(x), name_servers)

            self._check_stop()

            ns_list = []

            for name_server in name_servers:
                if name_server[-1] == '.':
                    name_server = name_server[:-1]

                ns_list.append(gethostbyname(name_server))

            r = Resolver()
            r.lifetime = self.DNS_TIMEOUT
            r.nameservers = ns_list

            a_records = r.query(self.host, 'A')
            a_records = map(lambda x: str(x), a_records)

            for a in a_records:
                if str(a) not in results:
                    results.append(str(a))
                    self._write_result(str(a))

        except NoNameservers:
            self._write_result('No name servers.')
            return

        except ( NoAnswer, NXDOMAIN ):
            self._write_result('Host not found.')
            return

        except Timeout:
            self._write_result('DNS request timeout.')
            return

        except DNSException:
            self._write_result('DNS error.')
            return

        self._check_stop()

        if len(results) == 0:
            self._write_result('No A records.')

    def test(self):
        """
        Test function
        """
        self.main()

execute_task(DNS_A)
