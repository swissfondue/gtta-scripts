# -*- coding: utf-8 -*-
from lixam import Lixam
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Lixam(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Lixam

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Lixam)
