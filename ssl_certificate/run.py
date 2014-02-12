# -*- coding: utf-8 -*-

from core import execute_task, parse
from sslyze import SSLyzeLauncher

class SSLCertificateInfoTask(SSLyzeLauncher):
    """
    SSL Certificate information checker
    """
    TIMEOUT = 60
    TEST_TIMEOUT = 60

    def _get_commands(self):
        """
        Returns the list of sslyze options
        """
        return [
            "--regular",
        ]

    def _parse_result(self, data):
        """
        Parses the sslyze output (@data)
        """
        parser = parse.LineByLineParser()
        parser["Issuer:"] = "issuer"
        parser["Key Size:"] = "size"
        parser["Signature Algorithm:"] = "alg"

        data = parser.parse(data.split("\n"))

        if "issuer" not in data:
            data["issuer"] = "N/A"

        if "size" not in data:
            data["size"] = "N/A"

        if "alg" not in data:
            data["alg"] = "N/A"

        return (
            "Certificate information:\n"
            "Issuer: {issuer}\n"
            "Key Size: {size}\n"
            "Algorithm: {alg}"
        ).format(**data)

    def test(self):
        """
        Test function
        """
        self.host = "www.google.com"
        self.main()

execute_task(SSLCertificateInfoTask)
