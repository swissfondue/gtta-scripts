# -*- coding: utf-8 -*-
from yahoo import Yahoo
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Yahoo(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Yahoo

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Yahoo)
