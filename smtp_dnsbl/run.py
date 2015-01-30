# -*- coding: utf-8 -*-

from dns.resolver import Resolver
from socket import gethostbyname
from core import Task, execute_task
from core.error import InvalidTarget

class SMTP_DNSBL(Task):
    """
    SMTP DNS blacklist check
    """
    BLACKLISTS = (
        'truncate.gbudb.net',
        'sbl-xbl.spamhaus.org',
        'bl.spamcop.net',
        'dnsbl.sorbs.net',
        'dnsbl-1.uceprotect.net',
        'rbl.orbitrbl.com',
        'psbl.surriel.com',
        'intercept.datapacket.net',
        'spam.spamrats.com',
        'bl.spamcannibal.org',
        'dnsbl.njabl.org',
        'spamtrap.drbl.drand.net',
        'dnsbl.ahbl.org',
        'dnsbl.dronebl.org',
        'ix.dnsbl.manitu.net',
        'dnsbl.inps.de',
    )

    def main(self, *args):
        """
        Main function
        """
        ip = self.ip

        if self.host:
            try:
                ip = gethostbyname(self.host)
            except:
                raise InvalidTarget('Host not found.')

        self._check_stop()

        # reverse IP
        reversed_ip = ip.split('.')
        reversed_ip.reverse()
        reversed_ip = '.'.join(reversed_ip)

        for blacklist in self.BLACKLISTS:
            self._check_stop()

            try:
                domain = '%s.%s' % (reversed_ip, blacklist)

                r = Resolver()
                r.lifetime = self.DNS_TIMEOUT

                result = r.query(domain, 'A')

                if result and len(result) > 0:
                    info = None

                    # try to request a TXT record
                    try:
                        r          = Resolver()
                        r.lifetime = self.DNS_TIMEOUT

                        result = r.query(domain, 'TXT')

                        if result and len(result) > 0:
                            info = str(result[0])

                            if info[0] == '"' and info[-1] == '"':
                                info = info[1:-1]
                    except:
                        pass

                    message = '%s is blacklisted in %s' % ( ip, blacklist )

                    if info:
                        message = '%s\nDetails: %s\n' % ( message, info )

                    self._write_result(message)

            except:
                pass

        self._check_stop()

        if not self.produced_output:
            self._write_result('Server is not listed in any known blocklist.')

    def test(self):
        """
        Test function
        """
        self.host = "smtp.gmail.com"
        self.main()

execute_task(SMTP_DNSBL)
