# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class PathDisclosureTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: pathDisclosure
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep pathDisclosure",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" has a path disclosure vulnerability which discloses: "([^"]+)".', line)

            if url:
                url = '%s (%s)' % url.groups()

                if url not in urls:
                    urls.append(url)

        if len(urls):
            return 'Found %i URLs with path disclosure vulnerability:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No URLs with path disclosure vulnerability found.'

execute_task(PathDisclosureTask)
