# -*- coding: utf-8 -*-

from core import Task, execute_task
from smtp_extension_checker import SMTPExtensionChecker

class SMTP_Auth(Task, SMTPExtensionChecker):
    """
    Check SMTP AUTH extension
    """
    TIMEOUT = 60
    EXTENSION = 'AUTH'

    def main(self, *args):
        """
        Main function
        """
        super(SMTP_Auth, self).main()

execute_task(SMTP_Auth)
