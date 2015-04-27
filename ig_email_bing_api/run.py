# -*- coding: utf-8 -*-
from bing_api import BingAPIParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_BingAPI(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = BingAPIParser

    def _wrapped_target(self):
        """
        Wrapping target
        """
        return "'@%s'" % self.target

    def test(self):
        """
        Test function
        """
        self.target = 'clariant.com'
        self.main(['aPosOzbRqf1/1/tXtoHug3VSXJYKC9YQHTnsip+cq34='])

execute_task(IG_Email_BingAPI)
