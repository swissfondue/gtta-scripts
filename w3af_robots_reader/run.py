# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class RobotsReaderTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: robotsReader
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery robotsReader",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []
        urls = []
        found = False

        for line in result:
            out_line = match(r'A robots.txt file was found at: "([^"]+)"', line)

            if out_line:
                found = True
                output.append('Found robots file at %s' % out_line.groups()[0])

            url = match(r'New URL found by robotsReader plugin: (.*)', line)

            if url and url.groups()[0] not in urls:
                if not url.groups()[0].endswith('robots.txt'):
                    urls.append(url.groups()[0])

        if found and urls:
            output.append('Found %i URLs in robots file:\n%s' % ( len(urls), '\n'.join(urls) ))

        if len(output):
            return '\n\n'.join(output)

        return 'Robots file not found.'

execute_task(RobotsReaderTask)
