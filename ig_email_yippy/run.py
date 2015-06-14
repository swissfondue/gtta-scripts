# -*- coding: utf-8 -*-
from yippy import Yippy
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Yippy(CommonIGEmailTask):
    """
    Search emails in pages
    """
    parser = Yippy

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Yippy)
