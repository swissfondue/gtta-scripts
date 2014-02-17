# Typosquatting
# --

use MooseX::Declare;
use core::task qw(execute);
use core::resulttable;

# Typosquatting task
class Typosquatting extends Task {
    use constant TIMEOUT => 3600;
    use Net::DNS;

    # generate typos
    method _keyslips(Str $name) {
        my @parts = split/\./, $name;
        my @set	= split //, $parts[0];
        my @res;

        # missing
        map {
            my $cur = $_;
            my @this = @set;
            splice(@this, $cur, 1);
            push @res, join( '', @this );
        } (0 .. $#set);

        # doubled
        map {
            my $cur = $_;
            my @this = @set;
            $this[ $cur ] .= $this[ $cur ];
            push @res, join('', @this);
        } ( 0 .. $#set );

        # swapped
        map {
            my $cur = $_;
            my @this = @set;

            if ($cur < $#set){
                ( $this[ $cur ], $this[ $cur +1 ]  ) = ( $this[ $cur +1 ], $this[ $cur ]  );
                push @res, join( '', @this );
            }
        } ( 0 .. $#set );

        # slipped
        my @abc	= ( 'a' .. 'z' );

        map {
            my $cur = $_;
            my @this = @set;

            map {
                $this[ $cur ] = $_;
                push @res, join( '', @this );
            } @abc;
        } ( 0 .. $#set );

        # look alikes
        my %looks = ( 'l' => 1, 'o' => 0, 'a' => 4, 4 => 'a', 0 => 'o', 1 => 'l' );

        map {
            my $cur = $_;
            my @this = @set;
            $this[ $cur ] = $looks{ $this[ $cur ] } if ( exists $looks{ $this[ $cur ] } );
            push @res, join( '', @this );
        } ( 0 .. $#set );

        # extra hyphens
        map {
            my $cur = $_;
            my @this = @set;

            if ( $cur < $#set and $cur > 0 ) {
                unless ( ( $this[ $cur +1 ] eq '-' ) or ( $this[ $cur -1 ] eq '-' ) ) {
                    $this[ $cur ] = '-' . $this[ $cur ];
                    push @res, join( '', @this );
                }
            }
        } ( 0 .. $#set );

        # missing hyphens
        map {
            my $cur = $_;
            my @this = @set;

            if ( $this[ $cur ] eq '-' ) {
                delete $this[ $cur ];
                push @res, join( '', @this );
            }
        } ( 0 .. $#set );

        # make unique name list
        my %squiz;
        @squiz{ @res } = ();

        # append TLDs
        my ( %res, );
        my @tlds	= ( $parts[1] );

        map {
            my $nm = $_;
            map { $res{ $nm . '.' . $_ } = undef; } @tlds;
        } keys %squiz;

        return \%res;
    }

    # Process
    method _process(Str $target, Int $timeout, Int $maxres, Int $mode) {
        my (@data, @set);

        @set = split //, $target;

        if (
            ($target =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/) &&
            (@set >= 3)
        ) {
            my $doms = $self->_keyslips($target);

            if ($mode) {
                my @lst = (keys %$doms);
                splice(@lst, $maxres);

                my $res = Net::DNS::Resolver->new;
                $res->tcp_timeout($timeout);

                map {
                    my $host = $_;
                    my $query = $res->search($host);

                    if ($query) {
                        foreach my $rr ($query->answer) {
                            next unless $rr->type eq "A";
                            push(@data, [ $host, $rr->address ]);
                        }
                    }
                } @lst;
            } else {
                map { push(@data, [ $_ ]); } sort { $a cmp $b } keys %{ $doms };
            }
        } else {
            $self->_write_result("Error: target must be 3+ symbols in length.");
            return;
        }

        if (scalar(@data) > 0) {
            my $table;

            if ($mode) {
                $table = ResultTable->new(columns => [
                    {name => "Domain", width => "0.5"},
                    {name => "IP", width => "0.5"},
                ]);
            } else {
                $table = ResultTable->new(columns => [
                    {name => "Domain", width => "1"},
                ]);
            }

            for (my $i = 0; $i < scalar(@data); $i++) {
                my $row = [];

                for (my $k = 0; $k < scalar(@{$data[$i]}); $k++) {
                    $data[$i][$k] =~ s/</&lt;/g;
                    $data[$i][$k] =~ s/>/&gt;/g;
                    $data[$i][$k] =~ s/&/&amp;/g;

                    push(@$row, $data[$i][$k]);
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
        my ($timeout, $maxres, $mode);

        $timeout = $self->_get_int($args, 0, 120);
        $maxres = $self->_get_int($args, 1, 100);
        $mode = $self->_get_int($args, 2, 0);

        $self->_process($self->target, $timeout, $maxres, $mode);
    }

    # Test function
    method test {
        $self->_process("google.com", 120, 10, 1);
    }
}

execute(Typosquatting->new());