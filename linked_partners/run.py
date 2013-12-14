# -*- coding: utf-8 -*-

from core import Task, execute_task, crawler

class ExternalLinksTask(Task):
    """
    External links collector
    """
    def __init__(self):
        """
        Constructor
        """
        super(ExternalLinksTask, self).__init__()
        self.links = []

    def _write_link(self, link):
        """
        Write a link
        """
        if link not in self.links:
            self._write_result(link)
            self.links.append(link)

    def main(self, *args):
        """
        Main function
        """
        cr = crawler.LinkCrawler()
        cr.ext_link_callback = self._write_link
        cr.stop_callback = self._check_stop

        target = '%s://%s' % (
            self.proto or 'http',
            self.host or self.ip
        )

        try:
            cr.process(target)

            if not self.produced_output:
                self._write_result('No external links.')

        except Exception as e:
            self._write_result('Error opening %s: %s' % ( target, str(e) ))

execute_task(ExternalLinksTask)
