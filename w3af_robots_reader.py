# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class RobotsReaderTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: robotsReader
    """
    def main(self):
        """
        Main function
        """
        super(RobotsReaderTask, self).main()

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
                output.append('Found robots.txt file at %s' % out_line.groups()[0])

            url = match(r'New URL found by robotsReader plugin: (.*)', line)

            if url and url.groups()[0] not in urls:
                if not url.groups()[0].endswith('robots.txt'):
                    urls.append(url.groups()[0])

        if found and urls:
            output.append('Found %i URLs:\n%s' % ( len(urls), '\n'.join(urls) ))

        if len(output):
            return '\n\n'.join(output)

        return 'Robots.txt file not found.'

gtta.execute_task(RobotsReaderTask)
