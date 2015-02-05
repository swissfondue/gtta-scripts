# -*- coding: utf-8 -*-

from core import execute_task
from smtp_extension_checker import SMTPExtensionChecker

class SMTP_StartTLS(SMTPExtensionChecker):
    """
    Check SMTP STARTTLS extension
    """
    EXTENSION = 'STARTTLS'

    def test(self):
        """
        Test function
        """
        self.host = "smtp.gmail.com"
        self.main()

execute_task(SMTP_StartTLS)
