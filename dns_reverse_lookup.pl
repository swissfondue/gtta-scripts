#!perl

use strict;
use Net::DNS;
use Net::IP;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $target  = &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

my $res = Net::DNS::Resolver->new;

if ( $target) {

  my @ranges = split /\s+/, $target;

  foreach my $t (@ranges)
  {
      $t =~ s/^\s+//gi;
      $t =~ s/\s+$//gi;

    my $ip = new Net::IP ( $t );

    do {
        unless ($ip)
        {
            print OUTFILE 'Invalid IP or range: ' . $t;
            next;
        }

        my $IP = $ip->ip();
        my $target_IP = join('.', reverse split(/\./, $IP)).'.in-addr.arpa';
        my $query = $res->query( $target_IP, 'PTR' );

        if ( $query ) {

            my $found = 0;

            foreach my $rr ( $query->answer ) 
            {
                next unless ($rr->type eq 'PTR');
                print OUTFILE $IP,"\t\t",$rr->rdatastr, "\n";
                $found = 1;
            }

            print OUTFILE $IP, "\t\tN/A\n" unless ($found);
        }
        else { print OUTFILE $IP, "\t\tN/A\n"; }

    } while (++$ip);
  }
}
else { print OUTFILE 'Error: no IP range is provided', "\n"; }

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){  chomp; push @fo, $_; }

	close( IN );

	# return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
