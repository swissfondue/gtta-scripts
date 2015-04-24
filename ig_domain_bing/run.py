# -*- coding: utf-8 -*-
from bing import BingParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Domain_Bing(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = BingParser

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Domain_Bing)
