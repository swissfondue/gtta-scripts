# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from gtta import Task, execute_task
import sql_inject

"""
SQL injection script
   Адаптировать скрипт - http://sqid.rubyforge.org/
   Скрипт должен запускать процесс в фоне и после завершения проверять его результат.

   Скрипт sqid должен запускаться со следующими параметрами:
       --mode c - mode = проверка страниц конкретного сайта
       --crawl http(s)://target.com:PORT - URL сайта
       --accept-cookies

   Пример по интеграции со внешними программами - в скрипте cms_detection.py
"""


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


        ok, sqlis = sql_inject.get_injections(target)

        if not ok:
            self._write_result('SQID call error!')
        else:
            self._write_result(sqlis)


execute_task(Sql_Injector)