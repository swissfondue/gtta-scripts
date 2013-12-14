# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class FaviconIdentificationTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: favicon_identification
    """
    def main(self, *args):
        """
        Main function
        """
        super(FaviconIdentificationTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery favicon_identification",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []

        for line in result:
            out_line = match(r'(Favicon.ico file was identified as "[^"]+".)', line)

            if out_line:
                output.append(out_line.groups()[0])

        if len(output):
            return '\n'.join(output)

        return 'Favicon identification failed.'

execute_task(FaviconIdentificationTask)
