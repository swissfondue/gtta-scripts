# Webserver Files
# ---

use MooseX::Declare;
use core::task qw(execute);

# Webserver Files task
class Webserver_Files extends Task {
    use constant {
        TIMEOUT => 3600,
        PARSE_FILES => 0
    };

    use core::task qw(call_external);

    # Process
    method _process(Str $target, $files) {
        my $joined_files = join(" ", @$files);
        $self->_write_result(call_external("perl webserver_files.pl $target $joined_files"));
    }

    # Main function
    method main($args) {
        $self->_process($self->target, $args);
    }

    # Test function
    method test {
        $self->_process("google.com", ["files/Apache_Web_Server.txt"]);
    }
}

execute(Webserver_Files->new());
