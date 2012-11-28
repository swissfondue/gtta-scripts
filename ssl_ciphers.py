# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import sslyze_tools

class SSLCiphersTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    SSL ciphers checker
    """
    TIMEOUT = 60

    def main(self):
        """
        Main function
        """
        super(SSLCiphersTask, self).main()

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

gtta.execute_task(SSLCiphersTask)
