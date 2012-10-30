# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FaviconIdentificationTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: favicon_identification
    """
    def main(self):
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

gtta.execute_task(FaviconIdentificationTask)
