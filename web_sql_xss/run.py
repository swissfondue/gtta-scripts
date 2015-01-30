# -*- coding: utf-8 -*-

from vulndetector import detect
from core import Task, execute_task


class Web_SQL_XSS(Task):
    """
    Web SQL/XSS vulnerability scanner
    """
    DEFAULT_PAGETYPE  = 'php'
    DEFAULT_URL_LIMIT = 100

    def main(self, domains=[], pagetype=[ DEFAULT_PAGETYPE ], cookies=[], url_limit=[ DEFAULT_URL_LIMIT ], *args):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        target = '%s://%s' % (
            self.proto or 'http',
            self.host or self.ip
        )

        if not target.startswith('http'):
            target = '%s://%s' % (self.proto or 'http', target)

        if not domains or not domains[0]:
            domain = None

            if target.startswith('https://'):
                domain = target[8:]

            if target.startswith('http://'):
                domain = target[7:]

            if domain.find('/') != -1:
                domain = domain[:domain.find('/')]

            domains = [ domain ]

        if pagetype and pagetype[0] in ( 'php', 'asp' ):
            pagetype = pagetype[0]
        else:
            pagetype = self.DEFAULT_PAGETYPE

        if cookies and cookies[0]:
            cookies = cookies[0]
        else:
            cookies = ''

        if url_limit and url_limit[0]:
            url_limit = int(url_limit[0])
        else:
            url_limit = self.DEFAULT_URL_LIMIT

        self._check_stop()

        results = detect(target, domains, pagetype, cookies, url_limit, self._check_stop, self.HTTP_TIMEOUT)

        self._check_stop()

        if len(results) > 0:
            self._write_result('\n'.join(results))

        if not self.produced_output:
            self._write_result('No result.')

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(Web_SQL_XSS)
