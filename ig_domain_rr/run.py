# -*- coding: utf-8 -*-
from core import Task, execute_task
import subprocess


class IG_Domain_RR(Task):
    """
    Search records
    """
    TEST_TIMEOUT = 3600

    def main(self, *args):
        """
        Main function
        """
        if self.ip:
            params = '-r %s' % self.ip
        else:
            params = '-d %s -w word.list' % self.host

        results = set()

        proc = subprocess.Popen('reverseraider %s' % params, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = proc.communicate()

        strings = filter(lambda x: len(x), res[0].split('\n'))
        map(lambda x: results.add(x.split('\t')[0].replace(' ', '')), strings)

        map(lambda x: self._write_result(x), results)

    def test(self):
        """
        Test function
        """
        self.host = "clariant.com"
        self.main()
        self.ip = "208.67.1.4"
        self.main()

execute_task(IG_Domain_RR)