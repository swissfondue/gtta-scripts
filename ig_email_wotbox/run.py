# -*- coding: utf-8 -*-
from wotbox import WotboxParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Wotbox(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = WotboxParser

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Wotbox)
