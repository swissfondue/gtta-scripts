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
my @data;

if (defined($timing) && !grep $_ == $timing, qw/0 1 2 3 4 5/)
{
    print q[Error: timing must be within 0..5 range], "\n";
    exit(0);
}

open(OUTFILE, ">>$outfile");

my $tmp;

if ($extract)
{
    $tmp = File::Temp->new(UNLINK => 1);
}

my $nmap_cmd = "nmap -O -sT " . ($skip_discovery ? '-PN ' : '') . ($verbose ? '-v ' : '') . ($probe ? '-sV ' : '') . ($timing ? "-T$timing " : '-T3 ') . ($ports ? "-p $ports " : '') . ($extract ? "-oX $tmp " : '') . "$host |";

undef $/;

open( READ, $nmap_cmd );
my $output = <READ>;
close(READ);

if ($extract)
{
    my $parser = XML::LibXML->new();
    my $xml = $parser->parse_file($tmp->filename);
    my $produced_output = 0;

    for my $host ($xml->findnodes('/nmaprun/host'))
    {
        my ($address, $hostname, $status, $ports, $extraports, @not_shown, @open_ports);

        @open_ports = ();
        ($ports) = $host->findnodes('ports');

        for my $port ($ports->findnodes('port'))
        {
            my ($id, $proto, $service, $state, $product);

            $id = $port->getAttribute('portid');
            $proto = $port->getAttribute('protocol');
            
            ($state) = $port->findnodes('./state');
            $state = $state->getAttribute('state');
            
            ($service) = $port->findnodes('./service');

            if ($service)
            {
                my ($sv, $version, $ostype);

                $sv = $service->getAttribute('name');
                $product = $service->getAttribute('product');
                $version = $service->getAttribute('version');
                $ostype = $service->getAttribute('ostype');

                $service = $sv; 
                
                if ($product)
                {
                    $product = $product . ($version ? "$version " : "") . ($ostype ? "($ostype)" : "");
                }
            }

            if ($state =~ /^open/)
            {
                $product = 'N/A' unless ($product);
                push(@open_ports, [ $id, $service, $product ]);
            }
        }    

        next unless (@open_ports);

        ($address) = $host->findnodes('./address');
        $address = $address->getAttribute('addr');

        ($hostname) = $host->findnodes('./hostnames/hostname');

        if ($hostname)
        {
            $hostname = $hostname->getAttribute('name');
        }

        ($status) = $host->findnodes('status');
        $status = $status->getAttribute('state');

        $address = $hostname ? $address . " ($hostname)" : $address;

        for my $port (@open_ports)
        {
            push(@data, [ $address, $port->[0], $port->[1], $port->[2] ]);
        }
    }

    if (scalar(@data) > 0)
    {
        print OUTFILE '<gtta-table><columns><column width="0.3" name="Address"/><column width="0.2" name="Port"/><column width="0.2" name="Service"/><column width="0.3" name="Product"/></columns>';
    
        for (my $i = 0; $i < scalar(@data); $i++)
        {
            print OUTFILE '<row>';
    
            for (my $k = 0; $k < scalar(@{$data[$i]}); $k++)
            {
                $data[$i][$k] =~ s/</&lt;/g;
                $data[$i][$k] =~ s/>/&gt;/g;
                $data[$i][$k] =~ s/&/&amp;/g;
    
                print OUTFILE '<cell>';
                print OUTFILE $data[$i][$k];
                print OUTFILE '</cell>';
            }
    
            print OUTFILE '</row>';
        }
    
        print OUTFILE '</gtta-table>';
    }
    else
    {
        print OUTFILE 'No open ports.';
    }
}
else
{
    print OUTFILE $output;
}

close(OUTFILE);

File::Temp::cleanup();

exit(0);

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
