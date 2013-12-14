# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class StrangeHTTPCodeTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: strangeHTTPCode
    """
    def main(self, *args):
        """
        Main function
        """
        super(StrangeHTTPCodeTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep strangeHTTPCode",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The remote Web server sent a strange HTTP response code: "([^"]+)" with the message: "([^"]+)" at "([^"]+)"', line)

            if url:
                url = '%s (%s %s)' % ( url.groups()[2], url.groups()[0], url.groups()[1] )

                if url not in urls:
                    urls.append(url)

        if len(urls):
            return 'Found %i URLs with strange HTTP codes:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No strange HTTP codes found.'

execute_task(StrangeHTTPCodeTask)
