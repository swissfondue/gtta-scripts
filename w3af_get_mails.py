# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class GetMailsTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: getMails
    """
    def main(self):
        """
        Main function
        """
        super(GetMailsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep getMails",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(GetMailsTask)
