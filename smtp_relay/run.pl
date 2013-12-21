# SMTP Relay
# --

use MooseX::Declare;
use core::task qw(execute);

# SMTP Relay task
class SMTP_Relay extends Task {
    use Net::SMTP;

    # Process
    method _process(Str $target, Int $port, Int $timeout, Str $mail_from, Str $mail_to) {
        my $smtp;

        if ($smtp = Net::SMTP->new($target, 'Debug' => 0, 'Timeout' => $timeout, 'Port' => $port)) {
            my $msg = $smtp->message();
            my @lines = split /\n/, $msg;

            $self->_write_result($smtp->code() . ' ' . $lines[0]);
            shift @lines;

            for my $line (@lines) {
                $self->_write_result($smtp->code() . '-' . $line);
            }

            $self->_write_result("MAIL FROM:<$mail_from>\n");
            my $ok = $smtp->mail($mail_from);
            $self->_write_result($smtp->code() . ' ' . $smtp->message());

            if ($ok) {
                $self->_write_result("RCPT TO:<$mail_to>\n");
                $ok = $smtp->to($mail_to);
                $self->_write_result($smtp->code() . ' ' . $smtp->message());

                if ($ok) {
                    $self->_write_result("DATA");
                    $smtp->data(".\r\n");
                    $self->_write_result($smtp->code() . ' ' . $smtp->message());
                }
            }
        } else {
            $self->_write_result("Error: server $target connection failed");
        }
    }
    
    # Main function
    method main($args) {
        my ($timeout, $mail_from, $mail_to);

        $timeout = $self->_get_int($args, 0, 60);
        $mail_from = $self->_get_arg_scalar($args, 1, 'test1@gmail.com');
        $mail_to = $self->_get_arg_scalar($args, 2, 'test2@gmail.com');

        $self->_process($self->target, $self->port || 25, $timeout, $mail_from, $mail_to);
    }

    # Test function
    method test {
        $self->_process("smtp.gmail.com", 25, 60, 'test1@gmail.com', 'pewpew@hotmail.com');
    }
}

execute(SMTP_Relay->new());
