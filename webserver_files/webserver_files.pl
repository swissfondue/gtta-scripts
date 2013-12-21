#!perl

# Copyright 2012 Dakota Simonds

use LWP::UserAgent;
use LWP::ConnCache;
use HTTP::Response;
use Digest::MD5;
use encoding "utf-8";
use strict;

my $Host = $ARGV[0];

my $i;
my @files = ();

if (scalar(@ARGV) > 1) {
    for ($i = 1; $i < scalar(@ARGV); $i++) {
        push(@files, $ARGV[$i]);
    }
}

if (scalar(@files) == 0) {
    print "No input files selected.";
    exit();
}

my $Opt;

my $ua = LWP::UserAgent->new('conn_cache' => 1);
$ua->conn_cache(LWP::ConnCache->new); # use connection cacheing (faster)

$ua->agent("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.5) Gecko/20031027");


if($Host =~ /http(s|):\/\//i){ #check host input
	print "- No \"http:/\/\" please! just domain name or IP ADDR\n";
	exit();
}

&checkHostAvailibilty();
my $resAnalIndex = $ua->get("http://$Host/");

&FilesAndDirsGoodies();

exit(0);

sub checkHostAvailibilty{
	my $CheckHost1 = $ua->get("http://$Host/");
	my $CheckHost2 = $ua->get("http://$Host");

	if($CheckHost2->is_error and $CheckHost1->is_error){
		print "Host: $Host maybe offline or unavailble!\n";
		exit();
	}
}

sub analyzeResponse{ # heres were all the smart is...
	my $CheckResp = shift;
	my $checkURL = shift;

	unless($checkURL =~ /\//){
		$checkURL = "/" . $checkURL; # makes for good output
	}

	#False Positive checking
	my @ErrorStringsFound;

	my @PosibleErrorStrings = (
								'404 error',
								'404 page',
								'error 40\d', # any digit so it can be 404 or 400 whatever
								'not found',
								'cannot be found',
								'could not find',
								'cant find',
								'bad request',
								'server error',
								'temporarily unavailable',
								'not exist',
								'unable to open',
								'check your spelling',
								'an error has occurred',
								);
	foreach my $errorCheck (@PosibleErrorStrings){
		if($CheckResp =~ /$errorCheck/i){
			push(@ErrorStringsFound, "\"$errorCheck\" ");

		}
	}
	if(defined $ErrorStringsFound[0]){ # if the page contains multi error just put em into the same string
		print "+ Item \"$checkURL\" Contains text(s): @ErrorStringsFound MAYBE a False Positive!\n";
	}

	while(defined $ErrorStringsFound[0]){  pop @ErrorStringsFound;  } # saves the above if for the next go around


    my @PosibleLoginPageStrings = ('login','log-in','sign( |)in','logon',);
    foreach my $loginCheck (@PosibleLoginPageStrings){
        if($CheckResp =~ /<title>.*?$loginCheck/i){
            print "+ Item \"$checkURL\" Contains text: \"$loginCheck\" in the title MAYBE a Login page\n";
        }
    }

	#determine content-type
	my $indexContentType;
	my $IndexPage = $resAnalIndex->as_string();
	my @indexheadersChop = split("\n\n", $IndexPage);
	my @indexHeaders = split("\n", $indexheadersChop[0]); # tehe i know...

	foreach my $indexHeader (@indexHeaders){
		if($indexHeader =~ /content-type:/i){
			$indexContentType = $indexHeader;;
		}
	}

	# check page size
	my $IndexLength = length($resAnalIndex->as_string()); # get byte length of page
	if(length($IndexLength) > 999) { chop $IndexLength;chop $IndexLength; } # make byte length aproximate

	my $respLength = length($CheckResp);
	if(length($respLength) > 999) { chop $respLength;chop $respLength; } else { goto skipLeng; }

	if($IndexLength = $respLength and $CheckResp =~ /$indexContentType/i){ # the content-type makes for higher confindence
		print "+ Item \"$checkURL\" is about the same length as root page / This is MAYBE a redirect\n";
	}
	skipLeng:

	# check headers
	my @analheadersChop = split("\n\n", $CheckResp);
	my @analHeaders = split("\n", $analheadersChop[0]); # tehe i know...

	foreach my $analHString (@analHeaders){ # method used in sub Standard is not used because of custom msgs and there's not more then 2 headers per msg so why bother

		#the page is empty?
		if($analHString =~ /Content-Length: (0|1)$/i){
			print "+ Item \"$checkURL\" contains header: \"$analHString\" MAYBE a False Positive or is empty!\n";
		}

		#auth page checking
		if($analHString =~ /www-authenticate:/i){
			print "+ Item \"$checkURL\" contains header: \"$analHString\" Hmmmm\n";
		}

		#a hash?
		if($analHString =~ /Content-MD5:/i){
			print "+ Item \"$checkURL\" contains header: \"$analHString\" Hmmmm\n";
		}

		#redircted me?
		if($analHString =~ /refresh:/i){
			print "+ Item \"$checkURL\" - looks like it redirects. header: \"$analHString\"\n";
		}

		if($analHString =~ /http\/1.1 30(1|2|7)/i){
			print "+ Item \"$checkURL\" - looks like it redirects. header: \"$analHString\"\n";
		}

		if($analHString =~ /location:/i){
			my @checkLocation = split(/:/,$analHString);
			my $lactionEnd = $checkLocation[1];
			unless($lactionEnd =~ /$checkURL/i){
				print "+ Item \"$analHString\" does not match the requested page: \"$checkURL\" MAYBE a redirect?\n";
			}
		}

	}
}

sub nonSyntDatabaseScan{ # for DBs without the dir;msg format
	my $DataFromDBNonSynt = shift;
	my $scanMSGNonSynt = shift;
	chomp $DataFromDBNonSynt;
    return unless ($DataFromDBNonSynt);
		# send req and check if it's valid
		if (substr($DataFromDBNonSynt, 0, 1) eq '/')
		{
		    $DataFromDBNonSynt = substr($DataFromDBNonSynt, 1);
		}

		my $checkDir = $ua->get("http://$Host/" . $DataFromDBNonSynt);
		if($checkDir->is_success){
			print "+ $scanMSGNonSynt: \"/$DataFromDBNonSynt\"\n";
			&analyzeResponse($checkDir->as_string() ,$DataFromDBNonSynt);
		}
		$checkDir = undef;
}

sub FilesAndDirsGoodies{ # databases provided by: raft team
	print "**** running Interesting files and dirs scanner ****\n";

	print "+ interesting Files And Dirs takes awhile....\n";

	foreach my $FilesAndDirsDB (@files){
			open(FilesAndDirsDBFile, "+< $FilesAndDirsDB");
			my @parseFilesAndDirsDB = <FilesAndDirsDBFile>;

			foreach my $JustDir (@parseFilesAndDirsDB){
				&nonSyntDatabaseScan($JustDir,"interesting File or Dir Found");
			}
		close(FilesAndDirsDBFile);
	}
}
