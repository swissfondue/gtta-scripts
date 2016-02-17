# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT
from core import Task, execute_task

class Nikto(Task):
    """
    Nikto scanner
    """
    def main(self, *args):
        """
        Main function
        """
        self._check_stop()

        task = Popen(
            ["perl", "nikto.pl", self.target, self.proto or "http", str(self.port or "80")],
            stdout=PIPE, stderr=STDOUT, shell=False
        )

        for line in iter(task.stdout.readline, ""):
            self._check_stop()
            self._write_result(line.rstrip())

        if not self.produced_output:
            self._write_result("No result.")

    def test(self):
        """
        Test function
        """
        self.port = "80"
        self.proto = "http"
        self.target = "gtta.demo.stellarbit.com"
        self.main()

execute_task(Nikto)
