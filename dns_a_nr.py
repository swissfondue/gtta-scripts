# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from dns import rdatatype, rdataclass, flags, query as dns_query, rcode, name as dns_name
from dns.message import make_query
from dns.resolver import NXDOMAIN, NoAnswer, Answer
from dns.exception import DNSException, Timeout
from socket import gethostbyname
from gtta import Task, execute_task
from gtta.error import NoHostName, InvalidTarget

class DNS_A_NR(Task):
    """
    Get DNS A records (non-recursive DNS request)
    """
    DNS_PORT = 53

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
            # make DNS query manually, clearing the RD (recursion desired) flag
            query = make_query(domain, rdatatype.A, rdataclass.IN)
            query.flags ^= flags.RD

            found = False

            try:
                response = dns_query.udp(query, target, self.DNS_TIMEOUT, self.DNS_PORT, None)

            except Exception:
                response = None

            if response and response.rcode() == rcode.NXDOMAIN:
                raise NXDOMAIN

            if response and response.rcode() == rcode.NOERROR:
                found = True
            else:
                raise NXDOMAIN

            a_records = Answer(dns_name.from_text(domain), rdatatype.A, rdataclass.IN, response, True)
            a_records = map(lambda x: str(x), a_records)

            for a in a_records:
                if str(a) not in results:
                    results.append(str(a))
                    self._write_result(str(a))

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

execute_task(DNS_A_NR)
