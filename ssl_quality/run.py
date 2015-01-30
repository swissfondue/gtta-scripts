# coding: utf-8

from subprocess import Popen
from threading import Timer
from core import Task, execute_task


class SSLQualityTask(Task):
    """
    SSL quality checker
    """
    TEST_TIMEOUT = 60
    PROTOCOL_TIMEOUT = 5

    PROTOCOLS = ("ssl2", "ssl3", "tls1", "tls1_1", "tls1_2")
    PROTOCOL_NAMES = {
        "ssl2": "SSL 2.0",
        "ssl3": "SSL 3.0",
        "tls1": "TLS 1.0",
        "tls1_1": "TLS 1.1",
        "tls1_2": "TLS 1.2"
    }

    @staticmethod
    def timeout(process):
        """
        Process timeout handler
        """
        if process.poll() is None:
            try:
                process.kill()
            except:
                pass

    def main(self, *args):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        port = self.port

        if not port:
            port = 443

        for protocol in self.PROTOCOLS:
            process = Popen(
                'echo "GET /" | openssl s_client -%s -connect %s:%i' % (protocol, target, port),
                shell=True
            )

            timer = Timer(self.PROTOCOL_TIMEOUT, self.timeout, [process])
            timer.start()
            process.wait()
            timer.cancel()

            result = "No"

            if process.returncode == 0:
                result = "Yes"

            self._write_result("%s: %s" % (self.PROTOCOL_NAMES[protocol], result))

    def test(self):
        """
        Test function
        """
        self.port = 443
        self.host = "google.com"
        self.main()

execute_task(SSLQualityTask)
