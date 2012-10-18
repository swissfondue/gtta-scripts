# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from smtplib import SMTP
from gtta import Task, execute_task

class SMTP_User_Verification(Task):
    """
    SMTP filter
    """
    TIMEOUT = 60

    def main(self, vrfy_users=[], src=[], dst=[]):
        """
        Main function
        """
        target = self.host or self.ip

        if not vrfy_users and self.host:
            vrfy_users += [ 'nonexistent@%s' % self.host, 'postmaster%s' % self.host ]

        if not src:
            src += [ 'source@gmail.com' ]

        if not dst and self.host:
            dst += [ 'nonexistent@%s' % self.host ]

        self._check_stop()

        try:
            smtp = SMTP(target, 25, timeout=self.SMTP_TIMEOUT)
            smtp.ehlo()

        except Exception:
            self._write_result('Error connecting to SMTP server.')
            return

        # VRFY checks
        if vrfy_users:
            for email in vrfy_users:
                self._check_stop()

                if len(email) < 6:
                    continue

                try:
                    reply = smtp.verify(email)
                    self._write_result('VRFY %s\n%s' % ( email, ' '.join(map(str, reply)) ))

                except Exception as e:
                    self._write_result('VRFY %s\nError (%s)' % ( email, str(e) ))

                self._write_result(' ')

        # send mail test
        if src and dst:
            try:
                smtp.send('MAIL FROM:<%s>\n' % src[0])
                reply = smtp.getreply()

                self._write_result('MAIL FROM:<%s>' % src[0])
                self._write_result(' '.join(map(str, reply)))
                self._write_result(' ')

                if reply[0] == 250:
                    smtp.send('RCPT TO:<%s>\n' % dst[0])
                    reply = smtp.getreply()

                    self._write_result('RCPT TO:<%s>' % dst[0])
                    self._write_result(' '.join(map(str, reply)))
                    self._write_result(' ')

            except Exception as e:
                self._write_result(str(e))

        self._check_stop()

        if not self.produced_output:
            self._write_result('No result.')

execute_task(SMTP_User_Verification)
