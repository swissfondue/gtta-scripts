# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import sslyze_tools

class RenegotiationTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    Renegotiation checker
    """
    def main(self):
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

gtta.execute_task(RenegotiationTask)
