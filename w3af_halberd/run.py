# -*- coding: utf-8 -*-

from core import execute_task
from w3af import W3AFScriptLauncher

class HalberdTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: halberd
    """
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

execute_task(HalberdTask)
