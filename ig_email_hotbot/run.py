# -*- coding: utf-8 -*-
from hotbot import HotbotParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Hotbot(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = HotbotParser

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Hotbot)
