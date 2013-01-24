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
            mail = match(r'The mail account: "([^"]+)" was found in: "([^"]+)"', line)

            if mail:
                mails.append(( mail.groups()[0], mail.groups()[1] ))

        if len(mails):
            table = gtta.ResultTable((
                { 'name' : 'E-mail', 'width' : 0.3 },
                { 'name' : 'URL',    'width' : 0.7 }
            ))

            for mail in mails:
                table.add_row(( mail[0], mail[1] ))

            return table.render()

        return 'No e-mails found.'

gtta.execute_task(FingerBingTask)
