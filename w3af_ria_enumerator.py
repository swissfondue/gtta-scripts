# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class RIAEnumeratorTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: ria_enumerator
    """
    def main(self):
        """
        Main function
        """
        super(RIAEnumeratorTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery ria_enumerator",
            "back"
        ]

gtta.execute_task(RIAEnumeratorTask)
