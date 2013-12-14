# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM, error as socket_error, gethostbyname
from errno import EINPROGRESS, EALREADY
from select import select
from core import Task, execute_task
from core.error import GTTAError

class TimedOut(GTTAError):
    pass

class NoMatch(GTTAError):
    pass

class NIC_Whois(Task):
    """
    NIC whois task
    """
    TIMEOUT = 60
    WHOIS_PORT = 43
    BUFFER_LENGTH = 8196
    SERVER_LIST = [
        'whois.arin.net', 'whois.ripe.net', 'whois.apnic.net', 'whois.lacnic.net', 'whois.afrinic.net'
    ]

    def query_whois(self, query, server):
        """
        Query whois
        """
        s = socket(AF_INET, SOCK_STREAM)

        while True:
            try:
                s.connect(( server, self.WHOIS_PORT ))

            except socket_error as ( ecode, reason ):
                if ecode in ( EINPROGRESS, EALREADY ):
                    continue

                raise

            break

        ret = select([ s ], [ s ], [], self.TIMEOUT)

        if len(ret[1]) == 0 and len(ret[0]) == 0:
            s.close()
            raise TimedOut

        s.setblocking(True)

        if server == 'whois.arin.net':
            query = 'n %s\n' % query
        else:
            query = '%s\n' % query

        s.send(query)
        page = ''

        while 1:
            data = s.recv(self.BUFFER_LENGTH)

            if not data:
                break

            page = page + data

            pass

        s.close()

        page = page.decode('utf-8', 'ignore')

        if page.find('IANA-BLK') != -1 or \
            page.find('Not allocated by') != -1 or \
            page.find('further assigned') != -1 or \
            page.find('further allocation') != -1 or \
            page.find('Please search the other RIRs') != -1 or \
            page.find('not registered in') != -1 or \
            page.find('not managed by') != -1 or \
            page.find('Allocated to ') != -1 or \
            page.find('not administered by') != -1 or \
            page.find('AFRINIC resource: ') != -1:
            raise NoMatch

        return page

    def main(self, *args):
        """
        Main function
        """
        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except Exception:
                self._write_result('Host not found: %s' % self.host)
                return

        for server in self.SERVER_LIST:
            try:
                res = self.query_whois(self.ip, server)
                self._write_result(res)

            except:
                continue

            break

        if not self.produced_output:
            self._write_result('No info found.')

execute_task(NIC_Whois)
