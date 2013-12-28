# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class FormAutocompleteTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: formAutocomplete
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "grep formAutocomplete",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        forms = []

        for line in result:
            form = match(r'The URL: "([^"]+)" has <form> element with autocomplete capabilities.', line)

            if form and not form.groups()[0] in forms:
                forms.append(form.groups()[0])

        if len(forms):
            return 'Found %i forms with autocomplete capability:\n%s' % ( len(forms), '\n'.join(forms) )

        return 'No forms with autocomplete capability found.'

execute_task(FormAutocompleteTask)
