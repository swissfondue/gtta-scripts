# -*- coding: utf-8 -*-

import os
import tempfile
from core import call

SCRIPT_TEMPLATE = '''target
set target {target}
back
http-settings
set timeout {timeout}
back
{script}
start
exit
'''

_W3AF_CMD = os.path.join(os.path.dirname(__file__), "w3af", "w3af_console")


def call_w3af(target, commands, timeout=15):
    """
    Call w2af_console with a defined command sequence
    Result: (success: boolean, data: unicode)
    """
    script = SCRIPT_TEMPLATE.format(
        target=target,
        timeout=timeout,
        script='\n'.join(commands),
    )

    with tempfile.NamedTemporaryFile() as tmpf:
        tmpf.write(script)
        tmpf.file.flush()
        return call.call(["python", _W3AF_CMD, "-s", tmpf.name])


class W3AFScriptLauncher(object):
    """
    Abstract w3af-script launching mixin
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return ["help"]

    def _filter_result(self, result):
        """
        Filter w3af result
        """
        return '\n'.join(result)

    def main(self):
        """
        Main function
        """
        target = self.host or self.ip
        protocol = self.proto or 'http'

        self._check_stop()
        called_ok, output = call_w3af(
            target='%s://%s' % (protocol, target),
            timeout=self.SOCKET_TIMEOUT,
            commands=self._get_commands()
        )

        self._check_stop()

        if not called_ok:
            self._write_result('w3af_console launching error!')

        else:
            data = iter(output.split('\r\n'))

            self._check_stop()

            # collecting of the script errors
            param_errors = []

            for line in data:
                if line.startswith('w3af>>> exit'):
                    param_errors.append('Unexpected end of script')
                    break

                if line.startswith('w3af>>> start'):
                    break

                if not line.startswith('w3af'):
                    param_errors.append(line)

            else:
                param_errors.append('Unexpected end of script')

            if param_errors:
                self._write_result('w3af configuration errors:\n')
                self._write_result('\n'.join(param_errors))
                return

            self._check_stop()

            result = []

            # collecting the w3af output
            for line in data:
                if line.startswith('w3af>>> exit'):
                    break

                result.append(line)

            self._write_result(self._filter_result(result))
