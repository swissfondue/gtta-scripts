# -*- coding: utf-8 -*-

from re import match
from core import Task, execute_task
from w3af import W3AFScriptLauncher

class RIAEnumeratorTask(Task, W3AFScriptLauncher):
    """
    GTTA task:
        w3af: ria_enumerator
    """
    def main(self, *args):
        """
        Main function
        """
        super(RIAEnumeratorTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery ria_enumerator",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        gears = []
        flash = []

        for line in result:
            url = match(r'A gears manifest file was found at: "([^"]+)"', line)

            if url and not url.groups()[0] in gears:
                gears.append(url.groups()[0])

            url = match(r'The "[^"]+" file at "([^"]+)" allows flash/silverlight access from any site', line)

            if url:
                url = '%s (allows access from any site)' % url.groups()[0]

                if url not in flash:
                    flash.append(url)

            url = match(r'The "[^"]+" file at "([^"]+)" allows access from: "([^"]+)"', line)

            if url:
                url = '%s (allows access from %s)' % url.groups()

                if url not in flash:
                    flash.append(url)

        msg = []

        if len(gears):
            msg.append('Found %i Google Gears manifest files:\n%s' % ( len(gears), '\n'.join(gears) ))

        if len(flash):
            msg.append('Found %i Flash/Silverlight policy files:\n%s' % ( len(flash), '\n'.join(flash) ))

        if msg:
            return '\n\n'.join(msg)

        return 'No Google Gears manifest files or Flash/Silverlight policy files found.'

execute_task(RIAEnumeratorTask)
