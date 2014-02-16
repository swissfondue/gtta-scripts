# coding: utf-8

from subprocess import Popen, PIPE, STDOUT
from core import Task, execute_task
from core.error import NotEnoughArguments


class ShellTask(Task):
    """
    Shell task
    """
    def _call_external(self, command):
        """
        Call external program
        """
        if command:
            command = command[0]

        command = command.replace("@target", self.target)
        process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
        out = process.communicate()[0]

        if out:
            self._write_result(out)

        if process.returncode != 0:
            raise ValueError("Command calling error: %s." % command)

    def main(self, *args):
        """
        Main function
        """
        if not args:
            raise NotEnoughArguments("Shell command should be specified.")

        try:
            self._call_external(args[0])
        except ValueError as err:
            self._write_result(unicode(err))

    def test(self):
        """
        Test function
        """
        self.target = "google.com"
        self.main(["/bin/ping -c 3 @target"])

execute_task(ShellTask)
