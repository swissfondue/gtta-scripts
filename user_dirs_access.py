# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import urllib
from gtta import Task, execute_task

class AccessUserDirsTask(Task):
    """
    Check access to user directory
    """
    def main(self, usernames):
        """
        Main function
        """
        target = '%s://%s' % (
            self.proto or 'http',
            self.host or self.ip
        )

        username = (usernames + [''])[0] or 'root'

        self._check_stop()

        try:
            res = urllib.urlopen("%s/~%s" % (target, username))

            if res.code == 403:
                msg = 'User "%s": user directory is accessible'
            else:
                msg = 'User "%s": user directory is NOT accessible'

            msg = msg % username

        except IOError:
            msg = "Connection error"

        self._write_result(msg)

execute_task(AccessUserDirsTask)
