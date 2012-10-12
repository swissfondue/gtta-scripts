#!perl
use strict;
use Net::DNS;

my $host    = &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

my $res   = Net::DNS::Resolver->new;
my $query = $res->search( $host );

if ( $query ) {

	foreach my $rr ($query->answer) {

		next unless $rr->type eq "A";
		print OUTFILE $rr->address, "\n";

	}
}
else { warn "query failed: ", $res->errorstring, "\n"; }

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){  s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	# return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};