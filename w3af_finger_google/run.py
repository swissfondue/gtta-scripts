# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task, ResultTable
from w3af import W3AFScriptLauncher

class FingerGoogleTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fingerGoogle
    """
    _result_limit = 300
    _fast_search = False

    def main(self, result_limit=[], fast_search=[], *args):
        """
        Main function
        """
        self._result_limit = 300
        self._fast_search = False

        if result_limit and result_limit[0]:
            self._result_limit = result_limit[0]

        if fast_search and fast_search[0] and fast_search[0] != '0':
            self._fast_search = True

        super(FingerGoogleTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery fingerGoogle",
            "discovery config fingerGoogle",
            "set fastSearch " + str(self._fast_search),
            "set resultLimit " + str(self._result_limit),
            "back",
            "back",
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
            table = ResultTable((
                { 'name' : 'E-mail', 'width' : 0.3 },
                { 'name' : 'URL',    'width' : 0.7 }
            ))

            for mail in mails:
                table.add_row(( mail[0], mail[1] ))

            return table.render()

        return 'No e-mails found.'

execute_task(FingerGoogleTask)
