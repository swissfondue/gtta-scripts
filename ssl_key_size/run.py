# -*- coding: utf-8 -*-

import re
from core import Task, execute_task
from sslyze import SSLyzeLauncher

class KeySizeTask(Task, SSLyzeLauncher):
    """
    Size of SSL certificate public key
    """
    TIMEOUT = 60

    def main(self, *args):
        """
        Main function
        """
        super(KeySizeTask, self).main()

    def _get_commands(self):
        """
        Returns the list of sslyze options
        """
        return [
            "--certinfo=basic",
        ]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        size = re.search(r'Key Size: *(\d+)', data).groups()[0]
        return 'Key size: %s\n' % size

    def test(self):
        """
        Test function
        """
        self.host = "www.google.com"
        self.main()

execute_task(KeySizeTask)
