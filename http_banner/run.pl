#!perl
use HTTP::Request;
use LWP::UserAgent;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my @target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
my @urlPath = &getinput( $ARGV[2] ) if ( $ARGV[2] );
my $urlPath;

if (@urlPath && $urlPath[0])
{
    $urlPath = $urlPath[0];
}

$urlPath = '/' unless ($urlPath);

if (substr($urlPath, 0, 1) ne '/')
{
    $urlPath = '/' . $urlPath;
}

open(OUTFILE, ">>$outfile");

my $ua 		= LWP::UserAgent->new;

# protocol
if (!$target[1])
{
    $target[1] = 'http';
}

my $request		= HTTP::Request->new( GET => $target[1] . '://' . $target[0] . $urlPath);
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
