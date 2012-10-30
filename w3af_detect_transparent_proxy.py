# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DetectTransparentProxyTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: detectTransparentProxy
    """
    def main(self):
        """
        Main function
        """
        super(DetectTransparentProxyTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery detectTransparentProxy",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []

        for line in result:
            out_line = match(r'(Your ISP seems to have a transparent proxy installed|Your ISP has no transparent proxy)', line)

            if out_line:
                output.append(out_line.groups()[0])

        if len(output):
            return '\n'.join(output) + '.'

        return 'Your ISP has no transparent proxy.'

gtta.execute_task(DetectTransparentProxyTask)
