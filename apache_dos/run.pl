#!perl
#
# [Author]
# Ryusuke Tsuda (InfoAlive Corp.)
# http://www.infoalive.com/
#
# --------------------------------------------------------------------
# [Description]
# This script can be used to test Apache can drop or reject many ranges
# http request against the Apache Range Header DOS(CVE-2011-3192).
#
# If your system use SetEnvIf or mod_rewrite to detect a large number
# of ranges, this script may be useful for testing.
#
# --------------------------------------------------------------------
# [Dependencies]
# This script needs libwww-perl module.
# You can download it here.
# http://search.cpan.org/~gaas/libwww-perl/
#
# Or if your system have yum command, you can install it by this command.
#
#   $root> yum install perl-libwww-perl
#
# Or you have cpan command, you can install by this command.
#
#   $root> cpan
#   > install LWP
#
# If you want to test https request, get Crypt::SSLeay module.
# http://search.cpan.org/~nanis/Crypt-SSLeay/
#
#---------------------------------------------------------------------
# [Usage]
# Simple test http request of 10 ranges.
#
#   $ ./httprangetest.pl www.example.local
#   $ ./httprangetest.pl http://wwww.example.local/foo/
#
# Test http requst by the number of ranges you specify.
#
#   $ ./httprangetest.pl 5 www.example.local
#   $ ./httprangetest.pl 20 http://www.example.local/bar/
#
# Test https request.
#
#   $ ./httprangetest.pl https://www.example.local/
#---------------------------------------------------------------------

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

 my $host 		= &getinput( $ARGV[0] ) if ( $ARGV[0] );
 my $outfile    = $ARGV[1];
   $range_count = &getinput( $ARGV[2] ) if ( $ARGV[2] );

open(OUTFILE, ">>$outfile");

# my $host 		= $ARGV[0];
#  $range_count = $ARGV[1];

# SETTING (Option) ---------------------------------------------------

# Warning when Apache accepted more than 5 ranges.
my $warn_range_count = 5;

# This script generate a http request of 10 ranges by default.
# You can change the default number of ranges.
my $default_range_count = 10;

# Set 0 if you want to hide hostname of test result.
#   0: Don't print hostname
#   1: Print hostname (default)
my $print_hostname = 1;

# Set 1 if you want to print contents from Apache.
#   0: Don't print content (default)
#   1: Print content.
my $print_content = 0;

#---------------------------------------------------------------------

use LWP::UserAgent;
my $ua = LWP::UserAgent->new;

my $url;

if ($host !~ /http/) {
	$url = "http://" . $host;
}
else {
	$url = $host;
	$host =~ s{https?//}{};
}
if ($print_hostname) {
	$print_hostname = "$host: ";
}
else {
	$print_hostname = "";
}

my $range = &make_range_header($range_count);

my $req = HTTP::Request->new(GET => $url);
$req->header(Range => $range);
my $res = $ua->request($req);

if ($res->is_success) {
	my $content = $res->content;
	my $header = $res->header("Content-Range");

	if ($print_content) {
		print OUTFILE "$content\n";
	}
	if ($content =~ /Content-range:/ && $range_count > $warn_range_count) {
		print OUTFILE "[Warning] " .$print_hostname. "Host can accept more than $warn_range_count ranges.\n";
	}
	elsif ($content =~ /Content-range:/ && $range_count <= $warn_range_count) {
		print OUTFILE "[Info] " .$print_hostname. "Host can accept $range_count ranges.\n";
	}
	elsif ($header =~ /bytes/ && $range_count <= $warn_range_count) {
		print OUTFILE "[Info] " .$print_hostname. "Host can accept $range_count range(s).\n";
	}
	else {
		print OUTFILE "[Info] " .$print_hostname. "Host ignored Range-Header.\n";
	}
}
else {
	print OUTFILE "[Info] " .$print_hostname. "HTTP Request was failed: " .$res->status_line."\n";
}

close(OUTFILE);

exit(0);

sub make_range_header {
	my $range_count = shift;
	my $range_start = 1;
	my $range_end = 10;
	my @range_set;

	foreach my $i ( 1 .. $range_count ) {
		push(@range_set, $range_start . "-" . $range_end);
		$range_start = (10 * $i) + 1;
		$range_end = $range_start + 9;
	}
	my $range_str = "bytes=" . join(",", @range_set);
	return $range_str;
}

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	# return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};