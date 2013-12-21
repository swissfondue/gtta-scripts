# Joomla scan
# ---

use MooseX::Declare;
use core::task qw(execute);

# Joomla scan
class Joomla_Scan extends Task {
    use core::task qw(call_external);

    # Process
    method _process(Str $target, Str $proto) {
        my $url = "$proto://$target";
        $self->_write_result(call_external("perl joomla_scan.pl $url"));
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

execute(Joomla_Scan->new());
