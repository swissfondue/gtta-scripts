# -*- coding: utf-8 -*-

import socket
import os
import core
import pygeoip
from Queue import Queue
from socket import inet_aton
from threading import Thread

ASN_DB = os.path.join("files", "GeoIPASNum.dat")
GIP_DB = os.path.join("files", "GeoIP.dat")

class ASNInfoTask(core.Task):
    """
    ASN Information task
    """

    MULTITHREADED = True

    def main(self, *args):
        """
        Main function
        """
        def get_info(db, method_name, target):
            """
            Get ASN info
            """
            result = None

            try:
                db_obj = pygeoip.GeoIP(db)
                m = getattr(db_obj, method_name)

                try:
                    result = m(target)
                except pygeoip.GeoIPError:
                    self._write_result('Error: Wrong database format! (%s)' % db)

            except IOError:
                self._write_result('Error: Can`t load the database: (%s)' % db)

            return result

        def worker():
            while True:
                ip = None
                host = None

                target = self.queue.get()

                try:
                    inet_aton(target)
                    ip = target

                except:
                    host = target

                if not ip:
                    try:
                        ip = socket.gethostbyname(host)
                    except Exception:
                        self._write_result('Host not found: %s' % host)
                        return

                asnum = get_info(ASN_DB, 'org_by_name', ip)
                company = None

                if asnum and asnum.find(' ') >= 0:
                    company = asnum[asnum.find(' ') + 1:]
                    asnum = asnum[:asnum.find(' ')]

                country = get_info(GIP_DB, 'country_name_by_name', ip)

                # Use Lock for clear output
                self.lock.acquire()

                self._write_result('Host IP: %s' % ip)
                self._write_result('AS Number: %s' % ( asnum or 'N/A' ))
                self._write_result('Company: %s' % ( company or 'N/A' ))
                self._write_result('Country: %s' % ( country or 'N/A' ))

                self.lock.release()

                self.queue.task_done()

        # Targets queue
        self.queue = Queue()

        for i in range(self.THREADS_COUNT):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        for target in self.targets:
            self.queue.put(target)

        self.queue.join()

    def test(self):
        """
        Test function
        """
        self.ip = "8.8.8.8"
        self.main()

core.execute_task(ASNInfoTask)
