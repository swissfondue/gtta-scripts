# -*- coding: utf-8 -*-
from lexxe import Lexxe
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Lexxe(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Lexxe

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Lexxe)
