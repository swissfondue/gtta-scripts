# -*- coding: utf-8 -*-

from core import call, Task, execute_task


class PingTask(Task):
    """
    Ping task
    """
    TIMEOUT = 240

    def _ping(self, target, packet):
        """
        Call ping
        """
        ok, out = call.call(['ping', '-s', str(packet - 8), '-c', '1', target])

        if not ok:
            raise ValueError('"ping" calling error!')

        for line in out.split('\n'):
            if 'unknown host' in line:
                raise ValueError('Unknown host: %s' % target)

            elif 'bytes from' in line or '0 received' in line:
                return '%s: %s' % (packet, line)

        return ''

    def main(self, *args):
        """
        Main function
        """
        target = self.host or self.ip
        result = []

        for packet in [2 ** x for x in xrange(4, 15)] + [64000]:
            try:
                result.append(self._ping(target, packet))
            except ValueError as err:
                self._write_result(unicode(err))
                return

            self._check_stop()

        self._write_result('\n'.join(result))

    def test(self):
        """
        Test function
        """
        self.host = "google.com"
        self.main()

execute_task(PingTask)
