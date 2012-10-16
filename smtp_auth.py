# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import smtp_utils

class SMTP_Auth(gtta.Task, smtp_utils.SMTPExtensionChecker):
    """
    Check SMTP AUTH extension
    """
    EXTENSION = 'AUTH'

    def main(self):
        """
        Main function
        """
        super(SMTP_Auth, self).main()

gtta.execute_task(SMTP_Auth)
