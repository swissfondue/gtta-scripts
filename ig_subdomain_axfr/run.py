# -*- coding: utf-8 -*-

import dns.resolver
import dns.query
import dns.zone
from core import Task, execute_task


class IG_Subdomain_AXFR(Task):
    """
    Get subdomains with AXFR records
    """

    def main(self, *args):
        """
        Main function
        """
        if not self.host:
            return

        if self.host.startswith("www."):
            self.host = self.host[4:]

        results = []

        try:
            answers = dns.resolver.query(self.host, "NS")
            nss = [str(rdata) for rdata in answers]

            for n in nss:
                try:
                    z = dns.zone.from_xfr(dns.query.xfr(n, self.host))
                    
                    for k in z.nodes.keys():
                        k = str(k)
                        
                        if k[0] not in ["@", "*"]:
                            subdomain = ".".join([k, self.host])

                            if subdomain not in results:
                                self._write_result(subdomain)
                                results.append(subdomain)

                except Exception, e:
                    continue
        except Exception, e:
            pass

    def test(self):
        """
        Test function
        """
        self.host = "livedoor.com"
        self.main()

execute_task(IG_Subdomain_AXFR)
