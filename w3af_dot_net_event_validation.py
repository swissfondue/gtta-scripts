# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class DotNetEventValidationTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: dotNetEventValidation
    """
    def main(self):
        """
        Main function
        """
        super(DotNetEventValidationTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep dotNetEventValidation",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls_validation = []
        urls_encryption = []

        for line in result:
            url = match(r'The URL: "([^"]+)" has .NET Event Validation disabled.', line)

            if url and not url.groups()[0] in urls_validation:
                urls_validation.append(url.groups()[0])

            url = match(r'The URL: "([^"]+)" has .NET ViewState encryption disabled.', line)

            if url and not url.groups()[0] in urls_encryption:
                urls_encryption.append(url.groups()[0])

        msg = []

        if len(urls_validation):
            msg.append('Found %i URLs with disabled event validation (possible programming/configuration error):\n%s' % ( len(urls_validation), '\n'.join(urls_validation) ))

        if len(urls_encryption):
            msg.append('Found %i URLs with disabled ViewState encryption (exploitable programming/configuration error):\n%s' % ( len(urls_encryption), '\n'.join(urls_encryption) ))

        if msg:
            return '\n\n'.join(msg)

        return 'No URLs with incorrect event validation found.'

gtta.execute_task(DotNetEventValidationTask)
