# -*- coding: utf-8 -*-

from re import match
from sys import path
path.append('pythonlib')

import gtta
import w3af_utils

class ZoneHTask(gtta.Task, w3af_utils.W3AFScriptLauncher):
    """
    GTTA task:
        w3af: zone_h
    """
    def main(self):
        """
        Main function
        """
        super(ZoneHTask, self).main()

    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return [
            "plugins",
            "discovery zone_h",
            "back"
        ]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        output = []

        for line in result:
            out_line = match(r'The target site was defaced more than one time in the past. For more information please visit the following URL: "([^"]+)"', line)

            if out_line:
                out_line = 'The target was defaced more than one time. Please see %s for more info.' % out_line.groups()[0]

                if out_line not in output:
                    output.append(out_line)

            out_line = match(r'The target site was defaced in the past. For more information please visit the following URL: "([^"]+)"', line)

            if out_line:
                out_line = 'The target was defaced in the past. Please see %s for more info.' % out_line.groups()[0]

                if out_line not in output:
                    output.append(out_line)

        if len(output):
            return '\n'.join(output)

        return 'The target is not listed in the Zone-H database.'

gtta.execute_task(ZoneHTask)
