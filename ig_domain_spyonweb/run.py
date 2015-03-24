# -*- coding: utf-8 -*-
import requests
from core import Task, execute_task


class IG_Domain_Spyonweb(Task):
    """
    Search records in Spyonweb
    """

    def main(self, access_token=[], *args):
        """
        Main function
        """
        results = []
        access_token_0 = access_token[0]
        headers = {'User-Agent': 'Mozilla/5.0'}

        if self.ip:
            req = requests.get(
                'https://api.spyonweb.com/v1/ip/%s?access_token=%s' % (self.ip, access_token_0),
                headers=headers)
            if req.json['status'] == 'not_found':
                return
            for result in req.json['result']['ip'][self.ip]['items'].keys():
                if result not in results:
                    results.append(result)
                    self._write_result(result)
        else:
            req = requests.get(
                'https://api.spyonweb.com/v1/summary/%s?access_token=%s' % (self.target, access_token_0),
                headers=headers)

            if req.json['status'] == 'not_found':
                return

            items = req.json['result']['summary'][self.target]['items']
            adsense_ids = items['adsense'] if 'adsense' in items.keys() else {}
            analytics_ids = items['analytics'] if 'analytics' in items.keys() else {}
            website_ips = items['ip'] if 'ip' in items.keys() else {}

            for key, val in adsense_ids.items():
                if val > 1:
                    req = requests.get(
                        'https://api.spyonweb.com/v1/adsense/%s?access_token=%s' % (key, access_token_0),
                        headers=headers)
                    for result in req.json['result']['adsense'][key]['items'].keys():
                        if result not in results:
                            results.append(result)
                            self._write_result(result)

            for key, val in analytics_ids.items():
                if val > 1:
                    req = requests.get(
                        'https://api.spyonweb.com/v1/analytics/%s?access_token=%s' % (key, access_token_0),
                        headers=headers)
                    for result in req.json['result']['analytics'][key]['items'].keys():
                        if result not in results:
                            results.append(result)
                            self._write_result(result)

            for key, val in website_ips.items():
                if val > 1:
                    req = requests.get(
                        'https://api.spyonweb.com/v1/ip/%s?access_token=%s' % (key, access_token_0),
                        headers=headers)
                    for result in req.json['result']['ip'][key]['items'].keys():
                        if result not in results:
                            results.append(result)
                            self._write_result(result)

    def test(self):
        """
        Test function
        """
        self.target = "infofaq.com"
        self.main(["QqklGZGUwMeW"])

execute_task(IG_Domain_Spyonweb)
