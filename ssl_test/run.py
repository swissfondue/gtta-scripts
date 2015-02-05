# -*- coding: utf-8 -*-

from core import execute_task
from sslyze import SSLyzeLauncher

class SSLQualityTask(SSLyzeLauncher):
    """
    SSL quality checker
    """

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
        out_data = []
        skip = False

        for line in data:
            if skip and not line:
                skip = False

            if line.find('Rejected Cipher Suite(s):') != -1:
                skip = True
                continue

            if skip:
                continue

            out_data.append(line)

        return '\n'.join(out_data)

    def test(self):
        """
        Test function
        """
        self.host = "www.google.com"
        self.main()

execute_task(SSLQualityTask)
