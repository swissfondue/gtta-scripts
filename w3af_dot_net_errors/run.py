# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class DotNetErrorsTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: dotNetErrors
    """
    def main(self, *args):
        """
        Main function
        """
        super(DotNetErrorsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery dotNetErrors",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" discloses detailed error messages', line)

            if url and not url.groups()[0] in urls:
                urls.append(url.groups()[0])

        if len(urls):
            return 'Found %i URLs with detailed error message disclosure:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No URLs with detailed error message disclosure found.'

execute_task(DotNetErrorsTask)
