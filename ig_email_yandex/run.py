# -*- coding: utf-8 -*-
from yandex import YandexParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_Yandex(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = YandexParser

    def test(self):
        """
        Test function
        """
        self.target = "teremok-finance.ru"
        self.main()

execute_task(IG_Email_Yandex)
