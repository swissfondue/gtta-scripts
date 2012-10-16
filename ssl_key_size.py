# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import re
import gtta
import sslyze_tools

class KeySizeTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    Size of SSL certificate public key
    """
    TIMEOUT = 60

    def main(self):
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

gtta.execute_task(KeySizeTask)
