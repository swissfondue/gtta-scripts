# -*- coding: utf-8 -*-

from urllib import urlencode
from urllib2 import urlopen, URLError, HTTPError, Request
from core import Task, execute_task
import json


class DNS_Hosting(Task):
    """
    Checks if there are other websites on the same server.
    """
    def main(self, api_key=None, *args):
        """
        Main function
        """
        target = self.host

        if not target:
            target = self.ip

        try:
            if not api_key:
                self._write_result("You must specify ViewDns Api Key.")
                return

            # Add parameter { "page" : 2 } if u want
            # to get next 10000 domains and increase
            # page if u need more then that
            params = urlencode({
                "host": target,
                "output": "json",
                "apikey": api_key
            })
            request = Request('http://pro.viewdns.info/reverseip?%s' % params)
            request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/11.10 Chromium/18.0.1025.142 Chrome/18.0.1025.142 Safari/535.19')
            response = urlopen(request, timeout=self.HTTP_TIMEOUT)

            response = response.read()

            response = json.loads(response)
            response = response["response"]

            if "error" in response:
                self._write_result("Service error: %s" % response["error"])
                return

            if "domains" not in response:
                self._write_result('No host names found.')
                return

            domains = []

            for d in response["domains"]:
                domains.append(d["name"])

            if len(domains) > 0:
                self._write_result(u'\n'.join(domains))
            else:
                self._write_result('No host names found.')

        except URLError, e:
            self._write_result('%s: %s' % ( e.__class__.__name__, e.reason ))
            return

        except HTTPError, e:
            self._write_result('HTTP error: %s' % str(e))
            return

        except ValueError, e:
            self._write_result('Value Error: Invalid API key.')
            return

        self._check_stop()

        if not self.produced_output:
            self._write_result('No result.')

    def test(self):
        """
        Test function
        """
        self.host = "microsoft.com"
        self.main(["ee61b8eb5e63aa95a63d15fa39d6e16e7ec15375"])

execute_task(DNS_Hosting)
