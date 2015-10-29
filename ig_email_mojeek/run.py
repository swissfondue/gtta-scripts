# -*- coding: utf-8 -*-
from mojeek import Mojeek
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Mojeek(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Mojeek

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Mojeek)
