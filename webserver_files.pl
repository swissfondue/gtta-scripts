#!perl

# Copyright 2012 Dakota Simonds

use LWP::UserAgent;
use LWP::ConnCache;
use HTTP::Response;
use Digest::MD5;
use encoding "utf-8";

use strict;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my @files = (
    'Admin_Logins.txt',
    'Adobe_xml.txt',
    'Apache_Dojo_Framework.txt',
    'Apache_Tomcat_Application_Server.txt',
    'Apache_Web_Server.txt',
    'Backend_Dirs.txt',
    'CA_Siteminder_Adminstration.txt',
    'Checkpoint_Firewall_Web_Interface.txt',
    'Citrix_Application_Server.txt',
    'Cold_Fusion_Application_Server.txt',
    'ContentXXL_Cms.txt',
    'DotProject.txt',
    'Drupal_Cms.txt',
    'Fatwire_CMS.txt',
    'Hyperion_CMS.txt',
    'Ibm_Websphere_Application_Server.txt',
    'Iis_Web_Server.txt',
    'J2EE_JRUN_Application_Server.txt',
    'Java_servlets_and_jboss.txt',
    'Jira_JSP.txt',
    'Joomla_Cms_Dirs.txt',
    'Lotus_Domino_Web_Server.txt',
    'Mbrs_Php.txt',
    'Nikto_Database_Checks.txt',
    'Novell_Access_Manager_and_Netware.txt',
    'Oracle_Web_and_Application_Server.txt',
    'Php_requests.txt',
    'Phpmyadmin_Cms.txt',
    'Piwik_Webalyzer.txt',
    'Proxy_Test.txt',
    'SAP_Web_Server.txt',
    'Sharepoint_Application_Server.txt',
    'Symfony_Cms.txt',
    'Typo3_Cms.txt',
    'Unix_Files.txt',
    'Vignette_Cms.txt',
    'Vuln_Files.txt',
    'Winlike.txt',
    'Wordpress_Cms.txt',
    'checkpoint_sslnetwork_extender.txt'
);

my $Host = &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
open(OUTFILE, ">>$outfile");

my $i;

my @selected_files = ();

for ($i = 0; $i < scalar(@files); $i++)
{
    my $value = &getinput($ARGV[2 + $i]) if ($ARGV[2 + $i]);
    push(@selected_files, $files[$i]) if ($value);
}

if (scalar(@selected_files) == 0)
{
    print OUTFILE "No input files selected.";
    exit();
}

my $Opt;

my $ua = LWP::UserAgent->new('conn_cache' => 1);
$ua->conn_cache(LWP::ConnCache->new); # use connection cacheing (faster)

$ua->agent("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.5) Gecko/20031027");


if($Host =~ /http(s|):\/\//i){ #check host input
	print OUTFILE "- No \"http:/\/\" please! just domain name or IP ADDR\n";
	exit();
}

&checkHostAvailibilty();
my $resAnalIndex = $ua->get("http://$Host/");

&FilesAndDirsGoodies();

close(OUTFILE);
exit(0);

sub checkHostAvailibilty{
	my $CheckHost1 = $ua->get("http://$Host/");
	my $CheckHost2 = $ua->get("http://$Host");

	if($CheckHost2->is_error and $CheckHost1->is_error){
		print OUTFILE "Host: $Host maybe offline or unavailble!\n";
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
		print OUTFILE "+ Item \"$checkURL\" Contains text(s): @ErrorStringsFound MAYBE a False Positive!\n";
	}

	while(defined $ErrorStringsFound[0]){  pop @ErrorStringsFound;  } # saves the above if for the next go around


    my @PosibleLoginPageStrings = ('login','log-in','sign( |)in','logon',);
    foreach my $loginCheck (@PosibleLoginPageStrings){
        if($CheckResp =~ /<title>.*?$loginCheck/i){
            print OUTFILE "+ Item \"$checkURL\" Contains text: \"$loginCheck\" in the title MAYBE a Login page\n";
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
		print OUTFILE "+ Item \"$checkURL\" is about the same length as root page / This is MAYBE a redirect\n";
	}
	skipLeng:

	# check headers
	my @analheadersChop = split("\n\n", $CheckResp);
	my @analHeaders = split("\n", $analheadersChop[0]); # tehe i know...

	foreach my $analHString (@analHeaders){ # method used in sub Standard is not used because of custom msgs and there's not more then 2 headers per msg so why bother

		#the page is empty?
		if($analHString =~ /Content-Length: (0|1)$/i){
			print OUTFILE "+ Item \"$checkURL\" contains header: \"$analHString\" MAYBE a False Positive or is empty!\n";
		}

		#auth page checking
		if($analHString =~ /www-authenticate:/i){
			print OUTFILE "+ Item \"$checkURL\" contains header: \"$analHString\" Hmmmm\n";
		}

		#a hash?
		if($analHString =~ /Content-MD5:/i){
			print OUTFILE "+ Item \"$checkURL\" contains header: \"$analHString\" Hmmmm\n";
		}

		#redircted me?
		if($analHString =~ /refresh:/i){
			print OUTFILE "+ Item \"$checkURL\" - looks like it redirects. header: \"$analHString\"\n";
		}

		if($analHString =~ /http\/1.1 30(1|2|7)/i){
			print OUTFILE "+ Item \"$checkURL\" - looks like it redirects. header: \"$analHString\"\n";
		}

		if($analHString =~ /location:/i){
			my @checkLocation = split(/:/,$analHString);
			my $lactionEnd = $checkLocation[1];
			unless($lactionEnd =~ /$checkURL/i){
				print OUTFILE "+ Item \"$analHString\" does not match the requested page: \"$checkURL\" MAYBE a redirect?\n";
			}
		}

	}
}

sub nonSyntDatabaseScan{ # for DBs without the dir;msg format
	my $DataFromDBNonSynt = shift;
	my $scanMSGNonSynt = shift;
	chomp $DataFromDBNonSynt;
     print "http://$Host/" . $DataFromDBNonSynt . "\n";
		# send req and check if it's valid
		if (substr($DataFromDBNonSynt, 0, 1) eq '/')
		{
		    $DataFromDBNonSynt = substr($DataFromDBNonSynt, 1);
		}

		my $checkDir = $ua->get("http://$Host/" . $DataFromDBNonSynt);
		if($checkDir->is_success){
			print OUTFILE "+ $scanMSGNonSynt: \"/$DataFromDBNonSynt\"\n";
			&analyzeResponse($checkDir->as_string() ,$DataFromDBNonSynt);
		}
		$checkDir = undef;
}

sub FilesAndDirsGoodies{ # databases provided by: raft team
	print OUTFILE "**** running Interesting files and dirs scanner ****\n";

	print OUTFILE "+ interesting Files And Dirs takes awhile....\n";

	foreach my $FilesAndDirsDB (@selected_files){
			print OUTFILE "+ Testing Files And Dirs with Database: $FilesAndDirsDB\n";

			open(FilesAndDirsDBFile, "+< webserver_files/$FilesAndDirsDB");
			my @parseFilesAndDirsDB = <FilesAndDirsDBFile>;

			foreach my $JustDir (@parseFilesAndDirsDB){
				&nonSyntDatabaseScan($JustDir,"interesting File or Dir Found ($FilesAndDirsDB)");
			}
		close(FilesAndDirsDBFile);
	}
}

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ s/^(\S+)$/{ push @fo, $1; }/e; }

	close( IN );

	#return \@fo if ( scalar @fo > 1 );
	return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
