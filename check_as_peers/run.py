# -*- coding: utf-8 -*-
"""
$Id: check_as_peers.py,v 1.6 2013/02/07 03:05:33 dee Exp $
"""
import socket
from core import Task, execute_task


class CheckASPeers(Task):
    """Check AS peers"""

    def main(self, *args):
        """
        GTTA check AS peers via cymru.com whois server
        @author: d@d.kiev.ua
        """
        if not self.ip:
            try:
                self.ip = socket.gethostbyname(self.host)
            except Exception:
                self._write_result('Host not found: %s' % self.host)
                return
        s = socket.socket()
        s.connect((socket.gethostbyname('v4.whois.cymru.com'),43))
        # query for AS
        self._write_result('SOURCE  | v4.whois.cymru.com')
        s.send(' -v %s\n' % self.ip)
        output = s.recv(4096)
        s.close()
        self._write_result(output.strip())
        # query for AS peers
        s = socket.socket()
        s.connect((socket.gethostbyname('v4-peer.whois.cymru.com'),43))
        self._write_result('SOURCE  | v4-peer.whois.cymru.com')
        s.send(' -v %s\n' % self.ip)
        output = s.recv(4096)
        s.close()
        self._write_result(output.strip())
        self._write_result('\nUPSTREAM PEER(s) DETECTED: %s' % (len(output.strip().split('\n'))-1))

    def test(self):
        """
        Test function
        """
        self.ip = "8.8.8.8"
        self.main()

execute_task(CheckASPeers)
