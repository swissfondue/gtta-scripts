# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FingerPKSTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fingerPKS
    """
    def main(self):
        """
        Main function
        """
        super(FingerPKSTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery fingerPKS",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        mails = []
        known_mails = []

        for line in result:
            mail = match(r'The mail account: "([^"]+)" was found in the (.+?) server', line)

            if mail and not mail.groups()[0] in known_mails:
                mails.append(( mail.groups()[0], mail.groups()[1] ))
                known_mails.append(mail.groups()[0])

        if len(mails):
            table = gtta.ResultTable((
                { 'name' : 'E-mail', 'width' : 0.5 },
                { 'name' : 'Server', 'width' : 0.5 }
            ))

            for mail in mails:
                table.add_row(( mail[0], mail[1] ))

            return table.render()

        return 'No e-mails found.'

gtta.execute_task(FingerPKSTask)
