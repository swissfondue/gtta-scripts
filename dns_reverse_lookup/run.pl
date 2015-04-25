# DNS reverse lookup
# ---

use MooseX::Declare;
use core::task qw(execute);
use threads;
use threads::shared;

# DNS reverse lookup task
class DNS_Reverse_Lookup extends Task {
    use Net::DNS;
    use Net::IP;

    use constant MULTITHREADED => 1;

    my @threads;
    my $last_t : shared = 0;

    # Process
    method _process() {
        while (1) {
            my $seq = $last_t++;

            if ($seq >= @{$self->targets}) {
                return;
            }

            my $target = $self->targets->[$seq];
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
    }

    # Main function
    method main($args) {
        for my $t (1 .. $self->THREADS_COUNT) {
            push @threads, threads->create(\$self->_process, $t);
        }

        for my $t (@threads) {
            $t->join();
        }
    }

    # Test function
    method test {
        $self->_process("8.8.8.8");
    }
}

execute(DNS_Reverse_Lookup->new());
