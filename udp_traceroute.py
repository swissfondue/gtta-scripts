# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import call
import gtta

class TracerouteTask(gtta.Task):
    """
    traceroute launcher
    """
    def main(self):
        """
        Main function
        """
        target = self.host or self.ip

        self._check_stop()
        called_ok, output = call.call(["traceroute", target])

        self._check_stop()

        if not called_ok:
            self._write_result('Traceroute launching error!')
        else:
            if output.find('Cannot handle "host"') >= 0:
                self._write_result('Host not found: %s' % target)
            else:
                self._write_result(output)

gtta.execute_task(TracerouteTask)
