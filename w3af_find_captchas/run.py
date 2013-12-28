# -*- coding: utf-8 -*-

from re import match
from core import execute_task
from w3af import W3AFScriptLauncher

class FindCaptchasTask(W3AFScriptLauncher):
    """
    GTTA task:
        w3af: findCaptchas
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery findCaptchas",
            "discovery webSpider",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        captchas = []

        for line in result:
            captcha = match(r'Found a CAPTCHA image at: "([^"]+)".', line)

            if captcha and not captcha.groups()[0] in captchas:
                captchas.append(captcha.groups()[0])

        if len(captchas):
            return 'Found %i CAPTCHAs:\n%s' % ( len(captchas), '\n'.join(captchas) )

        return 'No CAPTCHAs found.'

execute_task(FindCaptchasTask)
