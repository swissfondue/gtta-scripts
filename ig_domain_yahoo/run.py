# -*- coding: utf-8 -*-
import re
import whois
from yahoo import YahooParser
from emailgrabber import CommonIGEmailTask
from core import execute_task


class IG_Domain_Yahoo(CommonIGEmailTask):
    """
    Search emails in pages from source
    """
    parser = YahooParser
    results = set()
    headers = {'User-Agent': 'Mozilla/5.0'}
    whois_path = 'http://whois.domaintools.com/'
    domain_re = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$'
    TEST_TIMEOUT = 60 * 60

    def _collect_domains_by_target(self, target):
        """
        Collect domains
        """
        urls = self.parser('site:domaintools.com %s' % target).process()
        return [x.replace(self.whois_path, '') for x in urls]

    def main(self, *args):
        """
        Main function
        """
        if self.ip:
            return

        self.results.update(self._collect_domains_by_target(self.target))

        if re.match(self.domain_re, self.target):
            domain = whois.whois(self.target)
            self.results.update(self._collect_domains_by_target(domain.name))
            map(lambda x: self.results.update(self._collect_domains_by_target(x)), domain.emails)
            self.results.update(self._collect_domains_by_target(
                self.target.replace('.' + self.target.split('.')[-1], '')))

        self._write_result('\n'.join(
            filter(lambda x: re.match(self.domain_re, x), self.results)))

    def test(self):
        """
        Test function
        """
        self.target = "clariant.com"
        self.main()

execute_task(IG_Domain_Yahoo)
