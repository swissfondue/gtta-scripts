# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import re
from socket import gethostbyname

import gtta
import requests

class CallByIPTask(gtta.Task):
    """
    Calling by IP task
    """
    BODY_FRAGMENT_SIZE = 1000

    def main(self):
        """
        Main function
        """
        if not self.ip:
            try:
                self.ip = gethostbyname(self.host)
            except:
                self._write_result('Host not found: %s' % self.host)
                return

        target = '%s://%s' % (self.proto, self.ip)

        try:
            req = requests.get(target)

        except Exception as e:
            self._write_result('Error opening %s: %s' % ( target, str(e) ))
            return

        if req:
            self._write_result('Status code: %s' % req.status_code)

            if (req.status_code < 400 and req.headers['content-type'].startswith('text/')):
                page = req.text

                # extract title
                self._check_stop()

                try:
                    title = re.search(
                        r'<title>(.*?)</title>',
                        page, re.DOTALL | re.IGNORECASE
                    ).group(1)

                except AttributeError:
                    title = '<none>'

                self._write_result('Title: "%s"' % title)

                # extract part of body
                self._check_stop()

                try:
                    body = re.search(
                        r'<body.*?>(.*)</body>',
                        page, re.DOTALL | re.IGNORECASE
                    ).group(1)

                except AttributeError:
                    body = ''

                self._write_result(
                    'Body:\n%s' % re.sub(
                        r'<.*?>', '', body[:self.BODY_FRAGMENT_SIZE])
                )

gtta.execute_task(CallByIPTask)
