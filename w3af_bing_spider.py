# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class BingSpiderTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: bing_spider
    """
    def main(self):
        """
        Main function
        """
        super(BingSpiderTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery bing_spider",
            "grep getMails",
            "back"
        ]

gtta.execute_task(BingSpiderTask)
