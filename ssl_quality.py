# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import sslyze_tools

class SSLQualityTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    SSL quality checker
    """
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
            "--regular",
        ]

gtta.execute_task(SSLQualityTask)
