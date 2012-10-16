# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FeedsTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: feeds
    """
    def main(self):
        """
        Main function
        """
        super(FeedsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep feeds",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(FeedsTask)
