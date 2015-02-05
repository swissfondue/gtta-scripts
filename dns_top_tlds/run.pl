# DNS top TLDs
# ---

use MooseX::Declare;
use core::task qw(execute);
use core::resulttable;

# DNS top TLDs
class DNS_Top_TLDs extends Task {
    use Net::DNS;
    use LWP::UserAgent;
    use HTTP::Request;
    use core::task qw(call_external);

    # Process
    method _process(Str $target, $tld_list) {
        my ($dom, $my_tld) = split/\./, $target;
        my $tlds = [];

        foreach my $tld_entry (@$tld_list) {
            foreach my $tld (@$tld_entry) {
                chomp $tld;
                next unless $tld;

                unless ($tld ~~ @$tlds) {
                    push(@$tlds, $tld);
                }
            }
        }

        my $res = Net::DNS::Resolver->new;

        undef $/;

        my $ua = LWP::UserAgent->new;
        my @domains;
        $ua->timeout(60);

        map {
            my $cur = $_;

            unless ($cur eq $my_tld) {
                my $cur_domain = $dom . '.' . $cur;
                my $query = $res->search($cur_domain);

                if ($query) {
                    foreach my $rr ($query->answer) {
                        next unless $rr->type eq 'A';
                        my $whois = call_external("whois $cur_domain");

                        if (
                            $whois =~ /Company:(?: +)?([^\n]+)\n/si ||
                            $whois =~ /Organi[sz]ation:(?: +)?([^\n]+)\n/si ||
                            $whois =~ /Name:(?: +)?([^\n]+)\n/si
                        ) {
                            $whois = $1;
                        } else {
                            $whois = 'N/A';
                        }

                        my $request = HTTP::Request->new('GET' => 'http://' . $cur_domain);
                        my $response = $ua->request($request);
                        my $title = 'N/A';

                        unless ($response->is_error()) {
                            my $content = $response->content();
                            $title = $1 if ($content =~ /<title>(.*?)<\/title>/si);
                            $title =~ s/[\r\n]+//gi;
                        }

                        push(@domains, [$cur_domain, $rr->address, $whois, $title]);
                        last;
                    }
                }
            }
        } @$tlds;

        if (scalar(@domains) > 0) {
            my $table = ResultTable->new(columns => [
                {name => "Domain", width => "0.3"},
                {name => "IP", width => "0.2"},
                {name => "Whois", width => "0.2"},
                {name => "Title", width => "0.3"},
            ]);

            for (my $i = 0; $i < scalar(@domains); $i++) {
                my $row = [];

                for (my $k = 0; $k < scalar(@{$domains[$i]}); $k++) {
                    $domains[$i][$k] =~ s/</&lt;/g;
                    $domains[$i][$k] =~ s/>/&gt;/g;
                    $domains[$i][$k] =~ s/&/&amp;/g;

                    push(@$row, $domains[$i][$k]);
                }

                $table->add_row($row);
            }

            $self->_write_result($table->render());
        } else {
            $self->_write_result('No domains found.');
        }
    }

    # Main function
    method main($args) {
        $self->_process($self->target, $args);
    }

    # Test function
    method test {
        $self->_process("google.com", [["net", "org", "info"]]);
    }
}

execute(DNS_Top_TLDs->new());