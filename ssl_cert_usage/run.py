# -*- coding: utf-8 -*-

import re
from core import execute_task
from sslyze import SSLyzeLauncher


class SSLCertificateUsageTask(SSLyzeLauncher):
    """
    SSL certificate usage checker
    """
    TIMEOUT = 60

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

    def test(self):
        """
        Test function
        """
        self.host = "www.google.com"
        self.main()

execute_task(SSLCertificateUsageTask)
