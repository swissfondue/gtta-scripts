# -*- coding: utf-8 -*-

from duckduckgo import DuckDuckGo
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_DuckDuckGo(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = DuckDuckGo

    def _wrapped_target(self):
        """
        Wrapping target
        """
        return "@%s" % self.target

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_DuckDuckGo)
