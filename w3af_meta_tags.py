# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class MetaTagsTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: metaTags
    """
    def main(self):
        """
        Main function
        """
        super(MetaTagsTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep metaTags",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        tags = []

        for line in result:
            tag = match(r'The URI: "([^"]+)" sent a META tag with attribute \S+ "([^"]+)" which looks interesting.', line)

            if tag:
                tag = '%s (%s)' % tag.groups()

                if tag not in tags:
                    tags.append(tag)

        if len(tags):
            return 'Found %i interesting meta tags:\n%s' % ( len(tags), '\n'.join(tags) )

        return 'No interesting meta tags found.'

gtta.execute_task(MetaTagsTask)
