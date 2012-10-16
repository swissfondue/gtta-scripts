# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class CodeDisclosureTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: codeDisclosure
    """
    def main(self):
        """
        Main function
        """
        super(CodeDisclosureTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep codeDisclosure",
            "discovery webSpider",
            "back"
        ]

gtta.execute_task(CodeDisclosureTask)
