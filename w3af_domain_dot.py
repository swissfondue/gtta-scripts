# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DomainDotTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: domain_dot
    """
    def main(self):
        """
        Main function
        """
        super(DomainDotTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery domain_dot",
            "back",
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []

        for line in result:
            out_line = match(r'[Manual verification required] (.*)', line)

            if out_line:
                output.append(out_line.groups()[0])

        if len(output):
            return '\n'.join(output) + '.'

        return 'Responses are equal for both %s://%s/ and %s://%s./' % (
            self.proto or 'http',
            self.host or self.ip,
            self.proto or 'http',
            self.host or self.ip
        )

gtta.execute_task(DomainDotTask)
