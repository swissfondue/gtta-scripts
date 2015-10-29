# -*- coding: utf-8 -*-
from google import Google
from emailgrabber.domain import CommonIGDomainToolsTask
from core import execute_task


class IG_Domain_Google(CommonIGDomainToolsTask):
    """
    Search emails in pages from source
    """
    parser = Google

    def _search_by_ip(self):
        """
        Search by self.ip
        """
        pass

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Domain_Google)
