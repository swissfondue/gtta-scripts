#!perl

use strict;

# nslookup -type=txt -cl=chaos version.bind. muenchow.ch
unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my (@target, $out);

@target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
open(OUTFILE, ">>$outfile");

undef $/;
my $class = 'chaos';

while (1)
{
    open( READ, "nslookup -type=txt -cl=$class version.bind $target[0] |" );
    $out = <READ>;
    close(READ);

    if ($class eq 'chaos' && $out =~ m/got version.bind\/TXT\/IN/si)
    {
        print OUTFILE "Possible misconfiguration - expects version.bind in IN-class record.\n\n";
        $class = 'in';
        next;
    }

    last;
}

print OUTFILE $out;
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
