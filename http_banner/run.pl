# HTTP banner
# ---

use MooseX::Declare;
use core::task qw(execute);

# HTTP banner task
class HTTP_Banner extends Task {
    use HTTP::Request;
    use LWP::UserAgent;

    # Process
    method _process(Str $target, Str $proto, Str $url) {
        if (substr($url, 0, 1) ne "/") {
            $url = "/" . $url;
        }

        my $ua = LWP::UserAgent->new;
        my $request	= HTTP::Request->new(GET => $proto . "://" . $target . $url);
        my $response = $ua->request($request);

        $self->_write_result($response->dump());
    }

    # Main function
    method main($args) {
        my $url = $self->_get_arg_scalar($args, 0, "/");
        $self->_process($self->target, $self->proto || "http", $url);
    }

    # Test function
    method test {
        $self->_process("google.com", "http", "/");
    }
}

execute(HTTP_Banner->new());
