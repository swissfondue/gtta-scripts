# -*- coding: utf-8 -*-

import smtplib
from core import Task

class SMTPExtensionChecker(Task):
    """
    Abstract SMTP extension checker mixin
    """
    EXTENSION = None

    def main(self):
        """
        Main function
        """
        assert self.EXTENSION

        try:
            self._check_stop()
            smtp = smtplib.SMTP(
                host=self.host or self.ip,
                port=25,
                timeout=self.SOCKET_TIMEOUT
            )

            smtp.ehlo()

            if smtp.has_extn(self.EXTENSION):
                self._write_result('Server HAS the %s extension' % self.EXTENSION)

        except:
            self._write_result('Error connecting to SMTP server.')

        if not self.produced_output:
            self._write_result(
                'Server does NOT have the %s extension.' % self.EXTENSION)
