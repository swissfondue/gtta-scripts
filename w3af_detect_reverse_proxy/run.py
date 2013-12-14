# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class DetectReverseProxyTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: detectReverseProxy
    """
    def main(self, *args):
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

execute_task(DetectReverseProxyTask)
