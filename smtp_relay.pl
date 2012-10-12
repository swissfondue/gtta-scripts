#!perl
use Data::Dumper;
use strict;
use Net::SMTP;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my ( @target, $mail_from, $mail_to, @timeout, $smtp, ) = ( undef, 'aaa@mail.ru', 'bbb@mail.ru', 60, undef );

@target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
@timeout= &getinput( $ARGV[2] ) if ( $ARGV[2] );
my @mbfrom = &getinput( $ARGV[3] ) if ( $ARGV[3] );
my @mbto   = &getinput( $ARGV[4] ) if ( $ARGV[4] );

open(OUTFILE, ">>$outfile");

$mail_from = $mbfrom[0];
$mail_to   = $mbto[0];

my $srvr = $target[0];

if ( $smtp = Net::SMTP->new( $srvr, 'Debug'  => 0, 'Timeout' => $timeout[0] ) ) {

    print OUTFILE qq[OK: server $srvr connect successful\n];

    $smtp->mail( $mail_from );
    $smtp->to( $mail_to );
    my $ok = $smtp->data( ".\r\n" );

    print OUTFILE qq[OK: test data accepted for mailing\n] if $ok;

} else { print OUTFILE qq[NOT OK: server $srvr connect failed\n] }

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
