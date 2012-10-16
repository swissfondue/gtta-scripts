# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FaviconIdentificationTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: favicon_identification
    """
    def main(self):
        """
        Main function
        """
        super(FaviconIdentificationTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery favicon_identification",
            "back"
        ]

gtta.execute_task(FaviconIdentificationTask)
