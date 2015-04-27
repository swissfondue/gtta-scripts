# -*- coding: utf-8 -*-
from bing_api import BingAPIParser
from emailgrabber.domain import CommonIGDomainToolsTask
from core import execute_task


class IG_Domain_BingAPI(CommonIGDomainToolsTask):
    """
    Search emails in pages from source
    """
    parser = BingAPIParser

    def _wrap_target(self, target):
        """
        Wrap target
        """
        return "'%s'" % target

    def test(self):
        """
        Test function
        """
        self.target = 'clariant.com'
        self.main(['aPosOzbRqf1/1/tXtoHug3VSXJYKC9YQHTnsip+cq34='])

execute_task(IG_Domain_BingAPI)
