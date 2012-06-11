# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from smtplib import SMTP
from os import path as os_path, listdir
from gtta import Task, execute_task
from gtta.error import NoRecipient, NoAuth, InvalidAuth, NoMailServer

class SMTP_Filter(Task):
    """
    SMTP filter
    """
    DEFAULT_FOLDER = [ os_path.join(os_path.dirname(__file__), 'smtp_filter_files') ]

    def main(self, recipient=[], server=[], login=[], password=[], sender=[], folder=DEFAULT_FOLDER):
        """
        Main function
        """
        target = None

        if server and server[0]:
            target = server[0]

        if not target:
            raise NoMailServer('No mail server specified.')

        if recipient and recipient[0]:
            recipient = recipient[0]
        else:
            raise NoRecipient('No recipient specified.')

        if folder and folder[0]:
            folder = folder[0]
        else:
            folder = self.DEFAULT_FOLDER[0]

        if not login or not login[0]:
            raise NoAuth('No login specified.')

        login = login[0]

        if not password or not password[0]:
            raise InvalidAuth('No password specified.')

        password = password[0]

        if not sender or not sender[0]:
            sender = login
        else:
            sender = sender[0]

        output = []

        self._check_stop()

        messages_sent = 0

        for file in listdir(folder):
            message = MIMEMultipart()
            message['From']    = sender
            message['To']      = recipient
            message['Subject'] = 'SMTP filter test: %s' % file

            message.attach(MIMEText('SMTP filter test.'))

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(os_path.join(folder, file), 'rb').read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
            message.attach(part)

            try:
                smtp = SMTP(target, 25, timeout=self.SMTP_TIMEOUT)
            except Exception:
                return 'Error connecting to SMTP server.'

            try:
                smtp.login(login, password)
            except Exception:
                return 'SMTP login failed.'

            try:
                smtp.sendmail(sender, recipient, message.as_string())
            except Exception:
                return 'Error sending email message.'

            smtp.close()

            output.append(file)
            messages_sent += 1

        if messages_sent == 0:
            output.append('No messages sent.')
        else:
            output.append('%i messages sent.' % messages_sent)

        self._check_stop()

        if len(output) > 0:
            return '\n'.join(output)

        return 'No result.'

execute_task(SMTP_Filter)
