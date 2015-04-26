# Subdomain bruteforce
# ---

use MooseX::Declare;
use core::task qw(execute);

# Subdomain bruteforce task
class Subdomain_Bruteforce extends Task {
    use constant TEST_TIMEOUT => 360;
    use Net::DNS;
    use Net::hostent;
    use Socket;
    use core::resulttable;
    use threads::shared;

    use constant MULTITHREADED => 1;

    my @threads;
    my $last_t : shared = 0;

    my $known_names = {};
    my $domains = [];
    my $nameservers = [];
    my $wildcard_dns;

    # Search host IP
    method search_host($search_item, $target) {
        my $res = Net::DNS::Resolver->new;
        $res->tcp_timeout(30);
        my $packet = $res->search($search_item);

        return unless ($packet);

        foreach my $answer ($packet->answer) {
            my @name = split (/\t/, $answer->string);
            next unless ($name[3] eq "A" || $name[3] eq "PTR");

            chop $name[0];
            my $this_ip;

            if ($name[4] eq $wildcard_dns) {
                next;
            }

            $this_ip = $name[4];
            next if ($known_names->{"$this_ip,$search_item"});

            $known_names->{"$this_ip,$search_item"} = 1;
            push($domains, shared_clone([$search_item, $this_ip]));
        }
    }
    
    # Process
    method _process(Int $big_file) {
        while (1) {
            my $seq = $last_t++;

            if ($seq >= @{$self->targets}) {
                return;
            }

            my $target = $self->targets->[$seq];

            if ($target !~ /[a-z\d.-]\.[a-z]*/i) {
                die("Invalid domain name.");
            }

            $domains = shared_clone([]);
            $known_names = shared_clone({});
            $nameservers = shared_clone([]);

            my $res = Net::DNS::Resolver->new;
            $res->tcp_timeout(30);
            my $query = $res->query($target, 'NS');

            if ($query) {
                foreach my $rr (grep {$_->type eq 'NS'} $query->answer) {
                    my $dnssrv = $rr->nsdname;
                    push ($nameservers, $rr->nsdname);
                }
            }

            $res->nameservers($nameservers);

            my @common_cnames = ();
            my $hosts = q[files/hosts_small.txt];
            $hosts = q[files/hosts_big.txt] if ($big_file);

            if (-e $hosts) {
                open (WORDLIST, '<', $hosts) or die("Can't open $hosts");

                for (<WORDLIST>) {
                    chomp;
                    push @common_cnames, $_;
                }

                close WORDLIST;
            } else {
                die("Can't open $hosts");
            }

            srand;

            $wildcard_dns = 1e11 - int(rand(1e10));

            if (my $h = gethost($wildcard_dns . ".$target")) {
                my $wildcard_addr = inet_ntoa($h->addr);
                $wildcard_dns = $wildcard_addr;
                push($domains, shared_clone(["Wildcard", $wildcard_addr]));
            } else {
                $wildcard_dns = "";
            }

            foreach my $host (@common_cnames) {
                $self->search_host("$host.$target", $target);
            }

            unless ($domains) {
                $self->_write_result("No subdomains found.");
            } else {
                my $table = ResultTable->new(columns => [
                    {name => "#", width => "0.2"},
                    {name => "Domain", width => "0.5"},
                    {name => "IP", width => "0.3"}
                ]);

                for (my $i = 0; $i < scalar(@{$self->domains}); $i++) {
                    $table->add_row([
                        $i + 1,
                        $domains->[$i][0],
                        $domains->[$i][1]
                    ]);
                }

                $self->_write_result($table->render());
            }
        }
    }

    # Main function
    method main($args) {
        my $big_file = $self->_get_int($args, 0, 0);

        for my $t (1 .. $self->THREADS_COUNT) {
            push @threads, threads->create(sub { $self->_process($big_file); }, $t);
        }

        for my $t (@threads) {
            $t->join();
        }
    }

    # Test function
    method test {
        $self->_process("google.com", 0);
    }
}

execute(Subdomain_Bruteforce->new());
