# -*- coding: utf-8 -*-
from core import Task, execute_task
import subprocess


class IG_Domain_RR(Task):
    """
    Search records
    """
    TEST_TIMEOUT = 3600
    DEFAULT_WORDLIST = "fast"

    def main(self, word_list=(DEFAULT_WORDLIST,), *args):
        """
        Main function
        """
        if word_list and word_list[0]:
            word_list = word_list[0]
        else:
            word_list = self.DEFAULT_WORDLIST

        if self.ip:
            params = '-r %s' % self.ip
        else:
            params = '-d %s -w files/%s.txt' % (self.host, word_list)

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
        self.main(["fast"])
        self.ip = "208.67.1.4"
        self.main()

execute_task(IG_Domain_RR)