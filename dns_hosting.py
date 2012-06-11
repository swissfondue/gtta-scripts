# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from urllib import urlencode
from urllib2 import urlopen, URLError, HTTPError, Request
from lxml import html
from re import findall
from gtta import Task, execute_task

class DNS_Hosting(Task):
    """
    Checks if there are other websites on the same server.
    """
    def main(self, host=[], show_all=[]):
        """
        Main function
        """
        if host and host[0]:
            self.host = host[0]

        target = self.host

        if not target:
            target = self.ip

        if show_all and show_all[0].lower() in ( '1', 'true', 'yes', 'on', 'ok' ):
            show_all = True
        else:
            show_all = False

        output  = []
        domains = []
        offset  = 0
        first   = True
        results = 0

        try:
            while True:
                self._check_stop()

                domain_count = 0

                request = Request('http://serversniff.net/hostonip.php')
                request.add_data(urlencode({
                    'domain'    : target,
                    'fullcount' : 0,
                    'offset'    : offset
                }))
                request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/11.10 Chromium/18.0.1025.142 Chrome/18.0.1025.142 Safari/535.19')

                if first:
                    request.add_header('Referer', 'http://serversniff.net/content.php?do=hostonip')
                else:
                    request.add_header('Referer', 'http://serversniff.net/hostonip.php')

                response = urlopen(request, timeout=self.HTTP_TIMEOUT)
                response = response.read()

                if first:
                    results = findall('We currently know (\d+)', response)

                    if results and len(results) > 0:
                        results = int(results[0])
                    else:
                        results = 0

                    first = False

                doc  = html.fromstring(response)
                rows = doc.xpath('.//body/table/tr')

                for row in rows:
                    domain = row.xpath('.//td[2]/b/text()')

                    if domain and len(domain) == 1:
                        domain = domain[0].strip()

                        if domain not in domains:
                            domains.append(domain)

                        domain_count += 1

                results -= domain_count

                if results <= 0 or not show_all:
                    break

                offset += 100

            if len(domains) > 0:
                output += domains
            else:
                output.append('No host names found.')

        except URLError, e:
            return '%s: %s' % ( e.__class__.__name__, e.reason )

        except HTTPError, e:
            return 'HTTP error: %s' % str(e)

        self._check_stop()

        if len(output) > 0:
            return '\n'.join(output)

        return 'No result.'

execute_task(DNS_Hosting)
