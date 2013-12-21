# -*- coding: utf-8 -*-

from core import Task, execute_task
from sslyze import SSLyzeLauncher

class RenegotiationTask(Task, SSLyzeLauncher):
    """
    Renegotiation checker
    """
    TIMEOUT = 60

    def main(self, *args):
        """
        Main function
        """
        super(RenegotiationTask, self).main()

    def _get_commands(self):
        """
        Returns the list of sslyze options
        """
        return [
            "--reneg",
        ]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        result = []

        for line in data.split('\n'):
            if ' Renegotiation' in line:
                result.append(line.strip())

        return '\n'.join(result)

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(RenegotiationTask)
