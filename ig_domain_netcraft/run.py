# -*- coding: utf-8 -*-
import hashlib
import urlparse
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Domain_Netcraft(Task):
    """
    Search records in Netcraft
    """
    target = ''

    def main(self, *args):
        """
        Main function
        """
        results = []
        url = 'http://searchdns.netcraft.com/?restriction=site+contains&host=%s' % self.target
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
        req = requests.get(url, headers=headers)

        cookies = requests.utils.dict_from_cookiejar(req.cookies)
        challenge = urlparse.parse_qs("x=%s" % cookies['netcraft_js_verification_challenge'])
        challenge = challenge["x"][0]
        cookies['netcraft_js_verification_response'] = hashlib.sha1(challenge).hexdigest()

        req = requests.get(
            url,
            headers=headers,
            cookies=requests.utils.cookiejar_from_dict(cookies)
        )

        soup = BeautifulSoup(req.content)
        table = soup.find('div', attrs={'id': 'content'}).find('table', attrs={'class': 'TBtable'})

        for tag in table.findAll('a', attrs={'rel': 'nofollow'}):
            result = tag.text

            if result not in results:
                results.append(result)
                self._write_result(result)

    def test(self):
        """
        Test function
        """
        self.target = "clariant"
        self.main()

execute_task(IG_Domain_Netcraft)
