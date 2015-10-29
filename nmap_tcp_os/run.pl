# NMAP TCP OS
# --

use MooseX::Declare;
use core::task qw(execute);
use core::resulttable;

# NMAP TCP OS task
class NMAP_TCP_OS extends Task {
    use File::Spec;
    use File::Temp;
    use XML::LibXML;
    use core::task qw(call_external);

    use constant EXPAND_TARGETS => 0;

    # Process
    method _process(Str $host, Str $ports, Int $skip_discovery, Int $verbose, Int $probe, Int $timing, Int $extract) {
        my @data;

        if (!grep $_ == $timing, qw/0 1 2 3 4 5/) {
            die("Error: timing must be within 0..5 range\n");
        }

        my $tmp;

        if ($extract) {
            $tmp = File::Temp->new(UNLINK => 1);
        }

        my $nmap_cmd = "nmap -O -sT " . ($skip_discovery ? '-PN ' : '') . ($verbose ? '-v ' : '') . ($probe ? '-sV ' : '') . ($timing ? "-T$timing " : '-T3 ') . ($ports ? "-p $ports " : '') . ($extract ? "-oX $tmp " : '') . "$host";
        my $output = call_external($nmap_cmd);

        unless ($extract) {
            $self->_write_result($output);
            return;
        }

        my $parser = XML::LibXML->new();
        my $xml = $parser->parse_file($tmp->filename);

        for my $host ($xml->findnodes('/nmaprun/host')) {
            my ($address, $hostname, $status, $ports, $extraports, @not_shown, @open_ports);

            @open_ports = ();
            ($ports) = $host->findnodes('ports');

            for my $port ($ports->findnodes('port')) {
                my ($id, $proto, $service, $state, $product);

                $id = $port->getAttribute('portid');
                $proto = $port->getAttribute('protocol');

                ($state) = $port->findnodes('./state');
                $state = $state->getAttribute('state');

                ($service) = $port->findnodes('./service');

                if ($service) {
                    my ($sv, $version, $ostype);

                    $sv = $service->getAttribute('name');
                    $product = $service->getAttribute('product');
                    $version = $service->getAttribute('version');
                    $ostype = $service->getAttribute('ostype');

                    $service = $sv;

                    if ($product) {
                        $product = $product . ($version ? "$version " : "") . ($ostype ? "($ostype)" : "");
                    }
                }

                if ($state =~ /^open/) {
                    $product = 'N/A' unless ($product);
                    push(@open_ports, [ $id, $service, $product ]);
                }
            }

            next unless (@open_ports);

            ($address) = $host->findnodes('./address');
            $address = $address->getAttribute('addr');

            ($hostname) = $host->findnodes('./hostnames/hostname');

            if ($hostname) {
                $hostname = $hostname->getAttribute('name');
            }

            ($status) = $host->findnodes('status');
            $status = $status->getAttribute('state');

            $address = $hostname ? $address . " ($hostname)" : $address;

            for my $port (@open_ports) {
                push(@data, [ $address, $port->[0], $port->[1], $port->[2] ]);
            }
        }

        if (scalar(@data) > 0) {
            my $table = ResultTable->new(columns => [
                {name => "Address", width => "0.3"},
                {name => "Port", width => "0.2"},
                {name => "Service", width => "0.2"},
                {name => "Product", width => "0.3"},
            ]);

            for (my $i = 0; $i < scalar(@data); $i++) {
                my $row = [];

                for (my $k = 0; $k < scalar(@{$data[$i]}); $k++) {
                    $data[$i][$k] =~ s/</&lt;/g;
                    $data[$i][$k] =~ s/>/&gt;/g;
                    $data[$i][$k] =~ s/&/&amp;/g;

                    push(@$row, $data[$i][$k]);
                }

                $table->add_row($row);
            }

            $self->_write_result($table->render());
        } else {
            $self->_write_result('No open ports.');
        }

        File::Temp::cleanup();
    }

    # Main function
    method main($args) {
        my ($ports, $skip_discovery, $verbose, $probe, $timing, $extract);

        $ports = $self->_get_arg_scalar($args, 0, 0);
        $skip_discovery = $self->_get_int($args, 1, 0);
        $verbose = $self->_get_int($args, 2, 0);
        $probe = $self->_get_int($args, 3, 0);
        $timing = $self->_get_int($args, 4, 3);
        $extract = $self->_get_int($args, 5, 0);

        $self->_process($self->target, $ports, $skip_discovery, $verbose, $probe, $timing, $extract);
    }

    # Test function
    method test {
        $self->_process("google.com", "80", 0, 0, 1, 3, 1);
    }
}

execute(NMAP_TCP_OS->new());
