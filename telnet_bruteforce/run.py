# coding: utf-8

from telnetlib import Telnet, TELNET_PORT
from core import Task, execute_task


class TelnetBruteforce(Task):
    """
    Telnet banner
    """
    TEST_TIMEOUT = 120
    TELNET_TIMEOUT = 10

    def main(self, *args):
        """
        Main function
        """
        self._check_stop()
        passwords = open("files/data.txt", "r").read().split("\n")

        target = self.target or self.host or self.ip
        port = self.port or TELNET_PORT
        has_login = False
        has_password = False
        found = False

        try:
            ctr = 0

            for data in passwords:
                login, password = data.split(":")

                if has_login and not login:
                    continue

                if has_password and not password:
                    continue

                ctr += 1
                telnet = Telnet(target, port, self.TELNET_TIMEOUT)
                response = telnet.read_until("login:", self.TELNET_TIMEOUT)

                if not response:
                    self._write_result("No response from server.")
                    break

                if response.find("login:") != -1:
                    has_login = True
                elif response.find("Password:") != -1:
                    has_password = True

                if not has_login and not has_password:
                    self._write_result("No login or password required.")
                    break

                if has_login and login:
                    telnet.write("%s\n" % login)
                    response = telnet.read_until("Password:", self.TELNET_TIMEOUT)

                    if response.find("Password:") != -1:
                        has_password = True

                if has_password and password:
                    telnet.write("%s\n" % password)

                response = telnet.read_until("incorrect", self.TELNET_TIMEOUT)
                response = response.strip()

                if response and response.find("incorrect") == -1:
                    self._write_result("Password match - login: %s, password: %s" % (login, password))
                    found = True

                    break

                telnet.close()

            if not found:
                self._write_result("Login or password not found (tried %d combinations)" % ctr)

        except:
            self._write_result("Unable to connect to %s:%d" % (target, port))

    def test(self):
        """
        Test function
        """
        self.target = "192.168.1.111"
        self.main()

execute_task(TelnetBruteforce)
