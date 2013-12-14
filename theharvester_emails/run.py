# coding: utf-8

from core import Task, execute_task, call
import os

HARVESTER_CMD = os.path.join(os.path.dirname(__file__), "..", "lib", "harvester", "theHarvester_email.py")

class TheHarvesterEmailsTask(Task):
    """
    Get all emails from theHarvester script
    """
    TIMEOUT = 60

    def main(self, *args, **kwargs):
        """
        Main function
        @param args:
        @param kwargs:
        @return:
        """
        ok, output = call.call([
            "python",
            HARVESTER_CMD,
            '-b',
            'all',
            '-d',
            self.host
        ])

        if ok:
            self._write_result(output)
        else:
            self._write_result('ERROR CALLING theHarvester script')

execute_task(TheHarvesterEmailsTask)
