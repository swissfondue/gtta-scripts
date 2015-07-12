# -*- coding: utf-8 -*-
from yandex import Yandex
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Yandex(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = Yandex

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Email_Yandex)
