#!perl

use strict;
use Data::Dumper;
use Net::DNS;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

my $dns		= Net::DNS::Resolver->new;
my $answer	= $dns->search( $target, 'TXT');

if ( $answer ) {

	foreach my $rr ($answer->answer) {

		my $spf = lc($rr->txtdata);

		if ( $spf=~ m/v\=spf/ ) {

			print OUTFILE "SPF record: $spf\n";

		}

	}

}
else { print OUTFILE 'Error: could not get NS record',"\n"; }

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ next unless m/^[a-z]/i; s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	#return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
