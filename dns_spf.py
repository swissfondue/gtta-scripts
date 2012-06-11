# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Resolver
from dns.exception import DNSException, Timeout
from socket import gethostbyname
from gtta import Task, execute_task
from gtta.error import TaskTimeout, NoHostName, InvalidTarget
import spf

class DNS_SPF(Task):
    """
    Get DNS SPF records
    """
    def main(self, host=[]):
        """
        Main function
        """
        target = self.ip

        if self.host:
            try:
                target = gethostbyname(self.host)
            except:
                raise InvalidTarget('Host not found.')

        domain = None

        if host and host[0]:
            domain = host[0]

        if not domain:
            raise NoHostName('No host name specified.')

        errors     = []
        spf_record = None
        txt_record = None
        spf_valid  = False

        self._check_stop()

        try:
            try:
                # check TXT record type for SPF records
                r             = Resolver()
                r.lifetime    = self.DNS_TIMEOUT
                r.nameservers = [ target ]

                txt_records = r.query(domain, 'TXT')
                txt_records = map(lambda x: str(x), txt_records)

                for txt in txt_records:
                    txt = str(txt)

                    # remove quotes
                    if txt[0] == '"' and txt[-1] == '"':
                        txt = txt[1:-1]

                    if txt.startswith('v=spf1'):
                        txt_record = txt
                        break

            except NoAnswer:
                pass

            self._check_stop()

            try:
                # check SPF record type for SPF records
                r          = Resolver()
                r.lifetime = self.DNS_TIMEOUT

                spf_records = r.query(domain, 'SPF')
                spf_records = map(lambda x: str(x), spf_records)

                if len(spf_records) > 0:
                    spf_record = str(spf_records[0])

                    # remove quotes
                    if spf_record[0] == '"' and spf_record[-1] == '"':
                        spf_record = spf_record[1:-1]

            except NoAnswer:
                pass

            self._check_stop()

            # validate the SPF record
            if spf_record or txt_record:
                try:
                    record = txt_record

                    if spf_record:
                        record = spf_record

                    # get MX records
                    r          = Resolver()
                    r.lifetime = self.DNS_TIMEOUT

                    mx_records = r.query(domain, 'MX')
                    mx_records = map(lambda x: str(x), mx_records)

                    self._check_stop()

                    mx_ip = None

                    if mx_records and len(mx_records) > 0:
                        mx_server = str(mx_records[0]).split(' ')[1]
                        mx_ip     = gethostbyname(mx_server)

                    self._check_stop()

                    spf_query = spf.query(i=mx_ip, h=None, s='admin@%s' % domain, timeout=self.DNS_TIMEOUT)
                    result = spf_query.check(record)

                    if result[0] == 'pass':
                        spf_valid = True

                except TaskTimeout:
                    raise

                except:
                    pass

        except NoAnswer:
            return 'No answer from name server.'

        except NoNameservers:
            return 'No name servers.'

        except NXDOMAIN:
            return 'Host not found.'

        except Timeout:
            return 'DNS request timeout.'

        except DNSException:
            return 'DNS error.'

        self._check_stop()

        if spf_record or txt_record:
            output = []

            if spf_record:
                output.append('SPF "%s"' % spf_record)

            if txt_record:
                output.append('TXT "%s"' % txt_record)

            if spf_valid:
                output.append('SPF record is valid.')
            else:
                errors.append('SPF record is invalid.')

            if (spf_record and not txt_record) or (not spf_record and txt_record):
                errors.append('It\'s recommended to have SPF records of both SPF and TXT record types, RFC 4408.')
            elif spf_record != txt_record:
                errors.append('SPF record contents should be identical for TXT and SPF record types.')

            if errors:
                output.append('%s' % '\n'.join(errors))

            return '\n'.join(output)

        return 'No SPF records.'

execute_task(DNS_SPF)
