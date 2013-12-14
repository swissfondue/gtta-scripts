#!perl

use Data::Dumper;
use LWP::UserAgent;
use HTML::LinkExtor;
use URI::URL;
use HTTP::Request;

my ( @url, %done, $ua, $parser, $top, $base, $cnt, );
unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

$cnt	= 1;
# $url 	= q[http://artline.in.ua]; #  http://mir-skazki.org/
@url	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

if (!$url[1])
{
    $url[1] = 'http';
}

$ua		= LWP::UserAgent->new;
$ua->timeout( 55 );

$parser = HTML::LinkExtor->new;
$top    = $ua->request( HTTP::Request->new( 'HEAD' => $url[1] . '://' . $url[0] ) );
$base   = $top->base;

# callback to collect links
my @ahref;

sub callback {

   my($tag, %attr) = @_;
   return if $tag ne 'a';
   push( @ahref, values %attr );

};

&grab( URI::URL->new( $top->request->url ) );

# map { print $_,"\n" } sort { $a cmp $b } keys %done;
# print Dumper \%done;

close(OUTFILE);

exit(0);

sub grab {

  my $url 		= shift;
  my $path 		= $url->path;
  my $fixed_url = URI::URL->new($url->scheme . '://' . $url->netloc . $path);

  # return if $done{ $fixed_url }++;
  if ( $done{ $fixed_url }++ ) {

	return;

  }
  else { print OUTFILE $cnt++,') ',$fixed_url,"\n"; }

  # print q[printing links from page: ], $fixed_url, "\n";

  my $request	= HTTP::Request->new( 'GET' => $fixed_url );
  my $response	= $ua->request( $request );

  # if ($response->is_error()) { print $response->status_line, "\n"; }
  unless ($response->is_error()) {

	my $contents	= $response->content();
	$parser->parse( $contents )->eof;

	my @links	= $parser->links;
	my @hrefs 	= map { url( $_->[2], $base )->abs } @links;

	map {

	  my $url = $_;

	  if( &is_child( $base , $url ) ) {

		  # print "\t", $url,"\n";
		  &grab( $url );

	  }

	} @hrefs;

  }

};

 sub is_child {

  my ($base,$url) = @_;
  my $rel = $url->rel($base);
  return ($rel ne $url) && ($rel !~ m!^[/.]!);

};

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
