# Webserver error msg
# ---

use MooseX::Declare;
use core::task qw(execute);

# Webserver error msg
class Webserver_Error extends Task {
    use constant TIMEOUT => 3600;
    use core::task qw(call_external);

    # Process
    method _process(Str $target) {
        $self->_write_result(call_external("perl webserver_error_msg.pl $target"));
    }

    # Main function
    method main($args) {
        $self->_process($self->target);
    }

    # Test function
    method test {
        $self->_process("google.com");
    }
}

execute(Webserver_Error->new());
