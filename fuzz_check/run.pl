# Fuzz check
# ---

use MooseX::Declare;
use core::task qw(execute);

# Fuzz check
class Fuzz_Check extends Task {
    use constant TIMEOUT => 3600;
    use LWP::UserAgent;
    use HTTP::Request;

    # Process
    method _process(Str $target, Str $proto) {
        my $def = new LWP::UserAgent;
        my $ua = LWP::UserAgent->new("agent" => "Log", "env_proxy" => 1, "keep_alive" => 1, "timeout" => 1);
        my ($cnt, $found) = (0, 0);
        my $fuzzz = $self->_read_file("files/fuzz.txt");

        foreach my $fuzz (@$fuzzz) {
            my $url = "PROTO://HOST/FUZZ/";

            $url =~ s/PROTO/$proto/;
            $url =~ s/FUZZ/$fuzz/;
            $url =~ s/HOST/$target/;

            my $request = new HTTP::Request("GET" => $url);
            my $response = $def->request($request);

            if ($response->is_success) {
                $self->_write_result("with this URL $url obtained this:");
                $self->_write_result("----------------------START-----------------------------");
                $self->_write_result($response->decoded_content);
                $self->_write_result("----------------------END-------------------------------");

                $found++;
            }

            $cnt++;
        }

        $self->_write_result("tried $cnt time(s) with $found successful time(s)");
    }

    # Main function
    method main($args) {
        $self->_process($self->target, $self->proto || "http");
    }

    # Test function
    method test {
        $self->_process("google.com", "http");
    }
}

execute(Fuzz_Check->new());
