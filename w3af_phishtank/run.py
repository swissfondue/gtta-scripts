# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class PhishtankTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: phishtank
    """
    def main(self, *args):
        """
        Main function
        """
        super(PhishtankTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery phishtank",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = None

        for line in result:
            output_str = match(r'The URL: "([^"]+)" seems to be involved in a phishing scam. Please see "([^"]+)" for more info', line)

            if output_str:
                output = 'The target is listed in the PhishTank database: %s\nPlease see %s for more info.' % output_str.groups()
                break

        if output:
            return output

        return 'The target is not listed in the PhishTank database.'

execute_task(PhishtankTask)