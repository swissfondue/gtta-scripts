# -*- coding: utf-8 -*-
from bing import BingParser
from emailgrabber.domain import CommonIGDomainToolsTask
from core import execute_task


class IG_Domain_Bing(CommonIGDomainToolsTask):
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
        self.target = self.ip = "83.150.1.145"
        self.main()

execute_task(IG_Domain_Bing)
