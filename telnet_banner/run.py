# coding: utf-8

from telnetlib import Telnet, TELNET_PORT
from core import Task, execute_task


class Telnet_Banner(Task):
    """
    Telnet banner
    """
    TELNET_TIMEOUT = 10

    def main(self, *args):
        """
        Main function
        """
        self._check_stop()

        target = self.target or self.host or self.ip
        port = self.port or TELNET_PORT

        try:
            telnet = Telnet(target, port, self.TELNET_TIMEOUT)
            banner = telnet.read_until("login:", self.TELNET_TIMEOUT)

            if banner:
                self._write_result(banner)

        except:
            self._write_result("Unable to connect to %s:%d" % (target, port))

    def test(self):
        """
        Test function
        """
        self.target = "localhost"
        self.main()

execute_task(Telnet_Banner)
