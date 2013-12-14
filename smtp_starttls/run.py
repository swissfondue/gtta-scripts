# -*- coding: utf-8 -*-

from core import Task, execute_task
from smtp import SMTPExtensionChecker

class SMTP_StartTLS(Task, SMTPExtensionChecker):
    """
    Check SMTP STARTTLS extension
    """
    TIMEOUT = 60
    EXTENSION = 'STARTTLS'

    def main(self, *args):
        """
        Main function
        """
        super(SMTP_StartTLS, self).main()

execute_task(SMTP_StartTLS)
