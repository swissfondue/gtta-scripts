# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FingerBingTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fingerBing
    """
    def main(self):
        """
        Main function
        """
        super(FingerBingTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery fingerBing",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        mails = []

        for line in result:
            mail = match(r'The mail account: "([^"]+)"', line)

            if mail and not mail.groups()[0] in mails:
                mails.append(mail.groups()[0])

        if len(mails):
            return 'Found %i e-mails:\n%s' % ( len(mails), '\n'.join(mails) )

        return 'No e-mails found.'

gtta.execute_task(FingerBingTask)
