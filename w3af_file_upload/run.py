# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class FileUploadTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: fileUpload
    """
    def main(self, *args):
        """
        Main function
        """
        super(FileUploadTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep fileUpload",
            "discovery webSpider",
            "back",
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        urls = []

        for line in result:
            url = match(r'The URL: "([^"]+)" has form with file upload capabilities', line)

            if url and not url.groups()[0] in urls:
                urls.append(url.groups()[0])

        if len(urls):
            return 'Found %i URLs with file upload forms:\n%s' % ( len(urls), '\n'.join(urls) )

        return 'No URLs with file upload forms found.'

execute_task(FileUploadTask)
