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

        packet = IP(dst=self.ip) / UDP(dport=self.SNMP_PORT, sport=self.SNMP_PORT) / SNMP(
            community = 'public',
            PDU = SNMPget(varbindlist=[ SNMPvarbind(oid=ASN1_OID(self.OID_SYSTEM_DESCRIPTION)) ])
        )

        self._write_result('Trying to read the system description through SNMP...')

        try:
            data = sr1(packet, timeout=self.SNMP_TIMEOUT)

            if not data or ICMP in data:
                self._write_result('No response received.')
                return

            value = data[SNMPvarbind].value.val

            if not value:
                value = 'no such object'

            self._write_result('Received response: %s' % str(value))

        except Exception as e:
            self._write_result(str(e))

execute_task(SNMP_Community)
