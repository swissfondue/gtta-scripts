# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class AjaxTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: ajax
    """
    def main(self):
        """
        Main function
        """
        super(AjaxTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep ajax",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(AjaxTask)
