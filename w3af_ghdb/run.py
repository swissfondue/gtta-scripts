# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class GHDBTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: ghdb
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery ghdb",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        vulns = []

        for line in result:
            vuln = match(r'ghdb plugin found a vulnerability at URL: ([^ ]+) . Vulnerability description: (.*)', line)

            if vuln:
                vuln = '%s (%s)' % vuln.groups()

                if vuln not in vulns:
                    vulns.append(vuln)

        if len(vulns):
            return 'Found %i GHDB vulnerabilities:\n%s' % ( len(vulns), '\n'.join(vulns) )

        return 'No GHDB vulnerabilities found.'

execute_task(GHDBTask)
