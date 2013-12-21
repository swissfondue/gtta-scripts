# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class SvnUsersTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: svnUsers
    """
    def main(self, *args):
        """
        Main function
        """
        super(SvnUsersTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep svnUsers",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" contains a SVN versioning signature with the username: "([^"]+)"', line)

            if url:
                url = '%s (%s)' % url.groups()

                if url not in urls:
                    urls.append(url)

        if len(urls):
            return 'Found %i URLs with a SVN signature:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No SVN signatures found.'

execute_task(SvnUsersTask)