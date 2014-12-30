# -*- coding: utf-8 -*-

import os
import re
from core import call, Task


_SSLYZE_CMD = os.path.join(os.path.dirname(__file__), "sslyze", "sslyze.py")


def call_sslyze(target, port, commands, timeout=15):
    """
    Calls sslyze, and returns the result
    Result: (success: boolean, data: unicode)
    """
    commands.insert(0, '--timeout=%s' % timeout)
    commands.append("%s:%s" % (target, str(port)))

    return call.call(["python", _SSLYZE_CMD] + commands)


class SSLyzeLauncher(Task):
    """
    Abstract sslyze launching mixin
    """
    def _get_commands(self):
        """
        Returns the list of w3af commands
        """
        return ["-h"]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        return data

    def main(self, *args):
        """
        Main function
        """
        target = self.host or self.ip
        port = self.port or 443
        self._check_stop()

        called_ok, output = call_sslyze(
            target=target,
            port=port,
            timeout=self.SOCKET_TIMEOUT,
            commands=self._get_commands()
        )

        self._check_stop()

        if not called_ok:
            self._write_result('sslyze launching error!')

        else:
            self._check_stop()
            warning = re.search(r'(WARNING:.*)\n', output)

            if warning:
                self._write_result(warning.groups()[0])
            else:
                self._write_result(self._parse_result(output))
