use LWP::UserAgent;
use warnings;
use Net::SSL (); 

my @target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
my @lines   = &getinput( $ARGV[2] ) if ( $ARGV[2] );

open(OUTFILE, ">>$outfile");

my $host = $target[0];
my $protocol = $target[1];
my $port = $target[2];

if (!$protocol)
{
    $protocol = 'http';
}

if (!$port)
{
    $port = 80;
}

foreach $line (@lines)
{
my $request = new LWP::UserAgent;
$request->default_header(
"User-Agent" => "Mozilla/5.0 (Windows; U; Windows NT 5.2; de; rv:1.9.2.16) Gecko/20110319 Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; DigExt) ( .NET CLR 3.5.30729))", 
"accept" => "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
"Accept-Language" => "de-de,de;q=0.8,en-us;q=0.5,en;q=0.3", 
"Accept-Encoding" => "gzip,deflate", 
"Accept-Charset" => "ISO-8859-1,utf-8;q=0.7,*;q=0.7", 
"Keep-Alive" => "115", 
"Connection" => "keep-alive", 
"Referer" => "http://its.me.oliver"
);
my $output = $request->get("$protocol://$host:$port/$line ");
my $code = $output->code;
my $size = length ($output->content);
if ( $code == 200) 
{
print OUTFILE "Possible File found here: $protocol://$host:$port/$line  \t SIZE $size \t CODE:";
print OUTFILE $output->status_line . "\n";    
    
}

}

close(OUTFILE);
exit(0);

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ chomp; push @fo, $_; }

	close( IN );

	return @fo; # if ( scalar @fo > 1 );
	# return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
