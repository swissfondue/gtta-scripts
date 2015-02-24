package core::task;

use Exporter;
use MooseX::Declare;
use threads;
use threads::shared;
use constant SANDBOX_IP => "192.168.66.66";

our @ISA = qw(Exporter);
our @EXPORT_OK = qw(execute call_external SANDBOX_IP);

# Base class for all tasks
class Task {
    use IO::Handle;
    use Scalar::Util qw(looks_like_number);

    use constant {
        DEFAULT_TIMEOUT => 60 * 60 * 24, # 1 Day
        TEST_TIMEOUT => 30,
        PARSE_FILES => 1,
        USER_LIBRARY_PATH => "/opt/gtta/scripts/lib",
        SYSTEM_LIBRARY_PATH => "/opt/gtta/scripts/system/lib"
    };

    has "target" => (isa => "Str", is => "rw");
    has "host" => (isa => "Str", is => "rw");
    has "ip" => (isa => "Str", is => "rw");
    has "proto" => (isa => "Str", is => "rw");
    has "port" => (isa => "Int", is => "rw");
    has "timeout" => (isa => "Int", is => "rw");
    has "lang" => (isa => "Str", is => "rw");
    has "test_mode" => (isa => "Int", is => "rw", default => 0);
    has "error" => (isa => "Int", is => "rw", default => 0);
    has "_produced_output" => (isa => "Int", is => "rw", default => 0);
    has "_stop" => (isa => "Int", is => "rw", default => 0);
    has "_result" => (is => "rw", default => 0);

    # Check if task is stopped
    method _check_stop {
        if ($self->_stop) {
            die "Task stopped.";
        }
    }

    # Write result to a file
    method _write_result(Str $str) {
        $self->_produced_output(1);

        if ($self->_result) {
            my $result_file;

            open($result_file, ">>" . $self->_result) or die("Unable to open result file: " . $self->_result . ".\n");
            $result_file->autoflush(1);
            syswrite($result_file, $str . "\n");
            close($result_file);
        } else {
            syswrite(STDOUT, $str . "\n");
        }
    }

    # Read whole file into memory
    method _read_file(Str $path) {
        my @contents;

        unless (open(IN, "<:utf8", $path)) {
            die("Cannot open file: $path.\n");
        }

        while (<IN>) {
            chomp;
            next unless ($_);
            push @contents, $_;
        }

        close(IN);

        return \@contents;
    }

    # Parse input arguments
    method _parse_input {
        my @output_arguments;

        if (scalar(@ARGV) < 2) {
            die("At least 2 command line arguments should be specified.\n");
        }    

        # parse the first file with hostname or IP
        my ($fp, @lines);        
        open($fp, $ARGV[0]) or die("Unable to open target file: " . $ARGV[0] . ".\n");

        while (<$fp>) {
            chomp;
            push(@lines, $_);
        }

        close($fp);

        if (scalar(@lines) < 5) {
            die("Target file should contain at least 5 lines.\n");
        }

        unless ($lines[0]) {
            die("Target file should contain either host name or IP address of the target host on the 1st line.\n");
        }

        $self->target($lines[0]);

        if ($lines[0] =~ /^\d+\.\d+\.\d+\.\d+$/) {
            $self->ip($lines[0]);
        } else {
            $self->host($lines[0]);
        }

        $self->proto($lines[1]);
        $self->port($lines[2] ? $lines[2] : 0);
        $self->lang($lines[3]);

        if (length($lines[4]) > 0) {
            $self->timeout($lines[4]);
        } else {
            $self->timeout($self->DEFAULT_TIMEOUT);
        }

        unless ($self->lang) {
            die("Target file should contain language name on the 4th line.\n");
        }

        # output file
        my $result_file;

        open($result_file, ">" . $ARGV[1]) or die("Unable to open result file: " . $ARGV[1] . ".\n");
        $result_file->autoflush(1);
        close($result_file);
        $self->_result($ARGV[1]);

        # parse the remaining arguments
        for (my $i = 2; $i < scalar(@ARGV); $i++) {
            my $arg = $ARGV[$i];            

            unless ($arg) {
                next;
            }

            unless ($self->PARSE_FILES) {
                push(@output_arguments, $arg);
                next;
            }

            my @file_lines = ();            
            open($fp, $arg) or die("Unable to open input file: $arg.\n");

            while (<$fp>) {
                chomp;
                push(@file_lines, $_);
            }

            close($fp);
            push(@output_arguments, \@file_lines);            
        }

        return @output_arguments;
    }

