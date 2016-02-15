# -*- coding: utf-8 -*-
from bing import Bing
from emailgrabber.domain import CommonIGDomainToolsTask
from core import execute_task


class IG_Domain_Bing(CommonIGDomainToolsTask):
    """
    Search emails in pages from source
    """
    parser = Bing

    def test(self):
        """
        Test function
        """
        self.target = "microsoft.com"
        self.main()

execute_task(IG_Domain_Bing)
