# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from vulndetector import detect
from gtta import Task, execute_task

class Web_SQL_XSS(Task):
    """
    Web SQL/XSS vulnerability scanner
    """
    TIMEOUT           = 60 * 60 # 1 hour
    DEFAULT_PAGETYPE  = 'php'
    DEFAULT_URL_LIMIT = 100

    def main(self, url=[], domains=[], pagetype=[ DEFAULT_PAGETYPE ], cookies=[], url_limit=[ DEFAULT_URL_LIMIT ]):
        """
        Main function
        """
        target = self.host

        if url and url[0]:
            target = url[0]

        if not target:
            target = self.ip

        if not target.startswith('http'):
            target = 'http://%s/' % target

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

        results = []

        self._check_stop()

        results = detect(target, domains, pagetype, cookies, url_limit, self._check_stop, self.HTTP_TIMEOUT)

        self._check_stop()

        if len(results) > 0:
            return '\n'.join(results)

        return 'No result.'

execute_task(Web_SQL_XSS)
