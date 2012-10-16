# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FingerGoogleTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fingerGoogle
    """
    def main(self):
        """
        Main function
        """
        super(FingerGoogleTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery fingerGoogle",
            "back"
        ]

gtta.execute_task(FingerGoogleTask)
