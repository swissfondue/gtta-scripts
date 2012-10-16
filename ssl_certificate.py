# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

import gtta
import sslyze_tools
import parse

class SSLCertificateInfoTask(gtta.Task, sslyze_tools.SSLyzeLauncher):
    """
    SSL Certificate information checker
    """
    def main(self):
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

gtta.execute_task(SSLCertificateInfoTask)
