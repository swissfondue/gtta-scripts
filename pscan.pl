#!perl

use File::Spec;
use File::Temp;
use XML::LibXML;
use strict;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $host  = &getinput( $ARGV[0] );
my $outfile = $ARGV[1];
my $ports = &getinput( $ARGV[2] ) if ($ARGV[2]);
my $skip_discovery = &getinput( $ARGV[3] ) if ($ARGV[3]);
my $verbose = &getinput( $ARGV[4] ) if ($ARGV[4]);
my $probe = &getinput( $ARGV[5] ) if ($ARGV[5]);
my $timing = &getinput( $ARGV[6] ) if ($ARGV[6]);
my $extract = &getinput( $ARGV[7] ) if ($ARGV[7]);

if (defined($timing) && !grep $_ == $timing, qw/0 1 2 3 4 5/)
{
    print q[Error: timing must be within 0..5 range], "\n";
    exit(0);
}

open(OUTFILE, ">>$outfile");

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

my $tmp;

if ($extract)
{
    $tmp = File::Temp->new(UNLINK => 1);
}

my $nmap_cmd = "nmap -sT " . ($skip_discovery ? '-PN ' : '') . ($verbose ? '-v ' : '') . ($probe ? '-sV ' : '') . ($timing ? "-T$timing " : '-T3 ') . ($ports ? "-p $ports " : '') . ($extract ? "-oX $tmp " : '') . "$host |";

undef $/;

open( READ, $nmap_cmd );
my $output = <READ>;
close(READ);

if ($extract)
{
    my $parser = XML::LibXML->new();
    my $xml = $parser->parse_file($tmp->filename);

    for my $host ($xml->findnodes('/nmaprun/host'))
    {
        my ($address, $hostname, $status, $ports, $extraports, @not_shown);

        ($address) = $host->findnodes('./address');
        $address = $address->getAttribute('addr');

        ($hostname) = $host->findnodes('./hostnames/hostname');

        if ($hostname)
        {
            $hostname = $hostname->getAttribute('name');
        }

        ($status) = $host->findnodes('status');
        $status = $status->getAttribute('state');

        print OUTFILE "Scan report for $address " . ($hostname ? "($hostname) " : "") . "\n";
        print OUTFILE "Host is $status\n";
        
        ($ports) = $host->findnodes('ports');

        @not_shown = ();

        for my $port ($ports->findnodes('extraports'))
        {
            push(@not_shown, $port->getAttribute('count') . " " . $port->getAttribute('state') . " ports");
        }

        if (scalar @not_shown)
        {
            print OUTFILE "Not shown: " . join(', ', @not_shown). "\n";
        }

        for my $port ($ports->findnodes('port'))
        {
            my ($id, $proto, $service, $state);

            #<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" product="OpenSSH" version="5.5p1 Debian 6+squeeze2" extrainfo="protocol 2.0" ostype="Linux" method="probed" conf="10" /></port>
            $id = $port->getAttribute('portid');
            $proto = $port->getAttribute('protocol');
            
            ($state) = $port->findnodes('./state');
            $state = $state->getAttribute('state');
            
            ($service) = $port->findnodes('./service');

            if ($service)
            {
                my ($sv, $product, $version, $ostype);

                $sv = $service->getAttribute('name');
                $product = $service->getAttribute('product');
                $version = $service->getAttribute('version');
                $ostype = $service->getAttribute('ostype');

                $service = "$sv" . ($product ? "\t$product " . ($version ? "$version " : "") . ($ostype ? "($ostype)" : "") : "");
            }

            print OUTFILE $id . ($proto ? "/$proto" : "") . "\t$state" . ($service ? $service : "") . "\n";
        }

        print OUTFILE "\n";
    }
}
else
{
    print OUTFILE $output;
}

close(OUTFILE);

File::Temp::cleanup();

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

	while( <IN> ){ chomp; push @fo, $_; }

	close( IN );

	#return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
