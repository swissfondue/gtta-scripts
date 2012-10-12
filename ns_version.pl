#!perl

use strict;
use Net::DNS;

# nslookup -type=txt -cl=chaos version.bind. muenchow.ch
unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my (@target, $out);

@target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
open(OUTFILE, ">>$outfile");

my $host = $target[0];

unless ( $host =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/ ) {

print OUTFILE 'Error: not valid domain name ', $host, "\n";

}
else
{
    $host =~ s/^www\.//;

    my $res = Net::DNS::Resolver->new();
    my $cnt = 1;

    undef $/;
    
    my $query = $res->query( $host, 'NS' );

    if ( $query ) {

        foreach my $rr ( grep { $_->type eq 'NS' } $query->answer ) {

            print OUTFILE $cnt++, ". ", $rr->nsdname, ":\n";

            my $class = 'chaos';
            my $target = $rr->nsdname;

            while (1)
            {
                
                open( READ, "nslookup -type=txt -cl=$class version.bind $target |" );
                $out = <READ>;
                close(READ);

                if ($class eq 'chaos' && $out =~ m/got version.bind\/TXT\/IN/si)
                {
                    print OUTFILE "Possible misconfiguration - expects version.bind in IN-class record.\n\n";
                    $class = 'in';
                    next;
                }

                last;
            }

            print OUTFILE $out;
            print OUTFILE "\n";
        }
    }
    else { print OUTFILE "\n", $cnt++, ') Error: no NS for domain ', $host, ' (', $res->errorstring, ")\n"; }

    
}

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ chomp; push @fo, $_; }

	close( IN );

	return @fo;# if ( scalar @fo > 1 );
	#return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};

