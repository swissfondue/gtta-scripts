# coding: utf-8

from core import Task, execute_task, call
import os

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
        cmd = os.path.join(self._get_library_path("harvester"), "theHarvester_email.py")

        ok, output = call.call([
            "python",
            cmd,
            '-b',
            'all',
            '-d',
            self.host
        ])

        if ok:
            self._write_result(output)
        else:
            self._write_result('ERROR CALLING theHarvester script')

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(TheHarvesterEmailsTask)
