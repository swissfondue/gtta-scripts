# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError
from core import Task, execute_task
from core.error import NotEnoughArguments


class IG_Domain_Spyonweb(Task):
    """
    Search records in Spyonweb
    """
    def request(self, command, param, access_token):
        """API request"""

        try:
            req = requests.get(
                "https://api.spyonweb.com/v1/%s/%s?access_token=%s" % (command, param, access_token),
                headers={"User-Agent": "Mozilla/5.0"}
            )

        except ConnectionError:
            raise Exception("Spyonweb API connection error")

        try:
            json = req.json()
        except:
            json = None

        if not json or not "status" in json:
            return None

        if json["status"] == "error":
            raise Exception("Spyonweb API error: %s" % req.json["message"])

        if json["status"] == "not_found":
            return None

        if not "result" in json:
            return None

        return json["result"]

    def main(self, access_token=[], *args):
        """
        Main function
        """
        if not access_token or not access_token[0]:
            self._write_result("Spyonweb API key is required.")
            return

        results = []
        access_token = access_token[0]

        if self.ip:
            result = self.request("ip", self.ip, access_token)

            if not result:
                return

            for domain in result['ip'][self.ip]['items'].keys():
                if domain not in results:
                    results.append(domain)
                    self._write_result(domain)

        else:
            result = self.request("summary", self.target, access_token)

            if not result:
                return

            items = result['summary'][self.target]['items']
            adsense_ids = items['adsense'] if 'adsense' in items.keys() else {}
            analytics_ids = items['analytics'] if 'analytics' in items.keys() else {}
            website_ips = items['ip'] if 'ip' in items.keys() else {}

            for key, val in adsense_ids.items():
                if val > 1:
                    result = self.request("adsense", key, access_token)

                    if not result:
                        continue

                    for domain in result['adsense'][key]['items'].keys():
                        if domain not in results:
                            results.append(domain)
                            self._write_result(domain)

            for key, val in analytics_ids.items():
                if val > 1:
                    result = self.request("analytics", key, access_token)

                    if not result:
                        continue

                    for domain in result['analytics'][key]['items'].keys():
                        if domain not in results:
                            results.append(domain)
                            self._write_result(domain)

            for key, val in website_ips.items():
                if val > 1:
                    result = self.request("ip", key, access_token)

                    if not result:
                        continue

                    for domain in result['ip'][key]['items'].keys():
                        if domain not in results:
                            results.append(domain)
                            self._write_result(domain)

    def test(self):
        """
        Test function
        """
        self.target = "infofaq.com"
        self.main(["QqklGZGUwMeW"])

execute_task(IG_Domain_Spyonweb)
