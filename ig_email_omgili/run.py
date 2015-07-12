# -*- coding: utf-8 -*-
from omgili import Omgili
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Omgili(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Omgili

    def test(self):
        """
        Test function
        """
        self.target = "microsoft.com"
        self.main()

execute_task(IG_Email_Omgili)
