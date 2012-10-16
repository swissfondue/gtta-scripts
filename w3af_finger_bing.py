# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FingerBingTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fingerBing
    """
    def main(self):
        """
        Main function
        """
        super(FingerBingTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery fingerBing",
            "back"
        ]

gtta.execute_task(FingerBingTask)
