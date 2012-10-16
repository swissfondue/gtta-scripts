# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DetectReverseProxyTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: detectReverseProxy
    """
    def main(self):
        """
        Main function
        """
        super(DetectReverseProxyTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery detectReverseProxy",
            "back"
        ]

gtta.execute_task(DetectReverseProxyTask)
