# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class CodeDisclosureTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: codeDisclosure
    """
    def main(self, *args):
        """
        Main function
        """
        super(CodeDisclosureTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep codeDisclosure",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" has a (.*?) code disclosure vulnerability', line)

            if url and not ('%s (%s)' % url.groups()) in urls:
                urls.append('%s (%s)' % url.groups())

        if len(urls):
            return 'Found %i URLs with possible code disclosure:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No URLs with code disclosure found.'

execute_task(CodeDisclosureTask)
