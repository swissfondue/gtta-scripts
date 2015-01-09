# DNS AFXR
# ---

use MooseX::Declare;
use core::task qw(execute);

# DNS AFXR task
class DNS_AFXR extends Task {
    use Net::DNS;

    # Process host
    method _process(Str $host) {
        my (@zone, @domain_ns);
        my $res = Net::DNS::Resolver->new;
        my $query = $res->query($host, 'NS');

        if ($query) {
            $self->_write_result("DNS Servers for $host:");

            foreach my $rr (grep { $_->type eq 'NS' } $query->answer) {
                my $dnssrv = lc($rr->nsdname);
                $self->_write_result(" - $dnssrv");
                push (@domain_ns, lc($rr->nsdname));
            }
        } else {
            $self->_write_result("Please specify a domain name which DNS records should be tested.");
            return;
        }

        $self->_write_result("\nTesting NS servers:");

        for (@domain_ns) {
            $res->nameservers($_);
            @zone = $res->axfr($host);

            if (@zone) {
                $self->_write_result(" - $_: found " . scalar(@zone) . " records, AXFR is enabled");
            } else {
                $self->_write_result(" - $_: AXFR disabled");
            }
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

execute(DNS_AFXR->new());
