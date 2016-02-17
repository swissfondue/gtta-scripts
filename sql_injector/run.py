# -*- coding: utf-8 -*-

from core import Task, execute_task
from sqid import get_injections

class Sql_Injector(Task):
    """
    Sql Injector
    """
    def main(self, *args):
        """
        Main function
        """
        if not self.proto:
            self.proto = "http"

        if not self.port:
            self.port = 80

        target = self.proto + "://" + self.target + ":" + str(self.port)
        ok, sqlis = get_injections(target)

        if not ok:
            self._write_result("SQID call error.")
        else:
            self._write_result(sqlis)

    def test(self):
        """
        Test function
        """
        self.proto = "http"
        self.port = 80
        self.target = "gtta.demo.stellarbit.com"
        self.main()

execute_task(Sql_Injector)