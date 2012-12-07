# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import re
import datetime
import gtta
import sslyze_tools
import parse

class SSLValidityTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    SSL validity checker
    """
    TIMEOUT = 60

    def main(self):
        """
        Main function
        """
        super(SSLValidityTask, self).main()

    def _get_commands(self):
        """
        Returns the list of sslyze options
        """
        return [
            "--regular",
        ]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        def as_datetime(s):
            month, day, h, m, s, year = re.match(
                (r'([A-Z][a-z]{2})\s+(\d+) (\d\d):(\d\d):(\d\d) '
                r'(\d{4}) GMT'), s
            ).groups()

            month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'].index(month.upper()) + 1

            return datetime.datetime(
                int(year), month, int(day),
                int(h), int(m), int(s)
            )

        parser = parse.LineByLineParser()
        parser['Not Before:': as_datetime] = 'from'
        parser['Not After:': as_datetime] = 'to'
        parser['Certificate is Trusted'] = 'trusted'
        data = parser.parse(data.split('\n'))

        if 'trusted' in data and data['from'] <= datetime.datetime.now() <= data['to']:
            return 'Certificate is valid (expires %s)' % data['to']
        else:
            return 'Certificate is not valid (expires %s)' % data['to']

gtta.execute_task(SSLValidityTask)
