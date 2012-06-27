# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Resolver
from dns.exception import DNSException, Timeout
from socket import gethostbyname
from gtta import Task, execute_task
from gtta.error import NoHostName, InvalidTarget

class DNS_A(Task):
    """
    Get DNS A records
    """
    def main(self, host=[]):
        """
        Main function
        """
        target = self.ip

        if self.host:
            try:
                target = gethostbyname(self.host)
            except:
                raise InvalidTarget('Host not found.')

        domain = None

        if host and host[0]:
            domain = host[0]

        if not domain:
            raise NoHostName('No host name specified.')

        results = []

        self._check_stop()

        try:
            r             = Resolver()
            r.lifetime    = self.DNS_TIMEOUT
            r.nameservers = [ target ]

            a_records = r.query(domain, 'A')
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

execute_task(DNS_A)
