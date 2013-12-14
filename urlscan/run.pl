use LWP::UserAgent;
use warnings;
use strict;

my @target	= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
my @inputlistfile = &getinput( $ARGV[2] ) if ( $ARGV[2] );

open(OUTFILE, ">>$outfile");

if (!$target[1])
{
    $target[1] = 'http';
}

my $targeturl = $target[1] . '://' . $target[0];

#	print "Timeout is at 5 seconds for each attempt. Please wait...\n";
foreach my $line (@inputlistfile)
{
    my $request = new LWP::UserAgent;	
#		 $request->timeout(5);
    my $output = $request->get("$targeturl/$line");
    if($output->is_success) 
    {
        print OUTFILE "FOUND: $targeturl/$line\n";		
    } 
    else
    {
#		print "nothing found under $targeturl$line\n";
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

