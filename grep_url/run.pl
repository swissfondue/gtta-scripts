# Grep URL
# ---

use MooseX::Declare;
use core::task qw(execute);

# Grep URL task
class Grep_URL extends Task {
    use constant TIMEOUT => 3600;
    use LWP::UserAgent;
    use HTML::LinkExtor;
    use URI::URL;
    use HTTP::Request;

    has "cnt" => (is => "rw", default => 0);
    has "done" => (is => "rw", default => sub {{}});

    # Grab the given URL
    method _grab($ua, $base, $url) {
        my $parser = HTML::LinkExtor->new;
        my $path = $url->path;
        my $fixed_url = URI::URL->new($url->scheme . "://" . $url->netloc . $path);

        if ($self->done->{$fixed_url}++) {
            return;
        } else {
            $self->_write_result($self->cnt . ") " . $fixed_url . "\n");
            $self->cnt($self->cnt + 1);
        }

        my $request	= HTTP::Request->new("GET" => $fixed_url);
        my $response = $ua->request($request);

        unless ($response->is_error()) {
            my $contents = $response->content();
            $parser->parse($contents)->eof;

            my @links = $parser->links;
            my @hrefs = map { url($_->[2], $base)->abs } @links;

            map {
                my $url = $_;

                if ($self->_is_child($base, $url)) {
                    $self->_grab($ua, $base, $url);
                }
            } @hrefs;
        }
    }

    # Check if URL is a child of a given base
    method _is_child($base, $url) {
        my $rel = $url->rel($base);
        return ($rel ne $url) && ($rel !~ m!^[/.]!);
    }

    # Process
    method _process(Str $target, Str $proto) {
        $self->cnt(1);

        my $ua = LWP::UserAgent->new;
        $ua->timeout(55);

        my $top = $ua->request(HTTP::Request->new("HEAD" => $proto . "://" . $target));
        my $base = $top->base;

        $self->_grab($ua, $base, URI::URL->new($top->request->url));
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

execute(Grep_URL->new());
