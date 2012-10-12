#!perl

use strict;
use Net::Whois::IANA;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my @target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];

open(OUTFILE, ">>$outfile");

my $hostname = $target[0];
my $ip       = '';
if ($hostname =~ /^[\d\.]+$/)
{
    $ip = $hostname;
}
else
{
    $ip = &hostname($hostname);
}

my $iana	= new Net::Whois::IANA;

eval {

	  $iana->whois_query(-ip => $ip );
	  my $result = $iana->fullinfo();

	  if ($result) {

		  print OUTFILE 'report for ',$hostname,' (', $ip, ')',"\n";
		  print OUTFILE $result;

	  }
	  else { print OUTFILE "Error: $hostname WHOIS lookup failed.\n"; }

};

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

sub hostname {

  my ( @bytes, @octets, $packedaddr, $raw_addr, $host_name, $ip );

  if( $_[0] =~ /[a-zA-Z]/g ) {

     $raw_addr		= ( gethostbyname( $_[0] ) )[4];
     @octets		= unpack('C4', $raw_addr);
     $host_name 	= join('.', @octets);

  }
  else {

     @bytes			= split(/\./, $_[0]);
     $packedaddr	= pack('C4',@bytes);
     $host_name		= ( gethostbyaddr( $packedaddr, 2 ) )[0];

  }

  return $host_name;

};
