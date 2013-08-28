# -*- coding: utf-8 -*-
"""
Get all emails from theHarvester script
"""

import socket
import sys
sys.path.append('pythonlib')
from gtta import Task, execute_task
import call

class TheHarvesterEmailsTask(Task):
    TIMEOUT=60
    def main(self,*args,**kwargs):
        ok, output = call.call(['python',
            '/opt/gtta/scripts/theHarvest-2.2a/theHarvester_email.py',
            '-b','all','-d',self.host])
        if ok:
            self._write_result(output)
        else:
            self._write_result('ERROR CALLING theHarvester script')

execute_task(TheHarvesterEmailsTask)