    # Get library path
    method _get_library_path($library) {
        my $path = undef;

        if (-d $self->SYSTEM_LIBRARY_PATH . "/" . $library) {
            $path = $self->SYSTEM_LIBRARY_PATH . "/" . $library;
        } elsif (-d $self->USER_LIBRARY_PATH . "/" . $library) {
            $path = $self->USER_LIBRARY_PATH . "/" . $library;
        } 

        return $path;
    }

    # Get argument
    method _get_arg($args, $number) {
        my @arg_array = @$args;

        if ($number >= scalar(@arg_array)) {
            return [];
        }

        return $arg_array[$number];
    }

    # Get scalar param from array
    method _get_arg_scalar($args, $number, $default) {
        my ($argument, @arg_values);

        $argument = $self->_get_arg($args, $number);

        unless (defined($default)) {
            $default = undef;
        }

        unless ($argument) {
            return $default;
        }

        @arg_values = @$argument;

        unless(scalar(@arg_values)) {
            return $default;
        }

        return $arg_values[0];
    }

    # Get int value
    method _get_int($args, $number, $default) {
        my $value = $self->_get_arg_scalar($args, $number, $default);

        unless(looks_like_number($value)) {
            $self->_write_result("Invalid parameter value (#" . ($number + 1) . "): $value, using default: $default.");
            return $default;
        }

        return $value;
    }

    # Default test method
    method test {
        die("Test not implemented.");
    }

    # Stop the task
    method stop {
        $self->_stop = 1;
    }

    # Run the task
    method run {
        STDOUT->autoflush(1);
        STDERR->autoflush(1);

        eval {
            my $timeout;
            my @arguments;

            if ($self->test_mode) {
                $timeout = $self->TEST_TIMEOUT;
            } else {
                @arguments = $self->_parse_input();
                $timeout = $self->timeout;
            }

            if ($timeout > 0) {
                alarm($timeout);
            }

            if ($self->test_mode) {
                $self->test();
                $self->_produced_output(1);
            } else {
                $self->main(\@arguments);
            }
        };

        alarm(0);

        if ($@) {
            my $error = $@;
            $self->_write_result($error);
            $self->_produced_output(1);

            $self->error(1);
        }

        unless ($self->_produced_output) {
            $self->_write_result("No data returned.");
        }
    }
}

# Executes task and controls its execution
sub execute {    
    my $obj :shared = shared_clone(shift);

    if (!$obj || !$obj->isa("Task")) {
        die("Invalid task object.\n");
    }

    if (scalar(@ARGV) == 1 && $ARGV[0] eq "--test") {
        $obj->test_mode(1);
    }

    my $thread = async {
        $obj->run();
    };

    $SIG{"ALRM"} = sub {
        $obj->_write_result("Task has timed out.");
        my $group = getpgrp();
        kill("TERM", -$group);
    };

    while (1) {
        my @joinable = threads->list(threads::joinable);

        if (scalar(@joinable)) {
            $joinable[0]->join();
            last;
        }

        sleep(1);
    }

    if ($obj->error) {
        $obj->_write_result("Script completed with errors.\n");
        exit(1);
    }
}

# External program call
sub call_external {
    my ($cmd, $output, $status);

    $cmd = shift;
    $output = `$cmd`;

    if ($? == -1) {
        die("Error executing command: $cmd.\n");
    }

    return $output;
}

1;
