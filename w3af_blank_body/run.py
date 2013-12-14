# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class BlankBodyTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: blankBody
    """
    def main(self, *args):
        """
        Main function
        """
        super(BlankBodyTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep blankBody",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" returned an empty body', line)

            if url and not url.groups()[0] in urls:
                urls.append(url.groups()[0])

        if len(urls):
            return 'Found %i URLs with blank body:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No URLs with blank bodies found.'

execute_task(BlankBodyTask)
