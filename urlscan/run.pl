# URL Scan
# --

use MooseX::Declare;
use core::task qw(execute);

# URL Scan task
class URL_Scan extends Task {
    use LWP::UserAgent;

    # Process
    method _process(Str $target, Str $proto, $input_list) {
        my $url = "$proto://$target";

        foreach my $line (@$input_list) {
            my $request = new LWP::UserAgent;
            my $output = $request->get("$url/$line");

            if ($output->is_success) {
                $self->_write_result("FOUND: $url/$line");
            }
        }
    }

    # Main function
    method main($args) {
        my $input_list = $self->_get_arg($args, 0);
        $self->_process($self->target, $self->proto || "http", $input_list);
    }

    # Test function
    method test {
        $self->_process("google.com", "http", ["index.html", "test", "about"]);
    }
}

execute(URL_Scan->new());

