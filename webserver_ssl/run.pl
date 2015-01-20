# Webserver SSL
# ---

use MooseX::Declare;
use core::task qw(execute);

# Webserver SSL task
class Webserver_SSL extends Task {
    use LWP::UserAgent;
    use HTML::TreeBuilder;
    use XML::Simple;

    # Process
    method _process(Str $target, Str $proto, Int $timeout) {
        my $host = "$proto://$target";
        my $url = q[http://www.ssllabs.com/ssltest/analyze.html?d=___URL___&ignoreMismatch=on];
        $url =~ s/___URL___/$host/;

        my $sp = $/;
        undef $/;

        my $ua = LWP::UserAgent->new;
        $ua->timeout($timeout);
        my $response = $ua->get($url);

        unless ($response->is_success) {
            $self->_write_result($response->status_line);
            return;
        }

        my $content = $response->decoded_content;

        if (
            ($content =~ m/Assessment failed/sm) ||
            ($content =~ m/Unable&#32;to&#32;connect/sm)
        ) {
            $self->_write_result("Network error: SSL testing for $host cannot be completed for unknown reason");
            return;
        }

        $content =~ s/^(.+)?<div class=\"sectionTitle\">Details<\/div>//ms;
        $content =~ s/<div id=\"pageEnd\">.+$//ms;
        $content =~ s/&nbsp;/ /g;
        $/ = $sp;

        my @cont = split(m/[\r\n]+/, $content);
        my ($fl, @tables, $cur);

        $fl = 0;

        map {
            $cur = $_;

            if ($cur =~ m/<tbody>/) {
                $fl = 1;
            }

            if ($cur =~ m/<\/tbody>/) {
                $fl = 0;
            }

            if (($fl == 1) && ($cur !~ m/<tbody>/) && ($cur !~ m/<\/tbody>/)) {
                $cur =~ s/^\s+//;
                $cur =~ s/\s+$//;
                push(@tables, $cur) if ($cur =~ m/\S/);
            }
        } @cont;

        my $xml = HTML::TreeBuilder->new_from_content(join('', @tables))->as_XML();
        my $xout = XML::Simple->new();
        my $res = $xout->XMLin($xml);

        no warnings;

        map {
            $cur = $_;
            my @set = @{ $_->{'td'} };
            my ($lbl_1, $lbl_2,);

            if (exists $set[0]->{'font'}) {
                $lbl_1 = $set[0]->{'font'}{'content'};
                $lbl_2 = $set[1]->{'font'}{'content'};

                if ($set[0]->{'class'} eq 'tableLabel') {
                    $lbl_1 = $set[0]->{'font'}{'content'};
                }

                if ($set[1]->{'class'} eq 'tableCell') {
                    if (exists $set[1]->{'font'}{'b'}{'content'}) {
                        $lbl_2 = $set[1]->{'font'}{'b'}{'content'};
                    } else {
                        $lbl_2 = $set[1]->{'b'}{'content'};
                    }
                }
            } else {
                $lbl_1 = $set[0]->{'content'};
                $lbl_2 = $set[1]->{'content'};
                $lbl_1 = $set[0]->{'code'} if (exists $set[0]->{'code'});
                $lbl_2 = $set[1]->{'code'} if (exists $set[1]->{'code'});
            }

            $lbl_1 =~ s/^\s+//;
            $lbl_1 =~ s/\s+$//;
            $lbl_2 =~ s/^\s+//;
            $lbl_2 =~ s/\s+$//;

            if ($lbl_1 && $lbl_2) {
                $self->_write_result($lbl_1 . ': ' . $lbl_2);
            }
        } @{ $res->{'body'}{'table'}{'tr'} };
    }

    # Main function
    method main($args) {
        my $timeout = $self->_get_int($args, 0, 60);
        $self->_process($self->target, $self->proto || "http", $timeout);
    }

    # Test function
    method test {
        $self->_process("google.com", "http", 60);
    }
}

execute(Webserver_SSL->new());
