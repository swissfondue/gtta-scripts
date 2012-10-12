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

my ($dns, @zone, @domain_ns, $search, $dns_server, );

$dns = $target;

my $res = Net::DNS::Resolver->new;
my @search_strings = split(/\x2C/, $search) if $search;
my $query          = $res->query($dns, 'NS');

if ($query) {
  output("DNS Servers for $dns:");
  foreach my $rr (grep { $_->type eq 'NS' } $query->answer) {
    my $dnssrv = $rr->nsdname;
    output("\t$dnssrv");
    push (@domain_ns, $rr->nsdname);
  }
}

if ($dns_server) {
  @zone = $res->axfr($dns);
} else {
  for (@domain_ns) {
    $res->nameservers($_);
    output("\tTesting $_");
    @zone = $res->axfr($dns);
    @zone ? last : output("\t\tRequest timed out or transfer not allowed.");
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
