# -*- coding: utf-8 -*-

from core import execute_task
from smtp_extension_checker import SMTPExtensionChecker

class SMTP_Auth(SMTPExtensionChecker):
    """
    Check SMTP AUTH extension
    """
    EXTENSION = 'AUTH'

    def test(self):
        """
        Test function
        """
        self.host = "smtp.gmail.com"
        self.main()

execute_task(SMTP_Auth)
