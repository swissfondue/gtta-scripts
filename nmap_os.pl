#!perl

use File::Spec;
use File::Temp;
use XML::LibXML;
use strict;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $host  = &getinput( $ARGV[0] );
my $outfile = $ARGV[1];
my $skip_discovery = &getinput( $ARGV[2] ) if ($ARGV[2]);
my $verbose = &getinput( $ARGV[3] ) if ($ARGV[3]);
my @data;

if (defined($timing) && !grep $_ == $timing, qw/0 1 2 3 4 5/)
{
    print q[Error: timing must be within 0..5 range], "\n";
    exit(0);
}

open(OUTFILE, ">>$outfile");

my $nmap_cmd = "nmap -O " . ($skip_discovery ? '-PN ' : '') . ($verbose ? '-v ' : '') . "$host |";

undef $/;

open( READ, $nmap_cmd );
my $output = <READ>;
close(READ);

print OUTFILE $output;

close(OUTFILE);

File::Temp::cleanup();

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ chomp; push @fo, $_; }

	close( IN );

	#return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
