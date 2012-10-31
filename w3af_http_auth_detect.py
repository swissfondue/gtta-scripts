# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class HttpAuthDetectTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: httpAuthDetect
    """
    def main(self):
        """
        Main function
        """
        super(HttpAuthDetectTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep httpAuthDetect",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        uri_passwords = []
        body_passwords = []
        noauth_urls = []
        auth_urls = []

        for line in result:
            url = match(r'The resource: "([^"]+)" has a user and password in the URI.', line)

            if url and not url.groups()[0] in uri_passwords:
                uri_passwords.append(url.groups()[0])

            url = match(r'The resource: "([^"]+)" has a user and password in the body. The offending URL is: "([^"]+)".', line)

            if url:
                url = '%s (%s)' % url.groups()

                if url not in body_passwords:
                    body_passwords.append(url)

            url = match(r'The resource: "([^"]+)" requires authentication \(HTTP Code 401\) but the www-authenticate header is not present.', line)

            if url and not url.groups()[0] in noauth_urls:
                noauth_urls.append(url.groups()[0])

            url = match(r'The resource: "([^"]+)" requires authentication. The realm is: "(.*?)"\.', line)

            if url:
                url = '%s (%s)' % url.groups()

                if url not in auth_urls:
                    auth_urls.append(url)

        msg = []

        if len(uri_passwords):
            msg.append('Found %i URLs with a user and password in URI:\n%s' % ( len(uri_passwords), '\n'.join(uri_passwords) ))

        if len(body_passwords):
            msg.append('Found %i URLs with a user and password in the body:\n%s' % ( len(body_passwords), '\n'.join(body_passwords) ))

        if len(noauth_urls):
            msg.append('Found %i URLs that require authentication, but the www-authenticate header is not present:\n%s' % ( len(noauth_urls), '\n'.join(noauth_urls) ))

        if len(auth_urls):
            msg.append('Found %i URLs that require authentication:\n%s' % ( len(auth_urls), '\n'.join(auth_urls) ))

        return '\n\n'.join(msg)

        return 'No URLs with required authentication found.'

gtta.execute_task(HttpAuthDetectTask)
