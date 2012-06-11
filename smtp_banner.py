# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from string import strip
from socket import socket, AF_INET, SOCK_STREAM
from gtta import Task, execute_task

class SMTP_Banner(Task):
    """
    Return SMTP Banner
    """
    def main(self):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        results = []

        self._check_stop()

        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(( target, 25 ))

            file = s.makefile('rb')

        except:
            return 'Error connecting to SMTP server.'

        banner = []

        try:
            while True:
                line = file.readline()
                line = strip(line)

                banner.append(line)

                if line[:4] == '220 ':
                    break

        except:
            return 'Error reading SMTP banner.'

        self._check_stop()

        if len(banner) > 0:
            return '\n'.join(banner)

        return 'No SMTP banner.'

execute_task(SMTP_Banner)
