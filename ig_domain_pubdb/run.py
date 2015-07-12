# -*- coding: utf-8 -*-
import re
from time import sleep
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Domain_PubDB(Task):
    """
    Search records in PubDB
    """
    TEST_TIMEOUT = 60 * 60
    URL = 'http://pub-db.com'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
    }

    pubs = set()
    uas = set()

    def _get_soup_by_path(self, path):
        """
        Get soup by path from PubDB
        """
        return BeautifulSoup(requests.get('%s%s' % (self.URL, path), headers=self.HEADERS).content)

    def _get_request_by_proto(self, proto):
        """
        Get request by proto and self.target
        """
        return requests.get('%s://%s' % (proto, self.target), headers=self.HEADERS)

    def _exctract_pubs(self, content):
        """
        Exctract pubs from content
        """
        return re.findall(r'pub-\d{16}', content)

    def _exctract_uas(self, content):
        """
        Exctract uas from content
        """
        return re.findall(r'UA-\d{8}', content)

    def main(self, *args):
        """
        Main function
        """
        results = []
        http_failed = False

        # check http
        try:
            req = self._get_request_by_proto('http')
            self.pubs.update(self._exctract_pubs(req.content))
            self.uas.update(self._exctract_uas(req.content))
        except Exception as e:
            http_failed = True

        # check https
        try:
            req = self._get_request_by_proto('https')
            self.pubs.update(self._exctract_pubs(req.content))
            self.uas.update(self._exctract_uas(req.content))
        except Exception as e:
            if http_failed:
                # bad target
                return

        # using PubDB collect domains for 'search by domain'
        # get links for PubDB
        if self.ip:
            hrefs = []
            # from ip
            try:
                soup = self._get_soup_by_path('/reverse-ip/%s.html' % self.ip)
                if not soup.find('title').text == '404 Not Found':
                    links = soup.find('table').findAll('a')
                    hrefs = [x.attrs[0][1] for x in links]
            except Exception as e:
                pass
        else:
            # from host
            hrefs = ['/%s.html' % self.host]

        # search by collected links
        for href in hrefs:
            sleep(1)

            try:
                soup = self._get_soup_by_path('%s' % href)
            except:
                continue

            if soup.find('title').text == '404 Not Found':
                continue

            div = soup.find('div', attrs={'id': 'stat'})

            if not div:
                continue

            self.pubs.update(self._exctract_pubs(div.text))
            self.uas.update(self._exctract_uas(div.text))

        # get domains by pubs
        for pub in self.pubs:
            sleep(1)

            try:
                soup = self._get_soup_by_path('/adsense/%s.html' % pub)
            except:
                continue

            for li in soup.findAll('li'):
                tag_a = li.find('a')
                if not tag_a:
                    continue
                domain = tag_a.text

                if not domain == self.target and domain not in results:
                    results.append(domain)
                    self._write_result(domain)

        # get domains by uas
        for ua in self.uas:
            sleep(1)

            try:
                soup = self._get_soup_by_path('/google-analytics/%s.html' % ua)
            except:
                continue

            for li in soup.findAll('li'):
                tag_a = li.find('a')
                if not tag_a:
                    continue
                domain = tag_a.text

                if not domain == self.target and domain not in results:
                    results.append(domain)
                    self._write_result(domain)

    def test(self):
        """
        Test function
        """
        self.target = self.host = "infofaq.com"
        self.main()
        self.target = self.ip = "104.27.167.105"
        self.main()

execute_task(IG_Domain_PubDB)
