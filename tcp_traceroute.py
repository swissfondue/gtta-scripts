# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from subprocess import Popen, PIPE, STDOUT
from platform import system
from gtta import Task, execute_task

class TCP_Traceroute(Task):
    """
    Check TCP traceroute port
    """
    MAX_HOPS = 30

    def main(self):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        self._check_stop()

        self._write_result(
            Popen(
                [
                    'tcptraceroute',
                    '-m',
                    str(self.MAX_HOPS),
                    target,
                    str(self.port)
                ],
                stdout = PIPE,
                stderr = STDOUT,
                shell  = False
            ).communicate()[0]
        )

        self._check_stop()

        if not self.produced_output:
            self._write_result('No result.')

execute_task(TCP_Traceroute)
