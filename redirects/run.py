# -*- coding: utf-8 -*-

from core import Task, execute_task, crawler


class RedirectsTask(Task):
    """
    URL-redirects collector
    """
    PATTERNS = ( 
        'www.', 
        'http://', 
        'https://', 
        'target',
        'url', 
        'redirect', 
        'site', 
        'website', 
        'redir', 
        'go', 
        'jump' 
    )

    def __init__(self):
        """
        Constructor
        """
        super(RedirectsTask, self).__init__()
        self.redirects = []

    def _write_redirect(self, link):
        """
        Write a redirect 
        """
        orig_link = link

        if link[:5] == 'https':
            link = link[8:]
        elif link[:5] == 'http:':
            link = link[7:]

        if link.find('/') == -1:
            return True

        link = link[link.find('/'):].lower()
        found = False

        for pattern in self.PATTERNS:
            if pattern in link:
                found = True
                break

        if not found:
            return True

        if link not in self.redirects:
            self._write_result(orig_link)
            self.redirects.append(link)

        return True
    
    def main(self, *args):
        """
        Main function
        """
        cr = crawler.LinkCrawler()
        cr.redirect_callback = self._write_redirect
        cr.stop_callback = self._check_stop

        target = '%s://%s' % (
            self.proto or 'http',
            self.host or self.ip
        )

        try:
            cr.process(target)

            if not self.produced_output:
                self._write_result('No redirects found.')

        except Exception as e:
            self._write_result('Error opening %s: %s' % ( target, str(e) ))

    def test(self):
        """
        Test function
        """
        self.proto = "http"
        self.host = "google.com"
        self.main()

execute_task(RedirectsTask)
