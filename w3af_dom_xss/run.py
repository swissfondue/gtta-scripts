# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class DomXSSTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: domXss
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep domXss",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        vulns = []

        for line in result:
            vuln = match(r'The URL: "([^"]+)" has a DOM XSS \(Risky JavaScript Code\) bug using: "([^"]+)"', line)

            if vuln and not ('%s (%s)' % vuln.groups()) in vulns:
                vulns.append('%s (%s)' % vuln.groups())

        if len(vulns):
            return 'Found %i URLs with possible DOM XSS vulnerability:\n%s' % ( len(vulns), '\n'.join(vulns) )

        return 'No URLs with DOM XSS vulnerability found.'

execute_task(DomXSSTask)
