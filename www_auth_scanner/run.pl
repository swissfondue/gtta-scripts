# WWW Auth Scanner
# ---

use MooseX::Declare;
use core::task qw(execute);

# WWW Auth Scanner
class WWW_Auth_Scanner extends Task {
    use constant TIMEOUT => 3600;
    use LWP::UserAgent;
    use Net::SSL ();

    # Process
    method _process(Str $target, Str $protocol, Int $port, $lines) {
        my $found = 0;

        foreach my $line (@$lines) {
            my $request = new LWP::UserAgent;

            $request->default_header(
                "User-Agent" => "Mozilla/5.0 (Windows; U; Windows NT 5.2; de; rv:1.9.2.16) Gecko/20110319 Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; DigExt) ( .NET CLR 3.5.30729))",
                "accept" => "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language" => "de-de,de;q=0.8,en-us;q=0.5,en;q=0.3",
                "Accept-Encoding" => "gzip,deflate",
                "Accept-Charset" => "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Keep-Alive" => "115",
                "Connection" => "keep-alive",
                "Referer" => "http://its.me.oliver"
            );

            my $output = $request->get("$protocol://$target:$port/$line");
            my $error_code = $output->code;

            if ($error_code == 401) {
                $self->_write_result("Possible Admin Access found here: $protocol://$target:$port/$line. The response code was: " . $output->status_line);
                $found = 1;
            }
        }

        if (!$found) {
            $self->_write_result("No URLs with HTTP authorization detected.");
        }
    }

    # Main function
    method main($args) {
        my $lines = $self->_get_arg($args, 0);
        $self->_process($self->target, $self->proto || "http", $self->port || 80, $lines);
    }

    # Test function
    method test {
        $self->_process("google.com", "http", 80, ["auth", "admin", "login"]);
    }
}

execute(WWW_Auth_Scanner->new());
