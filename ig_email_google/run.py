# -*- coding: utf-8 -*-
from google import GoogleParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Google(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = GoogleParser

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Google)
