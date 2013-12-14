# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class SitemapReaderTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: sitemapReader
    """
    def main(self, *args):
        """
        Main function
        """
        super(SitemapReaderTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery sitemapReader",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []

        for line in result:
            url = match(r'New URL found by sitemapReader plugin: (.*)', line)

            if url and url.groups()[0] not in output:
                if not url.groups()[0].endswith('sitemap.xml'):
                    output.append(url.groups()[0])

        if len(output):
            return 'Found %i URLs in sitemap:\n%s' % ( len(output), '\n'.join(output) )

        return 'Sitemap file not found.'

execute_task(SitemapReaderTask)
