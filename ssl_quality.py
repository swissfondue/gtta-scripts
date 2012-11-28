# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import sslyze_tools

class SSLQualityTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    SSL quality checker
    """
    TIMEOUT = 60

    def main(self):
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
        protocols = {
            'TLS 1.0' : False,
            #'TLS 1.1' : False,
            #'TLS 1.2' : False,
            'SSL 2.0' : False,
            'SSL 3.0' : False
        }

        proto = None
        skip = False

        for line in data:
            if line.startswith('  *'):
                proto = line[4:line.find(' ', 5)]

                if proto == 'SSLV2':
                    proto = 'SSL 2.0'
                elif proto == 'SSLV3':
                    proto = 'SSL 3.0'
                elif proto == 'TLSV1':
                    proto = 'TLS 1.0'
                #elif proto == 'TLSV1_1':
                #    proto = 'TLS 1.1'
                #elif proto == 'TLSV1_2':
                #    proto = 'TLS 1.2'

                skip = False

                continue

            if skip:
                continue

            if line.find('Accepted Cipher Suite(s): None') != -1:
                protocols[proto] = False
                skip = True
                continue

            if line.find('Accepted Cipher Suite(s):') != -1:
                protocols[proto] = True
                skip = True
                continue

        out_data = []

        for key, value in protocols.iteritems():
            if value:
                value = 'Supported'
            else:
                value = 'Not Supported'

            out_data.append('%s: %s' % ( key, value ))

        return '\n'.join(out_data)

gtta.execute_task(SSLQualityTask)
