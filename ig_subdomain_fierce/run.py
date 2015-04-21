# -*- coding: utf-8 -*-
from core import Task, execute_task
import subprocess


class IG_Subdomain_Fierce(Task):
    """
    Search records with fierce.pl
    """
    TEST_TIMEOUT = 3600

    def main(self, *args):
        """
        Main function
        """
        if self.ip:
            return

        results = set()

        proc = subprocess.Popen('perl fierce.pl -dns %s' % self.host, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = proc.communicate()

        strings = filter(lambda x: len(x), res[0].split('\n'))
        res_strings = filter(lambda x: x[0].isdigit(), strings)
        map(lambda x: results.add(x.split('\t')[1]), res_strings)

        map(lambda x: self._write_result(x), results)

    def test(self):
        """
        Test function
        """
        self.host = "clariant.com"
        self.main()

execute_task(IG_Subdomain_Fierce)
