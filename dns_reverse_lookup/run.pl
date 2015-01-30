# DNS reverse lookup
# ---

use MooseX::Declare;
use core::task qw(execute);

# DNS reverse lookup task
class DNS_Reverse_Lookup extends Task {
    use Net::DNS;
    use Net::IP;

    # Process
    method _process(Str $target) {
        my $res = Net::DNS::Resolver->new;

        my @ranges = split /\s+/, $target;

        foreach my $t (@ranges) {
            $t =~ s/^\s+//gi;
            $t =~ s/\s+$//gi;

            my $ip = new Net::IP($t);

            do {
                unless ($ip) {
                    $self->_write_result("Invalid IP or range: " . $t);
                    next;
                }

                my $IP = $ip->ip();
                my $target_IP = join('.', reverse split(/\./, $IP)).'.in-addr.arpa';
                my $query = $res->query($target_IP, "PTR");

                if ($query) {
                    my $found = 0;

                    foreach my $rr ($query->answer) {
                        next unless ($rr->type eq 'PTR');
                        $self->_write_result($IP . "\t\t" . $rr->rdatastr);
                        $found = 1;
                    }

                    $self->_write_result($IP .  "\t\tN/A") unless ($found);
                } else {
                    $self->_write_result($IP .  "\t\tN/A");
                }
            } while (++$ip);
        }
    }

    # Main function
    method main($args) {
        $self->_process($self->target);
    }

    # Test function
    method test {
        $self->_process("8.8.8.8");
    }
}

execute(DNS_Reverse_Lookup->new());
