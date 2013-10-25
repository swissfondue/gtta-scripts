#!perl

use strict;
use Net::hostent;
use Net::DNS;
use IO::Socket;
use Socket;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

my (@zone, @domain_ns);

my $res = Net::DNS::Resolver->new;
my $query = $res->query($target, 'NS');

if ($query) {
    output("DNS Servers for $target:");

    foreach my $rr (grep { $_->type eq 'NS' } $query->answer) {
        my $dnssrv = lc($rr->nsdname);
        output(" - $dnssrv");
        push (@domain_ns, lc($rr->nsdname));
    }
} else {
    output("Please specify a domain name which DNS records should be tested.");
    exit(0);
}

output("\nTesting NS servers:");

for (@domain_ns) {
    $res->nameservers($_);
    @zone = $res->axfr($target);

    if (@zone) {
        output(" - $_: found " . scalar(@zone) . " records, AXFR is enabled");
    } else {
        output(" - $_: no response");
    }
}

exit(0);

close(OUTFILE);

sub output {
  my $text = shift;
  print OUTFILE "$text\n";
}

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
