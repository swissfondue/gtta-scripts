# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Domain_BLWatch(Task):
    """
    Search records in BackLinkWatcher
    """
    TEST_TIMEOUT = 60 * 60  # 1 hour

    def main(self, *args):
        """
        Main function
        """
        results = []
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'}
        index_params = {
            'backlinkurl': "http://" + self.host,
            'submit': 'Check Backlinks'}

        ses = requests.Session()

        # get salt
        soup = BeautifulSoup(
            ses.get(
                'http://www.backlinkwatch.com',
                headers=headers,
            ).content)

        salt = soup.find('input', attrs={'type': 'hidden', 'name': 'salt'}).attrMap['value']
        index_params.update({'salt': salt})

        soup = BeautifulSoup(ses.post(
            'http://www.backlinkwatch.com/index.php',
            headers=headers,
            data=index_params).content)

        td_list = soup.findAll('td', attrs={'width': '200'})
        for td in td_list:
            url = filter(lambda x: x[0] == 'href', td.find('a').attrs)[0][1]
            if not url in results:
                self._write_result(url)
                results.append(url)

    def test(self):
        """
        Test function
        """
        self.host = "clariant.com"
        self.main()

execute_task(IG_Domain_BLWatch)
