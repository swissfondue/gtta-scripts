# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DomainDotTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: domain_dot
    """
    def main(self):
        """
        Main function
        """
        super(DomainDotTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery domain_dot",
            "back",
        ]

gtta.execute_task(DomainDotTask)
