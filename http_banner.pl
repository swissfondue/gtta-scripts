#!perl
use HTTP::Request;
use LWP::UserAgent;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my @target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

my $ua 		= LWP::UserAgent->new;

# protocol
if (!$target[1])
{
    $target[1] = 'http';
}

my $request		= HTTP::Request->new( GET => $target[1] . '://' . $target[0] );
my $response	= $ua->request( $request );

print OUTFILE $response->dump(), "\n";

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
