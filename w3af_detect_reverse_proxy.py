# -*- coding: utf-8 -*-

from re import match
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

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []

        for line in result:
            out_line = match(r'(The remote web server seems to have a reverse proxy installed.|The remote web server doesn\'t seem to have a reverse proxy.)', line)

            if out_line:
                output.append(out_line.groups()[0])

        if len(output):
            return '\n'.join(output)

        return 'The remote web server doesn\'t seem to have a reverse proxy.'

gtta.execute_task(DetectReverseProxyTask)
