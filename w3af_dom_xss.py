# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DomXSSTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: domXss
    """
    def main(self):
        """
        Main function
        """
        super(DomXSSTask, self).main()

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

gtta.execute_task(DomXSSTask)
