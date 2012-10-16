# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class HttpAuthDetectTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: httpAuthDetect
    """
    def main(self):
        """
        Main function
        """
        super(HttpAuthDetectTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep httpAuthDetect",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(HttpAuthDetectTask)
