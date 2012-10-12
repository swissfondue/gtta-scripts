#!perl

# typo squatting generator

use Data::Dumper;
use strict;
use Net::DNS;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my ( @target, @timeout, @maxres, @mode );# = ( undef, 120, 100, 0 ); # defaults

@target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
@timeout= &getinput( $ARGV[2] ) if ( $ARGV[2] );
@maxres	= &getinput( $ARGV[3] ) if ( $ARGV[3] );
@mode	= &getinput( $ARGV[4] ) if ( $ARGV[4] );

open(OUTFILE, ">>$outfile");

my @set = split//, $target[0];

if (
	( $target[0] =~ m/^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$/ ) and
	( @set >= 3 )
) {

	my $doms = &keyslips( $target[0] );

	if ( $mode[0] ){

	  my @lst = ( keys %{ $doms } );
	  splice( @lst, $maxres[0] );

	  my $res = Net::DNS::Resolver->new;
	  $res->tcp_timeout( $timeout[0] );

	  map {

		  my $host = $_;

		  my $query = $res->search( $host );

		  if ( $query ) {

			  foreach my $rr ($query->answer) {

				  next unless $rr->type eq "A";
				  print OUTFILE $host,"\t\t\t", $rr->address, "\n";

			  }

		  }

	  } @lst;

	}
	else { map { print OUTFILE $_,"\n"; } sort { $a cmp $b } keys %{ $doms }; }

}
else { print OUTFILE 'Error: target must be 3+ symbols in length', "\n"; exit(0); }

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

#-------------------------------------------------------------------------------
#   keyboard slips
#   missing letters
#   double letters
#   letter swapping
#   look alikes (l - 1, o - 0, a - 4)
#   extra or missing hyphens
# com, .net, .org, .biz, .us, and .info (can be extended at wish)
#-------------------------------------------------------------------------------
sub keyslips {

  my $name	= shift; # ebay.com
  my @parts	= split/\./, $name;
  my @set	= split//, $parts[0]; # no TLD here

  my ( @res, );

  # missing
  map {

	  my $cur = $_;
	  my @this = @set;
	  delete $this[ $cur ];
	  push @res, join( '', @this );

  } ( 0 .. $#set );

  # doubled
  map {

	  my $cur = $_;
	  my @this = @set;
	  $this[ $cur ] .= $this[ $cur ];
	  push @res, join( '', @this );

  } ( 0 .. $#set );

  # swapped
  map {

	  my $cur = $_;
	  my @this = @set;

	  if ( $cur < $#set ){

		( $this[ $cur ], $this[ $cur +1 ]  ) = ( $this[ $cur +1 ], $this[ $cur ]  );
		push @res, join( '', @this );

	  }

  } ( 0 .. $#set );

  # slipped
  my @abc	= ( 'a' .. 'z' );
  map {

	  my $cur = $_;
	  my @this = @set;

	  map {

		$this[ $cur ] = $_;
		push @res, join( '', @this );

	  } @abc;

  } ( 0 .. $#set );

  # look alikes
  my %looks = ( 'l' => 1, 'o' => 0, 'a' => 4, 4 => 'a', 0 => 'o', 1 => 'l' );
  map {

	  my $cur = $_;
	  my @this = @set;
	  $this[ $cur ] = $looks{ $this[ $cur ] } if ( exists $looks{ $this[ $cur ] } );
	  push @res, join( '', @this );

  } ( 0 .. $#set );

  # extra hyphens
  map {

	  my $cur = $_;
	  my @this = @set;

	  if ( $cur < $#set and $cur > 0 ) {

		unless ( ( $this[ $cur +1 ] eq '-' ) or ( $this[ $cur -1 ] eq '-' ) ) {

		  $this[ $cur ] = '-' . $this[ $cur ];
		  push @res, join( '', @this );

		}

	  }

  } ( 0 .. $#set );

  # missing hyphens
  map {

	  my $cur = $_;
	  my @this = @set;

	  if ( $this[ $cur ] eq '-' ){

		delete $this[ $cur ];
		push @res, join( '', @this );

	  }

  } ( 0 .. $#set );

  # make unique name list
  my %squiz;
  @squiz{ @res } = ();

  # append TLDs
  my ( %res, );
  # my @tlds	= ( 'com', 'net', 'org', 'biz', 'us', 'info' );
  my @tlds	= ( $parts[1] );
  map {

	  my $nm = $_;
	  map { $res{ $nm . '.' . $_ } = undef; } @tlds;

  } keys %squiz;

  return \%res;

};
