#!perl

use File::Spec;
use strict;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $host  = &getinput( $ARGV[0] );
my $outfile = $ARGV[1];
my $ports = &getinput( $ARGV[2] );
my $tmout = &getinput( $ARGV[3] );
open(OUTFILE, ">>$outfile");

$tmout    .= 'ms'; # time units are crucial here

# my $nexe	= &find_exe();
#
# if ( $nexe =~ m/\S+/ ){
#   print q[nmap utility's found here: ],q['], $nexe,q['],"\n";
# }
#
# my $path = $nexe;
# $path =~ s/nmap\.exe$//;
#
# chdir( $path );

open( READ, "nmap  -sT -P0 --max_rtt_timeout $tmout -p $ports $host |" );
while(<READ>){ print OUTFILE $_;}
close(READ);
close(OUTFILE);
exit(0);

# sub find_exe {
#
#     my $exe_to_find = 'nmap.exe';
#
#     local ($_);
#     local (*DIR);
#
#     for my $dir ( File::Spec->path() ) {
#         opendir( DIR, $dir ) || next;
#         my @files = ( readdir(DIR) );
#         closedir(DIR);
#
#         my $path;
#         for my $file (@files) {
#
#             next unless ( $file eq $exe_to_find );
#
#             $path = File::Spec->catfile( $dir, $file );
#             next unless -r $path && ( -x _ || -l _ );
#
#             return $path;
#             last DIR;
#
#         }
#
#     }
#
# }

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	#return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
