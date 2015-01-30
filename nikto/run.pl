# Nikto
# ---

use MooseX::Declare;
use core::task qw(execute);

# Nikto
class Nikto extends Task {
    use core::task qw(call_external);

    # Process
    method _process(Str $target, Str $proto, Int $port) {
        $self->_write_result(call_external("perl nikto.pl $target $proto $port"));
    }

    # Main function
    method main($args) {
        $self->_process($self->target, $self->proto || "http", $self->port || 80);
    }

    # Test function
    method test {
        $self->_process("demonstratr.com", "http", 80);
    }
}

execute(Nikto->new());
