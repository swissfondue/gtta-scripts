# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from gtta import Task, execute_task
import sql_inject

class Sql_Injector(Task):
    """
    Sql Injector
    """
    def main(self):
        """
        Main function
        """
        if not self.proto:
            self.proto = 'http'

        if not self.port:
            self.port = 80

        if self.host:
            target = self.proto + '://' + self.host + ':' + str(self.port)
        else:
            target = self.proto + '://' + self.ip + ':' + str(self.port)

        ok, sqlis = sql_inject.get_injections(target + '/')

        if not ok:
            self._write_result('SQID call error.')
        else:
            self._write_result(sqlis)

execute_task(Sql_Injector)