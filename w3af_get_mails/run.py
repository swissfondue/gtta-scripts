# -*- coding: utf-8 -*-

from re import match, findall
from core import Task, execute_task, ResultTable
from w3af import W3AFScriptLauncher

class GetMailsTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: getMails
    """
    def main(self, *args):
        """
        Main function
        """
        super(GetMailsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep getMails",
            "grep config getMails",
            "set onlyTargetDomain False",
            "back",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        mails = []

        for line in result:
            mail = match(r'The mail account: "([^"]+)"', line)

            if mail:
                urls = findall(r'- (.*?) - In request with id:', line)

                for url in urls:
                    mails.append(( mail.groups()[0], url ))

        if len(mails):
            table = ResultTable((
                { 'name' : 'E-mail', 'width' : 0.3 },
                { 'name' : 'URL',    'width' : 0.7 }
            ))

            for mail in mails:
                table.add_row(( mail[0], mail[1] ))

            return table.render()

        return 'No e-mails found.'

execute_task(GetMailsTask)