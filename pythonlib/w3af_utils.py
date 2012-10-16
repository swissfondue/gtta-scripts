# -*- coding: utf-8 -*-
"""
w3af communication utils
"""

import os
import tempfile
import call

SCRIPT_TEMPLATE = '''target
set target {target}
back
http-settings
set timeout {timeout}
back
plugins
output !console textFile
output config textFile
set httpFileName /dev/null
set verbose False
set fileName {file_name}
back
back
{script}
start
exit
'''

W3AF_CMD = os.path.join(
    os.path.dirname(__file__), "w3af", "w3af_console")

def call_w3af(target, commands, output_file, timeout=15):
    """
    Call w2af_console with a defined command sequence
    Result: (success: boolean, data: unicode)
    """
    script = SCRIPT_TEMPLATE.format(
        target = target,
        timeout = timeout,
        script = '\n'.join(commands),
        file_name = output_file
    )

    with tempfile.NamedTemporaryFile() as tmpf:
        tmpf.write(script)
        tmpf.file.flush()
        
        called_ok, output = call.call([ W3AF_CMD, "-s", tmpf.name ])

        return called_ok, output, open(output_file).read()

class W3AFScriptLauncher(object):
    """
    Abstract w3af-script launching mixin
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return ["help"]

    def main(self):
        target = self.host or self.ip
        protocol = self.proto or 'http'
        output_file = tempfile.NamedTemporaryFile(delete=False)
        output_file.close()

        self._check_stop()

        called_ok, output, content = call_w3af(
            target = '%s://%s' % (protocol, target),
            timeout = self.SOCKET_TIMEOUT,
            commands = self._get_commands(),
            output_file = output_file.name
        )

        os.unlink(output_file.name)
        self._check_stop()

        if not called_ok:
            self._write_result('w3af_console launching error!')

        else:
            data = iter(output.split('\n'))
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

            # collecting the w3af output
            if content:
                for line in content.split('\n'):
                    if line.find(' - information ] ') == -1:
                        continue

                    self._write_result(line[line.find('] ') + 2:])

            else:
                self._write_result('No output from w3af.')

