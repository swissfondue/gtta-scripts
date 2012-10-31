# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class HttpInBodyTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: httpInBody
    """
    def main(self):
        """
        Main function
        """
        super(HttpInBodyTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep httpInBody",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        requests = []
        responses = []

        for line in result:
            request = match(r'An HTTP request was found in the HTTP body of a response: "([^"]+)"', line)

            if request and not request.groups()[0] in requests:
                requests.append(request.groups()[0])

            response = match(r'An HTTP response was found in the HTTP body of a response: "([^"]+)"', line)

            if response and not response.groups()[0] in responses:
                responses.append(response.groups()[0])

        msg = []

        if len(requests):
            msg.append('Found %i URLs with HTTP request:\n%s' % ( len(requests), '\n'.join(requests) ))

        if len(responses):
            msg.append('Found %i URLs with HTTP response:\n%s' % ( len(responses), '\n'.join(responses) ))

        if msg:
            return '\n\n'.join(msg)

        return 'No URLs with HTTP requests or responses found.'

gtta.execute_task(HttpInBodyTask)
