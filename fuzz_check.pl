#!perl
use strict;
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Response;
use Data::Dumper;
my $def = new LWP::UserAgent;
my $ua = LWP::UserAgent->new( 'agent' => "Log", 'env_proxy' => 1, 'keep_alive' => 1,'timeout' => 1 );
my @database=("http://HOST/FUZZ/\n");
my ($cnt, $found) = ( 0, 0 );

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };
my @target		= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
my @fuzzz		= &getinput( 'fuzz_check_files/fuzz.txt' );

open(OUTFILE, ">>$outfile");

my $host = $target[0];

foreach my $fuzz ( @fuzzz ) {

foreach (@database) {

  my $url = $_;
  $url =~ s/FUZZ/$fuzz/;
  $url =~ s/HOST/$host/;

  my $request = new HTTP::Request( 'GET' => $url );
  my $response = $def->request($request);
  if ($response->is_success) {

	print OUTFILE 'with this URL ', $url, ' obtained this: ',
	"\n----------------------START-----------------------------\n",
	 $response->decoded_content,
	"\n----------------------END-------------------------------\n";

	$found++;

  }

  

}
	$cnt++;# print $cnt,"\n";

}

print OUTFILE 'tried ', $cnt, ' time(s) with ', $found, ' successful time(s)',"\n";

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(.+)$/{ push @fo, $1; }/e; }

	close( IN );

	return @fo; # if ( scalar @fo > 1 );
	# return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};