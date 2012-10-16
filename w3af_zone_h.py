# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class ZoneHTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: zone_h
    """
    def main(self):
        """
        Main function
        """
        super(ZoneHTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery zone_h",
            "back"
        ]

gtta.execute_task(ZoneHTask)
