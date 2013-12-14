# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class DetectTransparentProxyTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: detectTransparentProxy
    """
    def main(self, *args):
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

execute_task(DetectTransparentProxyTask)
