# -*- coding: utf-8 -*-
from exalead import Exalead
from core import execute_task
from emailgrabber import CommonIGEmailTask


class IG_Email_Exalead(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Exalead

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Exalead)
