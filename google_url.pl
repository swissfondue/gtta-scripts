#!perl

use strict;
use URI;
use REST::Google;

# inurl:bankclient
# http://www.google.com/search?ix=acb&sourceid=chrome&ie=UTF-8&q=inurl%3Abankclient
# http://www.google.com/search?q=inurl:bankclient&hl=en
# http://www.google.com/search?q=inurl:bankclient&hl=en&start=10
# https://www.google.com/search?q=inurl:bankclient&num=100&hl=en&start=100
# </head> <div id="botstuff">

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my @str	= &getinput( $ARGV[0] ) if ( $ARGV[0] ); # MUST (!) look like 'ebay.com'
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

# set service to use
REST::Google->service('http://ajax.googleapis.com/ajax/services/search/web');

# provide a valid http referer
REST::Google->http_referer('http://google.com');

my $seen;
my @set	  = split/\./,$str[0];
my $token = $set[0];
my $res = REST::Google->new( 'q' => 'inurl:' . $token );
my $rsp = $res->responseStatus;

print OUTFILE "response status failure: $rsp\n" if $rsp != 200;

my $data = $res->responseData;

# print
#
# 'resultCount: ', $data->{'cursor'}{'resultCount'},"\n",
# 'moreResultsUrl: ', $data->{'cursor'}{'moreResultsUrl'},"\n",
# 'estimatedResultCount: ', $data->{'cursor'}{'estimatedResultCount'},"\n",
# 'URLs found for comparision',"\n--------------------\n";

my $curl = $data->{'cursor'}{'moreResultsUrl'};

my @pg;
my @pgs = @{ $data->{'cursor'}{'pages'} };
map {

  my $cur = $_;
  push @pg, $cur->{'start'} if ( $cur->{'start'} > 0 );

} @pgs;


my @set = @{ $data->{'results'} };

map {

  my $cur = $_;

  if (not $cur->{'visibleUrl'} =~ m!^http://.*!) {
	$cur->{'visibleUrl'} = "http://$cur->{'visibleUrl'}";
  }

  my $uri = URI->new( $cur->{'visibleUrl'} );
  my $dom = $uri->host;

  if ( $dom =~ m/[^\/]+\Q$token\E/ ) {

	$dom =~ s/^(http:\/\/[^\/]+)\/.*$/$1/;

	  unless( URI::eq( $str[0], $dom ) ){

		print OUTFILE $dom,"\n" unless ( exists $seen->{ $dom } );
		$seen->{ $dom }++;

	  }

	}

} @set;

if ( @pg > 0 ) {

  map{
	  my $start = $_; # print 'processing page: ', $start,"\n";

	  my $res = REST::Google->new( 	'hl' 		=> 'en' ,
									'oe' 		=> 'utf8',
									'ie' 		=> 'utf8',
									'source' 	=> 'uds',
									'start' 	=> $start,
									'q' 		=> 'inurl:' . $token );

	  print OUTFILE "response status failure" if $res->responseStatus != 200;
	  # http://www.google.com/search?oe=utf8&ie=utf8&source=uds&start=0&hl=en&q=inurl:bankclient

	  my $data = $res->responseData;

	  my @set = @{ $data->{'results'} };

	  map {

		my $cur = $_;

		if (not $cur->{'visibleUrl'} =~ m!^http://.*!) {
		  $cur->{'visibleUrl'} = "http://$cur->{'visibleUrl'}";
  		}

		my $uri = URI->new( $cur->{'visibleUrl'} );
		my $dom = $uri->host;

		if ( $dom =~ m/[^\/]+\Q$token\E/ ) {

		  $dom =~ s/^(http:\/\/[^\/]+)\/.*$/$1/;

		  unless( URI::eq( $str[0], $dom ) ){

			print OUTFILE $dom,"\n" unless ( exists $seen->{ $dom } );
			$seen->{ $dom }++;

		  }

	  	}

	  } @set;

  } @pg

}

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	return @fo; # if ( scalar @fo > 1 );
	#return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};