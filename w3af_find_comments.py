# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FindCommentsTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: findComments
    """
    def main(self):
        """
        Main function
        """
        super(FindCommentsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep findComments",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        comments = []

        for line in result:
            comment = match(r'A comment with the string "(.+?)" was found in: "([^"]+)".', line)

            if comment:
                comment = '%s (%s)' % ( comment.groups()[1], comment.groups()[0] )

                if comment not in comments:
                    comments.append(comment)

        if len(comments):
            return 'Found %i URLs with interesting comments:\n%s' % ( len(comments), '\n'.join(comments) )

        return 'No URLs with interesting comments found.'

gtta.execute_task(FindCommentsTask)
