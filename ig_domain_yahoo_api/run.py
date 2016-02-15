# -*- coding: utf-8 -*-
from yahoo_api import YahooAPI
from emailgrabber.domain import CommonIGDomainToolsTask
from core import execute_task


class IG_Domain_YahooAPI(CommonIGDomainToolsTask):
    """
    Search emails in pages from source
    """
    parser = YahooAPI

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
        self.main(
            ['dj0yJmk9SnhqbG5CR3IyRFVXJmQ9WVdrOWMyMTRlVlEzTjJNbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD00Mw--'],
            ['0239d730f5c6bf89233a185f6c7794829ba7947a']
        )

execute_task(IG_Domain_YahooAPI)
