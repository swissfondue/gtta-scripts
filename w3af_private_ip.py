# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class PrivateIPTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: privateIP
    """
    def main(self):
        """
        Main function
        """
        super(PrivateIPTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep privateIP",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(PrivateIPTask)
