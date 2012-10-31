# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class PrivateIPTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: privateIP
    """
    def main(self):
        """
        Main function
        """
        super(PrivateIPTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep privateIP",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        header_ips = []
        html_ips = []

        for line in result:
            ip = match(r'The URL: "([^"]+)" returned an HTTP header with an IP address: "([^"]+)"\.', line)

            if ip:
                ip = '%s (%s)' % ip.groups()

                if ip not in header_ips:
                    header_ips.append(ip)

            ip = match(r'The URL: "([^"]+)" returned an HTML document with an IP address: "([^"]+)"\.', line)

            if ip:
                ip = '%s (%s)' % ip.groups()

                if ip not in html_ips:
                    html_ips.append(ip)

        msg = []

        if len(header_ips):
            msg.append('Found %i URLs with IP address in HTTP header:\n%s' % ( len(header_ips), '\n'.join(header_ips) ))

        if len(html_ips):
            msg.append('Found %i URLs with IP address in HTML document:\n%s' % ( len(html_ips), '\n'.join(html_ips) ))

        if msg:
            return '\n\n'.join(msg)

        return 'No private IP addresses found.'

gtta.execute_task(PrivateIPTask)
