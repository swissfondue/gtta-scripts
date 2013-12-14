# -*- coding: utf-8 -*-

from re import match
from string import strip
from socket import socket, AF_INET, SOCK_STREAM
from core import Task, execute_task

class SMTP_Banner(Task):
    """
    Return SMTP Banner
    """
    TIMEOUT = 60
    MAX_LINES = 5

    def main(self, *args):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        self._check_stop()

        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(self.SOCKET_TIMEOUT)
            s.connect(( target, 25 ))

            file = s.makefile('rb')

        except:
            self._write_result('Error connecting to SMTP server.')
            return

        try:
            lines = 0

            while True:
                line = file.readline()
                line = strip(line)

                self._write_result(line)
                lines += 1

                if match('^\d{3} ', line) or lines > self.MAX_LINES:
                    break

        except:
            self._write_result('Error reading SMTP banner.')
            return

        self._check_stop()

        if not self.produced_output:
            self._write_result('No SMTP banner.')

execute_task(SMTP_Banner)
