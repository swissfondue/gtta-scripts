#!perl

use strict;
use Data::Dumper;
use Net::DNS;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
my $option	= &getinput( $ARGV[2] ) if ( $ARGV[2] );

open(OUTFILE, ">>$outfile");

my ($dom, $my_tld) = split/\./,$target->[0];

my $tld 	= 'dns_top_tlds_files/short_tld.txt'; # '0' - short, '1' - long TLD list
$tld 		= 'dns_top_tlds_files/tld.txt' if ( $option == 1 );
my $tlds	= &getinput( $tld );

my $res   	= Net::DNS::Resolver->new;

undef $/;

map {

	my $cur   = $_;
	unless ( $cur eq $my_tld )
    {
        my $cur_domain = $dom . '.' . $cur;

        my $query = $res->search( $cur_domain );
        if ( $query ) {

            foreach my $rr ($query->answer) 
            {
                next unless $rr->type eq 'A';

                open(READ, "whois $cur_domain |" );
                my $whois = <READ>;
                close(READ);

                my $whois_link = "http://whois.domaintools.com/$cur_domain";

                if ($whois =~ /Company:(?: +)?([^\n]+)\n/si || $whois =~ /Organi[sz]ation:(?: +)?([^\n]+)\n/si || $whois =~ /Name:(?: +)?([^\n]+)\n/si)
                {
                    $whois = $1;
                }
                else
                {
                    $whois = 'N/A';
                }

                print OUTFILE $cur_domain, "\t",$rr->address, "\t", "$whois\t$whois_link\n";
                last;
            }
        }
	}

} @{ $tlds };

close(OUTFILE);

exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ next unless m/^[a-z]/i; s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
