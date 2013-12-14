# -*- coding: utf-8 -*-

from subprocess import call
from core import Task, execute_task

class SSLQualityTask(Task):
    """
    SSL quality checker
    """
    _PROTOCOLS = ('ssl2', 'ssl3', 'tls1', 'tls1_1', 'tls1_2')
    _PROTOCOL_NAMES = {
        'ssl2': 'SSL 2.0',
        'ssl3': 'SSL 3.0',
        'tls1': 'TLS 1.0',
        'tls1_1': 'TLS 1.1',
        'tls1_2': 'TLS 1.2'
    }

    def main(self, *args):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        port = self.port

        if not port:
            port = 443

        for protocol in self._PROTOCOLS:
            return_code = call(
                'echo "GET /" | openssl s_client -%s -connect %s:%i' % (protocol, target, port),
                shell=True
            )

            result = "No"

            if return_code == 0:
                result = "Yes"

            self._write_result("%s: %s" % (self._PROTOCOL_NAMES[protocol], result))

execute_task(SSLQualityTask)
