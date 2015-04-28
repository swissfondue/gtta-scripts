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
    WHOIS_PATH = 'http://whois.domaintools.com/'
    DOMAIN_RE = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$'
    TEST_TIMEOUT = 60 * 60

    def _collect_domains_by_target(self, target):
        """
        Collect domains
        """
        urls = self.parser('site:whois.domaintools.com %s' % target).process(self.params)
        map(lambda x: self.results.add(x.replace(self.WHOIS_PATH, '')), urls)

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

        if re.match(self.DOMAIN_RE, self.target):
            self._search_by_domain()

    def _search_by_domain(self):
        """
        Search by self.target if it's domain
        """
        # get name and emails
        domain = whois.whois(self.target)

        # search by name
        self._collect_domains_by_target('"%s"' % domain.name)

        # search by emails
        unique_emails = set()

        for email in domain.emails:
            unique_emails.add(email.lower())

        map(lambda x: self._collect_domains_by_target(x), unique_emails)

        # search by domain without TLD
        self._collect_domains_by_target(self.target[:self.target.rindex(".")])

    def _output_result(self):
        """
        Output result
        """
        self._write_result('\n'.join(filter(lambda x: re.match(self.DOMAIN_RE, x), self.results)))

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
