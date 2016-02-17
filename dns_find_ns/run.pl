# DNS Find NS
# ---

use MooseX::Declare;
use core::task qw(execute);

# DNS find NS task
class DNS_NS extends Task {
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
    method _process(Str $host) {
        my $res = Net::DNS::Resolver->new();

        unless ($host =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/) {
            die("Not a valid domain name: $host ");
        }

        $res->tcp_timeout(10);

        unless ($res->query($host, "A") || $res->query($host, "CNAME")) {
            die("Host not found: $host");
        }

        # remove third, fourth and higher level domain names
        while ($host =~ tr/\.// > 1) {
            $host =~ s/^[a-z\-0-9]+\.//;
        }

        my $query = $res->query($host, "NS");

        unless ($query) {
            die("No NS found for $host (" . $res->errorstring . ")");
        }

        foreach my $rr (grep { $_->type eq "NS" } $query->answer) {
            $self->_write_result($rr->nsdname . " (" . $self->_hostname($rr->nsdname) . ")");
        }
    }

    # Main function
    method main($args) {
        $self->_process($self->target);
    }

    # Test function
    method test {
        $self->_process("google.com");
    }
}

execute(DNS_NS->new());
