# -*- coding: utf-8 -*-

import socket
from socket import gethostbyname
from core import Task, execute_task

class CheckSSHVersionTask(Task):
    """
    GTTA Check SSH version d@d.kiev.ua
    """
    TIMEOUT = 60

    def main(self, *args):
        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except:
                self._write_result('Host not found: %s' % self.host)
                return

        s = socket.socket()
        port = self.port or 22
        self._write_result('Trying %s port %s' % (self.ip,port))
        s.connect((self.ip,port))
        output = s.recv(128)
        s.close()
        self._write_result(output)

execute_task(CheckSSHVersionTask)
