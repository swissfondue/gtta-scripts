# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from core import Task, execute_task


class IG_Domain_BLWatch(Task):
    """
    Search records in BackLinkWatcher
    """

    def main(self, *args):
        """
        Main function
        """
        results = []
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'}

        index_params = {
            'backlinkurl': "http://" + self.host,
            'submit': 'Check Backlinks'
        }
        ses = requests.Session()
        soup = BeautifulSoup(
            ses.get(
                'http://www.backlinkwatch.com',
                headers=headers,
            ).content)

        salt = soup.find('input', attrs={'type': 'hidden', 'name': 'salt'}).attrMap['value']

        index_params.update({'salt': salt})

        req = ses.post(
            'http://www.backlinkwatch.com/index.php',
            headers=headers,
            data=index_params,
            timeout=10000
        )

        self._write_result(req.content)


    def test(self):
        """
        Test function
        """
        self.host = "clariant.com"
        self.main()

execute_task(IG_Domain_BLWatch)
