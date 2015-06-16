# -*- coding: utf-8 -*-

import socket
import os
import core
import pygeoip

ASN_DB = os.path.join("files", "GeoIPASNum.dat")
GIP_DB = os.path.join("files", "GeoIP.dat")


class ASNInfoTask(core.Task):
    """
    ASN Information task
    """
    MULTITHREADED = True

    def _get_info(self, db, method_name, target):
        """Get ASN info"""
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

    def main(self, *args):
        """Main function"""
        if not self.ip:
            try:
                self.ip = socket.gethostbyname(self.host)
            except Exception:
                self._write_result('Host not found: %s' % self.host)
                return

        asnum = self._get_info(ASN_DB, 'org_by_name', self.ip)
        company = None
        
        if asnum and asnum.find(' ') >= 0:
            company = asnum[asnum.find(' ') + 1:]
            asnum = asnum[:asnum.find(' ')]

        country = self._get_info(GIP_DB, 'country_name_by_name', self.ip)

        self._write_result('Host IP: %s' % self.ip)
        self._write_result('AS Number: %s' % ( asnum or 'N/A' ))
        self._write_result('Company: %s' % ( company or 'N/A' ))
        self._write_result('Country: %s' % ( country or 'N/A' ))

    def test(self):
        """
        Test function
        """
        self.ip = "8.8.8.8"
        self.main()

core.execute_task(ASNInfoTask)
