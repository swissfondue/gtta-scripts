# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class GHDBTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: ghdb
    """
    def main(self):
        """
        Main function
        """
        super(GHDBTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery ghdb",
            "back"
        ]

gtta.execute_task(GHDBTask)
