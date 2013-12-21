# -*- coding: utf-8 -*-

from core import Task, execute_task, parse
from sslyze import SSLyzeLauncher

class SSLCertificateInfoTask(Task, SSLyzeLauncher):
    """
    SSL Certificate information checker
    """
    TIMEOUT = 60

    def main(self, *args):
        """
        Main function
        """
        super(SSLCertificateInfoTask, self).main()

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
        parser['Issuer:'] = 'issuer'
        parser['Key Size:'] = 'size'
        parser['Signature Algorithm:'] = 'alg'

        return (
            'Certificate information:\n'
            'Issuer: {issuer}\n'
            'Key Size: {size}\n'
            'Algorithm: {alg}'
        ).format(**parser.parse(data.split('\n')))

    def test(self):
        """
        Test function
        """
        self.host = "www.google.com"
        self.main()

execute_task(SSLCertificateInfoTask)
