# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class StrangeHTTPCodeTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: strangeHTTPCode
    """
    def main(self):
        """
        Main function
        """
        super(StrangeHTTPCodeTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep strangeHTTPCode",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(StrangeHTTPCodeTask)
