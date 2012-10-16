# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DotNetEventValidationTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: dotNetEventValidation
    """
    def main(self):
        """
        Main function
        """
        super(DotNetEventValidationTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep dotNetEventValidation",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(DotNetEventValidationTask)
