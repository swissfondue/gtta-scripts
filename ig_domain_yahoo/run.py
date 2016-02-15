# -*- coding: utf-8 -*-
from yahoo import Yahoo
from emailgrabber.domain import CommonIGDomainToolsTask
from core import execute_task


class IG_Domain_Yahoo(CommonIGDomainToolsTask):
    """
    Search emails in pages from source
    """
    parser = Yahoo

    def _search_by_ip(self):
        """
        Search by self.ip
        """
        pass

    def test(self):
        """
        Test function
        """
        self.target = "netprotect"
        self.main()

execute_task(IG_Domain_Yahoo)
