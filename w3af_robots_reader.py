# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class RobotsReaderTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: robotsReader
    """
    def main(self):
        """
        Main function
        """
        super(RobotsReaderTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery robotsReader",
            "back"
        ]

gtta.execute_task(RobotsReaderTask)
