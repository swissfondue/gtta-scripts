# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from smtplib import SMTP
from os import path as os_path, listdir
from core import Task, execute_task
from core.error import NoRecipient, NoAuth, InvalidAuth, NoMailServer

class SMTP_Filter(Task):
    """
    SMTP filter
    """
    DEFAULT_FOLDER = ["Encrypted"]

    def main(self, tls=[], recipient=[], login=[], password=[], sender=[], folder=DEFAULT_FOLDER, *args):
        """
        Main function
        """
        if recipient and recipient[0]:
            recipient = recipient[0]
        else:
            raise NoRecipient('No recipient specified.')

        if tls and tls[0]:
            tls = True
        else:
            tls = False

        if folder and folder[0]:
            folder = folder[0]
        else:
            folder = self.DEFAULT_FOLDER[0]

        folder = os_path.join(os_path.dirname(__file__), "files", folder)

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

        self._check_stop()

        messages_sent = 0

        for file in listdir(folder):
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = recipient
            message['Subject'] = 'SMTP filter test: %s' % file

            message.attach(MIMEText('SMTP filter test.'))

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(os_path.join(folder, file), 'rb').read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
            message.attach(part)

            try:
                smtp = SMTP(self.target, self.port or 25, timeout=self.SMTP_TIMEOUT)
            except Exception:
                self._write_result('Error connecting to SMTP server.')
                return

            try:
                if tls:
                    try:
                        smtp.starttls()
                    except:
                        pass

                smtp.login(login, password)

            except Exception:
                self._write_result('SMTP login failed.')
                return

            try:
                smtp.sendmail(sender, recipient, message.as_string())
            except Exception:
                self._write_result('Error sending e-mail message.')
                return

            smtp.close()

            self._write_result(file)
            messages_sent += 1

        if messages_sent == 0:
            self._write_result('No messages sent.')
        else:
            self._write_result('%i messages sent.' % messages_sent)

        self._check_stop()

        if not self.produced_output:
            self._write_result('No result.')

    def test(self):
        """
        Test function
        """
        self.main(["1"], ["test@gmail.com"], ["smtp.gmail.com"], ["johndoe.123@gmail.com"], ["123"], ["johndoe.123@gmail.com"])

execute_task(SMTP_Filter)
