# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class FeedsTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: feeds
    """
    def main(self, *args):
        """
        Main function
        """
        super(FeedsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep feeds",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" is a ([^ ]+) version "([^"]+)" feed', line)

            if url:
                url = '%s (%s %s)' % url.groups()

                if not url in urls:
                    urls.append(url)

        if len(urls):
            return 'Found %i feeds:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No feeds found.'

execute_task(FeedsTask)
