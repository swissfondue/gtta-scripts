# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from socket import gethostbyname
from scapy.all import sr1, IP, UDP, SNMP, SNMPget, SNMPvarbind, ASN1_OID, ICMP
from gtta import Task, execute_task
from gtta.error import InvalidTarget

class SNMP_Community(Task):
    """
    SNMP community string task
    """
    TIMEOUT = 60
    SNMP_TIMEOUT = 10
    SNMP_PORT = 161
    OID_SYSTEM_DESCRIPTION = '1.3.6.1.2.1.1.1.0'

    def main(self):
        """
        Main function
        """
        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except Exception:
                raise InvalidTarget('Host not found.')

        packet = IP(dst=self.ip) / UDP() / SNMP(
            community = 'public',
            PDU = SNMPget(varbindlist=[ SNMPvarbind(oid=ASN1_OID(self.OID_SYSTEM_DESCRIPTION)) ])
        )

        try:
            data = sr1(packet, timeout=self.SNMP_TIMEOUT)

            if not data:
                self._write_result('No answer.')
                return

            if ICMP in data:
                self._write_result('Failed to get data: %s' % repr(data.getlayer('ICMP')))
                return

            self._write_result('Got SNMP response: %s' % repr(data))

        except Exception as e:
            self._write_result(str(e))

execute_task(SNMP_Community)
