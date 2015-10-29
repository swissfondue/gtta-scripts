# -*- coding: utf-8 -*-
from bing import Bing
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Bing(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Bing

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Bing)
