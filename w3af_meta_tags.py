# -*- coding: utf-8 -*-

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

gtta.execute_task(MetaTagsTask)
