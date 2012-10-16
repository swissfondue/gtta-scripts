# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DotNetErrorsTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: dotNetErrors
    """
    def main(self):
        """
        Main function
        """
        super(DotNetErrorsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery dotNetErrors",
            "back"
        ]

gtta.execute_task(DotNetErrorsTask)
