# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import smtp_utils

class SMTP_StartTLS(gtta.Task, smtp_utils.SMTPExtensionChecker):
    """
    Check SMTP STARTTLS extension
    """
    EXTENSION = 'STARTTLS'

    def main(self):
        """
        Main function
        """
        super(SMTP_StartTLS, self).main()

gtta.execute_task(SMTP_StartTLS)
