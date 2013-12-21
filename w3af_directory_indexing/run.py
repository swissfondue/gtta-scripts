# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class DirectoryIndexingTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: directoryIndexing
    """
    def main(self, *args):
        """
        Main function
        """
        super(DirectoryIndexingTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep directoryIndexing",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" has a directory indexing vulnerability', line)

            if url and not url.groups()[0] in urls:
                urls.append(url.groups()[0])

        if len(urls):
            return 'Found %i directories with indexing vulnerability:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No directory indexing vulnerabilities found.'

execute_task(DirectoryIndexingTask)
