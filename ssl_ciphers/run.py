# -*- coding: utf-8 -*-

from core import execute_task
from sslyze import SSLyzeLauncher

class SSLCiphersTask(SSLyzeLauncher):
    """
    SSL ciphers checker
    """
    TIMEOUT = 60

    def _get_commands(self):
        """
        Returns the list of sslyze options
        """
        return [
            '--sslv2',
            '--sslv3',
            '--tlsv1',
            #'--tlsv1_1',
            #'--tlsv1_2',
        ]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        data = data.split('\n')
        accepted = []

        add = False

        for line in data:
            if add and not line:
                add = False
                continue

            if add:
                line = line[8:]

                if line not in accepted:
                    accepted.append(line)

            if line.find('Accepted Cipher Suite(s):') != -1 and line.find('None') == -1:
                add = True
                continue

        out_data = []

        if accepted:
            out_data = 'Accepted ciphers:\n' + '\n'.join(accepted)
        else:
            out_data = 'No ciphers accepted.'

        return out_data

    def test(self):
        """
        Test function
        """
        self.host = "www.google.com"
        self.main()

execute_task(SSLCiphersTask)
