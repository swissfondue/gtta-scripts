# -*- coding: utf-8 -*-
import re
import whois
from core import Task


class CommonIGDomainToolsTask(Task):
    """
    Common abstract class for ig_domain tasks
    """
    parser = None
    params = None
    results = set()
    whois_path = 'http://whois.domaintools.com/'
    domain_re = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$'
    TEST_TIMEOUT = 60 * 60

    def _collect_domains_by_target(self, target):
        """
        Collect domains
        """
        urls = self.parser('site:domaintools.com %s' % target).process(self.params)
        map(lambda x: self.results.add(x.replace(self.whois_path, '')), urls)

    def _search_by_ip(self):
        """
        Search by self.ip
        """
        pass

    def _search_by_target(self):
        """
        Search by self.target
        """
        self._collect_domains_by_target(self.target)

        if re.match(self.domain_re, self.target):
            self._search_by_domain()

    def _search_by_domain(self):
        """
        Search by self.target if it's domain
        """
        # get name and emails
        domain = whois.whois(self.target)

        # search by name
        if hasattr(domain, 'name'):
            self._collect_domains_by_target('"%s"' % domain.name)

        # search by emails
        if hasattr(domain, 'emails'):
            map(lambda x: self._collect_domains_by_target(x), domain.emails)

        # search by domain without TLD
        self._collect_domains_by_target(
            self.target.replace('.' + self.target.split('.')[-1], ''))

    def _output_result(self):
        """
        Output result
        """
        self._write_result('\n'.join(
            filter(lambda x: re.match(self.domain_re, x), self.results)))

    def main(self, *args):
        """
        Main function
        """
        if not self.parser:
            self._write_result('It requires a "self.parser".')
            return

        self.params = args

        if self.ip:
            self._search_by_ip()
        else:
            self._search_by_target()

        self._output_result()
