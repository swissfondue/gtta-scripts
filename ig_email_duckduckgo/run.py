# -*- coding: utf-8 -*-
from duckduckgo import DuckDuckGo
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_DuckDuckGo(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = DuckDuckGo

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_DuckDuckGo)
