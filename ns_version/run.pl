# NS Version
# --

use MooseX::Declare;
use core::task qw(execute);

# NS Version task
class NS_Version extends Task {
    use Net::DNS;
    use core::task qw(call_external);

    # Process
    method _process(Str $host) {
        unless ($host =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/) {
            $self->_write_result('Error: not valid domain name ' . $host);
        } else {
            $host =~ s/^www\.//;

            my $res = Net::DNS::Resolver->new();
            my $cnt = 1;

            undef $/;

            my $query = $res->query($host, 'NS');

            if ($query) {
                foreach my $rr (grep { $_->type eq 'NS' } $query->answer) {
                    $self->_write_result($cnt++ . ". " . $rr->nsdname . ":");

                    my $class = 'chaos';
                    my $target = $rr->nsdname;
                    my $out = "";

                    while (1) {
                        $out = call_external("nslookup -type=txt -cl=$class version.bind $target");

                        if ($class eq 'chaos' && $out =~ m/got version.bind\/TXT\/IN/si) {
                            $self->_write_result("Possible misconfiguration - expects version.bind. in IN-class record.");
                            $class = 'in';
                            next;
                        }

                        last;
                    }

                    $self->_write_result($out);
                    $self->_write_result("\n");
                }
            } else {
                $self->_write_result("\n" . $cnt++ . ') Error: no NS for domain ' . $host . ' (' . $res->errorstring . ")");
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

execute(NS_Version->new());
