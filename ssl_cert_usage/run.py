# -*- coding: utf-8 -*-

import re
from core import Task, execute_task
from sslyze import SSLyzeLauncher

class SSLCertificateUsageTask(Task, SSLyzeLauncher):
    """
    SSL certificate usage checker
    """
    TIMEOUT = 60

    def main(self, *args):
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

execute_task(SSLCertificateUsageTask)
