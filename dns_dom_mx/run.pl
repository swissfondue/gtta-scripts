# DNS Domain MX
# ---

use MooseX::Declare;
use core::task qw(execute);

# DNS MX task
class DNS_MX extends Task {
    use Net::DNS;

    # Get hostname
    method _hostname(Str $hostname) {
        my (@bytes, @octets, $packedaddr, $raw_addr, $host_name, $ip);

        if ($hostname =~ /[a-zA-Z]/g) {
            $raw_addr = (gethostbyname($hostname))[4];
            @octets	= unpack('C4', $raw_addr);
            $host_name = join('.', @octets);
        } else {
            @bytes = split(/\./, $hostname);
            $packedaddr	= pack('C4', @bytes);
            $host_name = (gethostbyaddr($packedaddr, 2))[0];
        }

        return $host_name;
    }

    # Process
    method _process(Str $host, Int $timeout, Int $debug) {
        no warnings; # no unicode garbage
        my $res = Net::DNS::Resolver->new('debug' => $debug);
        my $cnt = 1;

        unless ($host =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/) {
            $self->_write_result("\n" . $cnt++ . ') Error: not valid domain name ' . $host . "\n");
        } else {
            $host =~ s/^www\.//;

            $res->tcp_timeout($timeout);
            my @mx = mx($res, $host);

            if (@mx) {
                foreach my $rr ( @mx ) {
                    $self->_write_result($rr->preference . ' ' . $rr->exchange . ' (' . $self->_hostname($rr->exchange) . ")\n");
                }
            } else {
                $self->_write_result("\n" . $cnt++ . ') Warning: no MX records for domain ' . $host . ' (' . $res->errorstring . ")\n");
            }
        }
    }

    # Main function
    method main($args) {
        my ($timeout, $debug);

        $timeout = $self->_get_int($args, 0, 10);
        $debug = $self->_get_int($args, 1, 0);

        $self->_process($self->target, $timeout, $debug);
    }

    # Test function
    method test {
        $self->_process("google.com", 10, 1);
    }
}

execute(DNS_MX->new());
