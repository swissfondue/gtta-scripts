# -*- coding: utf-8 -*-

from socket import gethostbyname
from time import sleep
from scapy.all import sr1, IP, TCP
from core import Task, execute_task
from core.error import InvalidTarget

class TCP_Timestamp(Task):
    """
    TCP timestamp task
    """
    TIMEOUT = 60
    TCP_TIMEOUT = 10
    NUMBER_OF_PACKETS = 3
    PACKET_DELAY = 1
    DEFAULT_PORT = 80

    def main(self, *args):
        """
        Main function
        """
        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except Exception:
                raise InvalidTarget('Host not found.')

        timestamps = []

        # sending packets
        for i in xrange(self.NUMBER_OF_PACKETS):
            self._check_stop()

            packet = IP(dst=self.ip) / TCP(dport=self.port or self.DEFAULT_PORT, options=[( 'Timestamp', (1, 0) )])

            try:
                data = sr1(packet, timeout=self.TCP_TIMEOUT)

                if not data:
                    raise Exception('host unreachable')

                if 'timestamp' in map(lambda opt: opt[0].lower(), data.getlayer('TCP').options):
                    timestamp = 0

                    for option in data.getlayer('TCP').options:
                        if option[0].lower() == 'timestamp':
                            timestamp = option[1][0]

                    timestamps.append(( i + 1, str(timestamp) ))

                else:
                    timestamps.append(( i + 1, 'N/A' ))

            except Exception as e:
                timestamps.append(( i + 1, 'N/A (%s)' % str(e) ))

            sleep(self.PACKET_DELAY)

        self._write_result('#\tTimestamp')

        for timestamp in timestamps:
            self._write_result('%i\t%s' % timestamp)

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(TCP_Timestamp)
