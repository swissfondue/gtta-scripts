# -*- coding: utf-8 -*-
from exalead import ExaleadParser
from core import execute_task
from emailgrabber import CommonIGEmailTask


class IG_Email_Exalead(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = ExaleadParser

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Exalead)
