# -*- coding: utf-8 -*-

from httplib import HTTPConnection, HTTPSConnection, HTTPException
from core import Task, execute_task

class Web_HTTP_Methods(Task):
    """
    Web HTTP methods
    """
    TIMEOUT = 60
    DANGEROUS_METHODS = ( 'TRACE', 'PUT', 'DELETE' )

    def main(self, *args):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        self._check_stop()

        if not self.proto:
            self.proto = 'http'

        if not self.port:
            if self.proto == 'http':
                self.port = 80
            elif self.proto == 'https':
                self.port = 443

        class_name = HTTPConnection

        if self.proto == 'https':
            class_name = HTTPSConnection

        try:
            conn = class_name(host=target, port=self.port, timeout=self.HTTP_TIMEOUT)
            conn.request('OPTIONS', '/')

            response = conn.getresponse()
            methods  = response.getheader('Allow')

            self._check_stop()

            if methods:
                methods = methods.replace(' ', '')
                methods = methods.split(',')

                dangerous = []

                for method in methods:
                    if method in self.DANGEROUS_METHODS:
                        dangerous.append(method)

                methods = dangerous

            else:
                methods = []

                for method in self.DANGEROUS_METHODS:
                    self._check_stop()

                    conn = HTTPConnection(self.host, timeout=self.HTTP_TIMEOUT)
                    conn.request(method, '/')

                    response = conn.getresponse()

                    if response.status not in ( 405, 501 ):
                        methods.append(method)

            if len(methods) > 0:
                self._write_result('Dangerous methods allowed: %s.' % ', '.join(methods))
            else:
                self._write_result('No dangerous methods allowed.')

        except HTTPException:
            self._write_result('HTTP error.')
            return

        self._check_stop()

        if not self.produced_output:
            self._write_result('No result.')

execute_task(Web_HTTP_Methods)
