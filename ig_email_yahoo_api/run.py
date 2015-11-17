# -*- coding: utf-8 -*-
from yahoo_api import YahooAPI
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Email_YahooAPI(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = YahooAPI

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main(
            ['dj0yJmk9SnhqbG5CR3IyRFVXJmQ9WVdrOWMyMTRlVlEzTjJNbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD00Mw--'],
            ['0239d730f5c6bf89233a185f6c7794829ba7947a']
        )

execute_task(IG_Email_YahooAPI)
