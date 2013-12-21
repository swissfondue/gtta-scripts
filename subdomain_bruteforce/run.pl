# Subdomain bruteforce
# ---

use MooseX::Declare;
use core::task qw(execute);

# Subdomain bruteforce task
class Subdomain_Bruteforce extends Task {
    use constant TIMEOUT => 3600;
    use core::task qw(call_external);

    # Process
    method _process(Str $target, Int $big_file, Int $start_harvester) {
        my $harvester_path = $self->_get_library_path("harvester");
        $self->_write_result(call_external("perl subdomain_bruteforce.pl $target $big_file $start_harvester $harvester_path"));
    }

    # Main function
    method main($args) {
        my ($big_file, $start_harvester);

        $big_file = $self->_get_int($args, 0, 0);
        $start_harvester = $self->_get_int($args, 1, 0);

        $self->_process($self->target, $big_file, $start_harvester);
    }

    # Test function
    method test {
        $self->_process("google.com", 0, 0);
    }
}

execute(Subdomain_Bruteforce->new());
