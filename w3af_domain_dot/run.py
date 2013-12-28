# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class DomainDotTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: domain_dot
    """
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

execute_task(DomainDotTask)
