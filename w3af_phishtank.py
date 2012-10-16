# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class PhishtankTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: phishtank
    """
    def main(self):
        """
        Main function
        """
        super(PhishtankTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery phishtank",
            "back"
        ]

gtta.execute_task(PhishtankTask)
