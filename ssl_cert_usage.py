# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import re

import gtta
import sslyze_tools

class SSLCertificateUsageTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    SSL certificate usage checker
    """
    TIMEOUT = 60

    def main(self):
        """
        Main function
        """
        super(SSLCertificateUsageTask, self).main()

    def _get_commands(self):
        """
        Returns the list of sslyze options
        """
        return [
            "--certinfo=full",
        ]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        try:
            groups = re.search(r'Key Usage:\s\n\s+(.*?)$', data, re.MULTILINE).groups()
        except AttributeError:
            return "No key usage info!"

        return "Key usage: %s" % ''.join(groups)

gtta.execute_task(SSLCertificateUsageTask)
