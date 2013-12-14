# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class AjaxTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: ajax
    """
    def main(self, *args):
        """
        Main function
        """
        super(AjaxTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep ajax",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        ajax_urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" has an AJAX code', line)

            if url and not url.groups()[0] in ajax_urls:
                ajax_urls.append(url.groups()[0])

        if len(ajax_urls):
            return 'Found %i URLs containing AJAX code:\n%s' % ( len(ajax_urls), '\n'.join(ajax_urls) )

        return 'No AJAX code found.'

execute_task(AjaxTask)
