# -*- coding: utf-8 -*-

from re import match, findall
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class CollectCookiesTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: collectCookies
    """
    def main(self):
        """
        Main function
        """
        super(CollectCookiesTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep collectCookies",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        cookies = []
        platform = None

        for line in result:
            cookie = match(r'The URL: "[^"]+" sent the cookie: "([^"]+)".', line)

            if cookie and not cookie.groups()[0] in cookies:
                cookies.append(cookie.groups()[0])

            platform_detection = findall(r'The remote platform is: "([^"]+)"', line)

            if platform_detection and not platform:
                platform = platform_detection[0]

        if len(cookies):
            msg = 'Found %i cookies:\n%s' % ( len(cookies), '\n'.join(cookies) )

            if platform:
                msg = '%s\n\nPlatform detected: %s' % ( msg, platform )

            return msg

        return 'No cookies found.'

gtta.execute_task(CollectCookiesTask)
