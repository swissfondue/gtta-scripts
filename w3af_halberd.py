# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class HalberdTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: halberd
    """
    def main(self):
        """
        Main function
        """
        super(HalberdTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery halberd",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        for line in result:
            if line.find('doesn\'t seem to have a HTTP load balancer configuration') >= 0:
                return 'The site doesn\'t seem to have a HTTP load balancer configuration.'

        return 'The site has HTTP load balancer.'

gtta.execute_task(HalberdTask)
