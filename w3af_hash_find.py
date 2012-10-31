# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class HashFindTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: hashFind
    """
    def main(self):
        """
        Main function
        """
        super(HashFindTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep hashFind",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        hashes = []

        for line in result:
            hash = match(r'The URL: "([^"]+)" returned a response that may contain a "([^"]+)" hash. The hash is: "([^"]+)"', line)

            if hash:
                hash = '%s (%s: %s)' % hash.groups()

                if hash not in hashes:
                    hashes.append(hash)

        if len(hashes):
            return 'Found %i hashes:\n%s' % ( len(hashes), '\n'.join(hashes) )

        return 'No hashes found.'

gtta.execute_task(HashFindTask)
