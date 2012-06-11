# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from httplib import HTTPConnection, HTTPException
from gtta import Task, execute_task

class Web_HTTP_Methods(Task):
    """
    Web HTTP methods
    """
    DANGEROUS_METHODS = ( 'TRACE', 'PUT', 'DELETE' )

    def main(self, host=[]):
        """
        Main function
        """
        if host and host[0]:
            self.host = host[0]

        target = self.host

        if not target:
            target = self.ip

        results = []

        self._check_stop()

        try:
            conn = HTTPConnection(self.host, timeout=self.HTTP_TIMEOUT)
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
                results.append('Dangerous methods allowed: %s.' % ', '.join(methods))
            else:
                results.append('No dangerous methods allowed.')

        except HTTPException:
            return 'HTTP error.'

        self._check_stop()

        if len(results) > 0:
            return '\n'.join(results)

        return 'No result.'

execute_task(Web_HTTP_Methods)
