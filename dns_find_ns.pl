#!perl
use strict;
use Net::DNS;
use Socket;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my ( $target, $timeout, $debug, $outfile ) = ( undef, 120, 0, undef ); # defaults

$target	 = &getinput( $ARGV[0] ) if ( $ARGV[0] );
$outfile = $ARGV[1];
$timeout = &getinput( $ARGV[1] ) if ( $ARGV[1] );
$debug	 = &getinput( $ARGV[2] ) if ( $ARGV[2] );

open(OUTFILE, ">>$outfile");

  my $res = Net::DNS::Resolver->new( 'debug' => $debug );
  my $cnt = 1;

my $host  = $target;
unless ( $host =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/ ) {

print OUTFILE "\n", $cnt++, ') Error: not valid domain name ', $host, "\n";

}
else{

$host =~ s/^www\.//;

$res->tcp_timeout( $timeout );
my $query = $res->query( $host, 'NS' );

if ( $query ) {

	foreach my $rr ( grep { $_->type eq 'NS' } $query->answer ) {

		print OUTFILE $rr->nsdname, ' (', &hostname( $rr->nsdname ), ")\n";

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

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	#return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};

sub hostname {

  my ( @bytes, @octets, $packedaddr, $raw_addr, $host_name, $ip );

  if( $_[0] =~ /[a-zA-Z]/g ) {

     $raw_addr		= ( gethostbyname( $_[0] ) )[4];
     @octets		= unpack('C4', $raw_addr);
     $host_name 	= join('.', @octets);

  }
  else {

     @bytes			= split(/\./, $_[0]);
     $packedaddr	= pack('C4',@bytes);
     $host_name		= ( gethostbyaddr( $packedaddr, 2 ) )[0];

  }

  return $host_name;

};
