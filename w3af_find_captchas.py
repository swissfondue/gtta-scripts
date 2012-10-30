# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class FindCaptchasTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: findCaptchas
    """
    def main(self):
        """
        Main function
        """
        super(FindCaptchasTask, self).main()

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

gtta.execute_task(FindCaptchasTask)
