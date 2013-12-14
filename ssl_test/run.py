# -*- coding: utf-8 -*-

from core import Task, execute_task
from sslyze import SSLyzeLauncher

class SSLQualityTask(Task, SSLyzeLauncher):
    """
    SSL quality checker
    """
    TIMEOUT = 60

    def main(self, *args):
        """
        Main function
        """
        super(SSLQualityTask, self).main()

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

execute_task(SSLQualityTask)
