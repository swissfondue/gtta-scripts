# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from socket import gethostbyname
from scapy.all import sr1, IP, ICMP
from random import randint
from gtta import Task, execute_task

class ICMP_IP_ID(Task):
    """
    Ping task
    """
    TIMEOUT = 60
    ICMP_TIMEOUT = 10
    NUMBER_OF_PACKETS = 3
    MAX_ID = 65535

    def main(self):
        """
        Main function
        """
        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except:
                self._write_result('Host not found: %s' % self.host)
                return

        id = randint(0, self.MAX_ID - self.NUMBER_OF_PACKETS)
        ids = []

        # sending 3 packets
        for i in xrange(self.NUMBER_OF_PACKETS):
            packet = IP(dst=self.ip) / ICMP()
            packet.id = id

            try:
                data = sr1(packet, timeout=self.ICMP_TIMEOUT)

                if not data:
                    raise Exception('host unreachable')

                ids.append(( i + 1, str(id), str(data.id) ))

            except Exception as e:
                ids.append(( i + 1, str(id), 'N/A (%s)' % str(e) ))

            id += 1

        if ids:
            self._write_result('#\tSrc ID\tDst ID')

            for id in ids:
                self._write_result('%i\t%s\t%s' % id)

        else:
            self._write_result('Destination host unreachable.')

execute_task(ICMP_IP_ID)
