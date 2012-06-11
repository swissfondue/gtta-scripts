# -*- coding: utf-8 -*-

from sys import path
path.append('lib')

from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Resolver
from dns.exception import DNSException, Timeout
from socket import gethostbyname
from re import match
from gtta import Task, execute_task
from gtta.error import TaskTimeout, NoHostName

class DNS_SOA(Task):
    """
    Get & validate DNS SOA records
    """
    DAY    = 60 * 60 * 24
    HOUR   = 60 * 60
    MINUTE = 60

    def format_seconds(self, seconds):
        """
        Convert seconds to a more human-friendly form
        """
        seconds = int(seconds)
        output  = []

        if seconds > self.DAY:
            days    = seconds / self.DAY
            seconds = seconds % self.DAY
            output.append('%id' % days)

        if seconds > self.HOUR:
            hours   = seconds / self.HOUR
            seconds = seconds % self.HOUR
            output.append('%ih' % hours)

        if seconds > self.MINUTE:
            minutes = seconds / self.MINUTE
            seconds = seconds % self.MINUTE
            output.append('%im' % minutes)

        if seconds > 0:
            output.append('%is' % seconds)

        return ' '.join(output)

    def validate_soa(self, soa):
        """
        Validate SOA record
        """
        serial, refresh, retry, expire, minimum = soa
        errors = []

        if match('^\d{1,10}$', serial):
            if int(serial) < 1 or int(serial) > 4294967295:
                errors.append('Serial number should be between 1 and 4294967295, RFC 1035 (%i)' % int(serial))

            else:
                century = int(serial[:2])
                month   = int(serial[4:6])
                day     = int(serial[6:8])

                if century not in ( 19, 20 ) or month < 1 or month > 12 or day < 1 or day > 31:
                    errors.append(
                        'The recommended syntax for serial number is YYYYMMDDnn '\
                        '(YYYY=year, MM=month, DD=day, nn=revision number), RFC 1912 (%i)' % int(serial)
                    )

        else:
            errors.append('Serial number should be between 1 and 4294967295, RFC 1035 (%s)' % serial)

        if match('^\d+$', refresh):
            refresh = int(refresh)

            if refresh < 1200 or refresh > 43200:
                errors.append('The recommended value for refresh time interval is 20 minutes to 12 hours, RFC 1912 (%s)' % self.format_seconds(refresh))

        else:
            errors.append('Refresh time interval should be a 32 bit number (%s)' % self.format_seconds(refresh))

        if match('^\d+$', retry):
            retry = int(retry)

            if retry < 180 or retry > 3600:
                errors.append('Typical value for retry time interval is 3 minutes to 1 hour (%s)' % self.format_seconds(retry))

        else:
            errors.append('Retry time interval should be a 32 bit number (%s)' % self.format_seconds(retry))

        if match('^\d+$', expire):
            expire = int(expire)

            if expire < 1209600 or expire > 2419200:
                errors.append('The recommended value for expire time is 2 to 4 weeks, RFC 1912 (%s)' % self.format_seconds(expire))

        else:
            errors.append('Expire time should be a 32 bit number (%s)' % self.format_seconds(expire))

        if match('^\d+$', minimum):
            minimum = int(minimum)

            if minimum < 1 or minimum > 4294967295:
                errors.append('Minimum TTL should be between 1 and 4294967295, RFC 1035 (%s)' % self.format_seconds(minimum))

            elif minimum < 86400 or minimum > 432000:
                errors.append('The recommended value for minimum TTL is 1 to 5 days, RFC 1912 (%s)' % self.format_seconds(minimum))

        else:
            errors.append('Minimum TTL should be a 32 bit number (%s)' % self.format_seconds(minimum))

        return errors

    def main(self, host=[]):
        """
        Main function
        """
        if host and host[0]:
            self.host = host[0]

        if not self.host:
            raise NoHostName('No host name specified.')

        results = []
        serials = []
        errors  = []

        self._check_stop()

        try:
            # get all name servers
            r          = Resolver()
            r.lifetime = self.DNS_TIMEOUT

            name_servers = r.query(self.host, 'NS')
            name_servers = map(lambda x: str(x), name_servers)

            # get each server's SOA record
            for name_server in name_servers:
                self._check_stop()

                result = {
                    'server'  : '?',
                    'ip'      : '?',
                    'soa'     : '?',
                    'message' : None
                }

                # remove the trailing dot
                if name_server[-1] == '.':
                    name_server = name_server[:-1]

                result['server'] = name_server

                try:
                    result['ip'] = gethostbyname(name_server)
                    self._check_stop()

                    try:
                        r             = Resolver()
                        r.lifetime    = self.DNS_TIMEOUT
                        r.nameservers = [ result['ip'] ]

                        soa_records = r.query(self.host, 'SOA')
                        soa_records = map(lambda x: str(x), soa_records)

                        if len(soa_records) == 0:
                            result['message'] = 'No SOA records.'

                        else:
                            soa = str(soa_records[0]).split(' ')
                            serial, refresh, retry, expire, minimum = soa[2:]

                            result['soa'] = '%-11s %-10s %-10s %-10s %-10s' % (
                                serial,
                                self.format_seconds(refresh),
                                self.format_seconds(retry),
                                self.format_seconds(expire),
                                self.format_seconds(minimum)
                            )

                            serials.append(soa[2])

                            # validate SOA record
                            soa_errors = self.validate_soa(soa[2:])

                            for error in soa_errors:
                                if error not in errors:
                                    errors.append(error)

                    except NoAnswer:
                        result['message'] = 'No answer from name server.'

                    except Exception, e:
                        result['message'] = e.__class__.__name__

                        if str(e):
                            result['message'] += ': %s' % str(e)

                except TaskTimeout:
                    raise

                except:
                    result['message'] = 'Host not found.'

                results.append(result)

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

        if len(results) > 0:
            output = []

            output.append('Nameserver                     IP                  SOA Serial      Refresh    Retry      Expire     Minimum')
            output.append('-----------------------------------------------------------------------------------------------------------')
            for result in results:
                line = '%-30s IP %-16s SOA %s' % ( result['server'], result['ip'], result['soa'] )

                if result['message']:
                    line += ' (%s)' % result['message']

                output.append(line)

            serials_equal = True
            sample_serial = serials[0]

            for soa in serials[1:]:
                if soa != sample_serial:
                    serials_equal = False
                    break

            if not serials_equal:
                errors.append('SOA record serial numbers should be equal across all name servers.')

            if errors:
                output.append('%s' % '\n'.join(errors))

            return '\n'.join(output)

        return 'No SOA records.'

execute_task(DNS_SOA)
