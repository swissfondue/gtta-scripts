# -*- coding: utf-8 -*-

from sys import path
path.append('pythonlib')

from time import time
from urllib2 import Request, urlopen, URLError, HTTPError
from threading import Thread
from gtta import Task, execute_task

class HTTP_DOS(Task):
    """
    Fetching pages
    """
    HEADERS = {
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept-Encoding' : 'gzip,deflate',
        'Accept-Charset'  : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Connection'      : 'keep-alive',
    }

    any_thread_complete = False

    def main(self, thread_number=[], repeat_number=[], url=[], test_urls=[], cookie=[], referer=[]):
        """
        Main function that starts threads_counter and waits for them to finish
        """
        threads = self.check_value('threads', thread_number)
        repeats = self.check_value('repeats', repeat_number)

        if not self.proto:
            self.proto = 'http'

        headers = {}

        if self.host:
            headers['Host'] = self.host
            target = self.proto + '://' + self.host + '/'

        else:
            headers['Host'] = self.ip
            target = self.proto + '://' + self.ip + '/'

        headers.update(self.HEADERS)

        if url[0]:
            url = url[0]

            if url.startswith('/'):
                url = url[1:]

            target += url

        _test_urls = []

        if len(test_urls) > 0 and test_urls[0]:
            for test_url in test_urls:
                if test_url.startswith('/'):
                    test_url = test_url[1:]

                _test_urls.append(target + test_url)

        else:
            _test_urls.append(target)

        test_urls = _test_urls

        if cookie[0]:
            headers['Cookie'] = cookie[0]

        if referer[0]:
            headers['Referer'] = referer[0]

        self._check_stop()
        self.check_test_urls(test_urls, headers)

        thread_list = []

        for i in xrange(threads):
            thread_list.append(Thread(target=self.worker, args=( target, headers, repeats )))

        self._write_result('Starting %i threads (%i repeats)' % ( threads, repeats ))

        for thread in thread_list:
            thread.start()

        start_time = time()

        for thread in thread_list:
            self._check_stop()
            thread.join()

        self._check_stop()

        total_time = time() - start_time
        self._write_result('All threads finished, requests took %.2f seconds' % total_time)

        self.check_test_urls(test_urls, headers)

        if not self.produced_output:
            self._write_result('No result.')

    def worker(self, url, headers, repeats):
        """
        Worker thread
        """
        request = Request(url, headers=headers)

        for repeat in xrange(repeats):
            try:
                urlopen(request)
            except Exception:
                pass

    def check_test_urls(self, test_urls, headers):
        """
        Check urls from testing URL list for response time
        """
        self._write_result('Testing URLs...')

        for url in test_urls:
            self._check_stop()

            request = Request(url, headers=headers)
            result = ''
            start_time = int(time() * 1000)

            try:
                response = urlopen(request)
                result = str(response.getcode())

            except HTTPError as e:
                result = str(e.code)

            except URLError as e:
                result = 'URL error (%s)' % e.reason

            except Exception as e:
                result = 'error (%s: %s)' % ( e.__class__.__name__, str(e) )

            finally:
                end_time = int(time() * 1000) - start_time
                result += ' (%i ms)' % end_time

            if result:
                self._write_result('%s: %s' % ( url, result ))

    def check_value(self, value_name, value):
        """
        Check non-zero value
        """
        try:
            if not value[0]:
                raise ValueError

            value[0] = int(value[0])

            if value[0] == 0:
                raise ValueError

            return value[0]

        except ValueError:
            raise ValueError('Invalid value - %s: %s' % ( value_name, value[0] ))

execute_task(HTTP_DOS)
