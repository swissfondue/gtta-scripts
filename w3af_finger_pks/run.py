# -*- coding: utf-8 -*-

from re import match
from core import execute_task, ResultTable
from w3af import W3AFScriptLauncher

class FingerPKSTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fingerPKS
    """
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

        for line in result:
            mail = match(r'The mail account: "([^"]+)" was found in the (.+?) server', line)

            if mail:
                mails.append(( mail.groups()[0], mail.groups()[1] ))

        if len(mails):
            table = ResultTable((
                { 'name' : 'E-mail', 'width' : 0.5 },
                { 'name' : 'Server', 'width' : 0.5 }
            ))

            for mail in mails:
                table.add_row(( mail[0], mail[1] ))

            return table.render()

        return 'No e-mails found.'

execute_task(FingerPKSTask)
