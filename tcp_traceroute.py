# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from subprocess import check_output, STDOUT
from platform import system
from gtta import Task, execute_task

class TCP_Traceroute(Task):
    """
    Check TCP traceroute port
    """
    MAX_HOPS = 30
    TIMEOUT  = 120

    def main(self):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        output = []

        self._check_stop()

        if system() == 'Windows':
            output.append(check_output([ 'tracetcp.exe', '%s:%i' % ( target, self.port ), '-m', str(self.MAX_HOPS) ], stderr=STDOUT))
        else:
            output.append(check_output([ 'tcptraceroute', '-m', str(self.MAX_HOPS), target, str(self.port) ], stderr=STDOUT))

        self._check_stop()

        if len(output) > 0:
            return '\n'.join(output).replace('\r', '')

        return 'No result.'

execute_task(TCP_Traceroute)
