# -*- coding: utf-8 -*-

import socket
import sys
sys.path.append('pythonlib')
from gtta import Task, execute_task

class CheckSSHVersionTask(Task):
    """
    GTTA Check SSH version d@d.kiev.ua
    """
    TIMEOUT=60
    def main(self):
        s = socket.socket()
        port = self.port or 22
	self._write_result('Trying %s port %s' % (self.ip,port))
        s.connect((self.ip,port))
        output = s.recv(128)
        s.close()
        self._write_result(output)

execute_task(CheckSSHVersionTask)
