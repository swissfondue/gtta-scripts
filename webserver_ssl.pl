#!perl
# tried -
# normal (a) test: siam.org
# failed test: bn.com
# normal (b) test: verio.com
# 'ignoreMismatch': muenchow.ch

use Data::Dumper;
use LWP::UserAgent;
use HTML::TreeBuilder;
use XML::Simple;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };
my @timeout;
$timeout[0]	= 255;

my @domain	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
@timeout	= &getinput( $ARGV[2] ) if ( $ARGV[2] );
open(OUTFILE, ">>$outfile");

my $target	= q[http://www.ssllabs.com/ssltest/analyze.html?d=___URL___&ignoreMismatch=on];
$target		=~ s/___URL___/$domain[0]/;

my $sp = $/;
undef $/;

my $ua = LWP::UserAgent->new;

$ua->timeout( $timeout[0] );
my $response = $ua->get( $target );

unless ($response->is_success) {

   print OUTFILE $response->status_line;
   close(OUTFILE);
   exit(0);

}

my $content = $response->decoded_content;

if(
  ( $content =~ m/Assessment failed/sm ) or
  ( $content =~ m/Unable&#32;to&#32;connect/sm )
){ print OUTFILE qq[Network error: SSL testing for $domain[0] cannot be completed for unknown reason\n]; exit(0); } # bn.com

$content 	=~ s/^(.+)?<div class=\"sectionTitle\">Details<\/div>//ms;
$content 	=~ s/<div id=\"pageEnd\">.+$//ms;
$content 	=~ s/&nbsp;/ /g;
$/ = $sp;

my @cont = split( m/[\r\n]+/, $content );

my ( $fl, @tables, );

map {

  my $cur = $_;
  if ( $cur =~ m/<tbody>/ ){ $fl = 1; }
  if ( $cur =~ m/<\/tbody>/ ){ $fl = 0; }
  if( ( $fl == 1 ) and
  ( $cur !~ m/<tbody>/ ) and
  ( $cur !~ m/<\/tbody>/ ) ) {

	$cur =~ s/^\s+//;
	$cur =~ s/\s+$//;
	push @tables, $cur if( $cur =~ m/\S/ );

  }

} @cont;

my $xml 	= HTML::TreeBuilder->new_from_content( join( '', @tables ) )->as_XML();
my $xout 	= XML::Simple->new();
my $res    	= $xout->XMLin( $xml );
# print Dumper $res->{'body'}{'table'}{'tr'}; die;
no warnings;
map {
	  my $cur = $_; #print Dumper $cur;
	  my @set = @{ $_->{'td'} };

	  my ( $lbl_1, $lbl_2, );

	  if ( exists $set[0]->{'font'} ) {

		$lbl_1 = $set[0]->{'font'}{'content'};
		$lbl_2 = $set[1]->{'font'}{'content'};

		if ( $set[0]->{'class'} eq 'tableLabel' ){

		  $lbl_1 = $set[0]->{'font'}{'content'};


		}

		if ( $set[1]->{'class'} eq 'tableCell' ){

		  if ( exists $set[1]->{'font'}{'b'}{'content'} ){

			$lbl_2 = $set[1]->{'font'}{'b'}{'content'};

		  }
		  else { $lbl_2 = $set[1]->{'b'}{'content'}; }

		}

	  }
	  else{

		$lbl_1 = $set[0]->{'content'};
		$lbl_2 = $set[1]->{'content'};
		$lbl_1 = $set[0]->{'code'} if( exists $set[0]->{'code'} );
		$lbl_2 = $set[1]->{'code'} if( exists $set[1]->{'code'} );

	  }

	  $lbl_1 =~ s/^\s+//;
	  $lbl_1 =~ s/\s+$//;
	  $lbl_2 =~ s/^\s+//;
	  $lbl_2 =~ s/\s+$//;

	  print OUTFILE $lbl_1, ': ',$lbl_2, "\n" if ( $lbl_1 and $lbl_2 );

} @{ $res->{'body'}{'table'}{'tr'} };

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }
	close( IN );
	return @fo;# if ( scalar @fo > 1 );
	#return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
