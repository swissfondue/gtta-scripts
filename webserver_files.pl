#!perl

# Copyright 2012 Dakota Simonds

use LWP::UserAgent;
use LWP::ConnCache;
use HTTP::Response;
use Digest::MD5;
use encoding "utf-8";

use strict;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my $Host = &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
open(OUTFILE, ">>$outfile");

my $i;
my $Opt;
my $Eb; # error begging
my $S; # Standard checks
my $auth; # MEH!!!!!! self explanitory
my $cmsPlugins; # cms plugins
my $interesting; # find interesting text in /index.whatever
my $Ws; # Web services
my $e; # EVERYTHINGGGGGGGG
my $ProxyServer; #use a proxy
my $Fd = 1; # files and dirs

my $ua = LWP::UserAgent->new('conn_cache' => 1);
$ua->conn_cache(LWP::ConnCache->new); # use connection cacheing (faster)

$ua->agent("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.5) Gecko/20031027");


if($Host =~ /http(s|):\/\//i){ #check host input
	print OUTFILE "- No \"http:/\/\" please! just domain name or IP ADDR\n";
	exit();
}

#triger scan

&proxy() 				if(defined $ProxyServer); # always make sure to put this first, lest we send un-proxied packets

&checkHostAvailibilty();
my $resAnalIndex = $ua->get("http://$Host/");

&Standard() 			if(defined $S);
&ErrorBegging() 		if(defined $Eb);
&auth() 				if(defined $auth);
&cmsPlugins()			if(defined $cmsPlugins);
&webServices() 			if(defined $Ws);
&FilesAndDirsGoodies() 	if(defined $Fd);
&runAll() 				if(defined $e);

close(OUTFILE);
exit(0);

sub runAll{
	&Standard();
	&ErrorBegging();
	&auth();
	&webServices();
	&FilesAndDirsGoodies();
	&cmsPlugins();
}

# non scanning subs for clean code and speed 'n stuff

sub usage{

print q{
usage:
	-host [host] -- Defines host to scan.
	-proxy [ip:port] -- use a proxy server
	-S -- Standard misconfig and other checks
	-Eb -- Error Begging. Sometimes a 404 page contains server info such as daemon or even the OS
	-auth -- Dictionary attack to find login pages (not passwords)
	-cmsPlugins [dp | jm | wp | all] -- check for cms plugins. dp = drupal, jm = joomla, wp = wordpress (db's a bit outdated 2010)
	-I -- Find interesting strings in pages (very verbose)
	-Fd -- look for common interesting files and dirs
	-Ws -- look for Web Services on host. such as hosting porvider, blogging service, favicon fingerprinting, and cms version info
	-e -- everything. run all scans

Example:
	perl Wsorrow.pl -host scanme.nmap.org -S
	perl Wsorrow.pl -host scanme.nmap.org -Eb -cmsPlugins dp,jm
	perl Wsorrow.pl -host 66.11.227.35 -S -Ws -I -proxy 129.255.1.17:3128
};

}

sub checkHostAvailibilty{
	my $CheckHost1 = $ua->get("http://$Host/");
	my $CheckHost2 = $ua->get("http://$Host");

	if($CheckHost2->is_error and $CheckHost1->is_error){
		print OUTFILE "Host: $Host maybe offline or unavailble!\n";
		exit();
	}
}

sub PromtUser{ # Yes or No?
	my $PromtMSG = shift; # i find the shift is much sexyer then then @_

	print OUTFILE $PromtMSG;
	$Opt = <stdin>;
	return $Opt;
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


	unless(defined $auth){ # that would make a SAD panda :(
		my @PosibleLoginPageStrings = ('login','log-in','sign( |)in','logon',);
		foreach my $loginCheck (@PosibleLoginPageStrings){
			if($CheckResp =~ /<title>.*?$loginCheck/i){
				print OUTFILE "+ Item \"$checkURL\" Contains text: \"$loginCheck\" in the title MAYBE a Login page\n";
			}
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

	if(defined $interesting){
			&interesting($CheckResp,$checkURL,);
	}
}

sub genErrorString{
	my $errorStringGGG = "";
	for($i = 0;$i < 20;$i++){
		$errorStringGGG .= chr((int(rand(93)) + 33)); # random 20 bytes to invoke 404 sometimes 400
	}

	$errorStringGGG =~ s/(#|&|\?)//g; #strip anchors and q stings
	return $errorStringGGG;
}

sub proxy{ # simple!!! i loves it
	$ua->proxy('http',"http://$ProxyServer");
}

sub dataBaseScan{ # use a database for scanning.
	my $DataFromDB = shift;
	my $scanMSG = shift;


		# take data from database and seperate dir from msg
		my @LineFromDB = split(';',$DataFromDB);
		my $JustDir = $LineFromDB[0]; #Dir or file to req
		my $MSG = $LineFromDB[1]; #this is the message printed if the url req isn't an error
		chomp $MSG;

		# send req and validate
		my $checkMsgDir = $ua->get("http://$Host" . $JustDir);
		if($checkMsgDir->is_success){
			print OUTFILE "+ $scanMSG: \"$JustDir\"  -  $MSG\n";
			&analyzeResponse($checkMsgDir->as_string() ,$JustDir);
		}
		$checkMsgDir = undef;
}

sub nonSyntDatabaseScan{ # for DBs without the dir;msg format
	my $DataFromDBNonSynt = shift;
	my $scanMSGNonSynt = shift;
	chomp $DataFromDBNonSynt;

		# send req and check if it's valid
		my $checkDir = $ua->get("http://$Host/" . $DataFromDBNonSynt);
		if($checkDir->is_success){
			print OUTFILE "+ $scanMSGNonSynt: \"/$DataFromDBNonSynt\"\n";
			&analyzeResponse($checkDir->as_string() ,$DataFromDBNonSynt);
		}
		$checkDir = undef;
}

sub matchScan{
	my $checkMatchFromDB = shift;
	my $checkMatch = shift;
	my $matchScanMSG = shift;
	chomp $checkMatchFromDB;


		my @matchScanLineFromDB = split(';',$checkMatchFromDB);
		my $msJustString = $matchScanLineFromDB[0]; #String to find
		my $msMSG = $matchScanLineFromDB[1]; #this is the message printed if it isn't an error

		if($checkMatch =~ /$msJustString/){
			print OUTFILE "+ $matchScanMSG: $msMSG\n";
		}

}


#---------------------------------------------------------------------------------------------------------------
# scanning subs


sub Standard{ #some standard stuff

		my @checkHeaders = (
							'server:',
							'x-powered-by:',
							'x-meta-generator:',
							'x-meta-framework:',
							'x-meta-originator:',
							'x-aspnet-version:',
							);


		my $resP = $ua->get("http://$Host/");
		my $headers = $resP->as_string();

		my @headersChop = split("\n\n", $headers);
		my @headers = split("\n", $headersChop[0]);

		foreach my $HString (@headers){
			foreach my $checkSingleHeader (@checkHeaders){
				if($HString =~ /$checkSingleHeader/i){
					print OUTFILE "+ Server Info in Header: \"$HString\"\n";
				}
			}
		}

		#robots.txt
		my $roboTXT = $ua->get("http://$Host/robots.txt");
		unless($roboTXT->is_error){
			&analyzeResponse($roboTXT->as_string() ,"/robots.txt");

			my $Opt = &PromtUser("+ robots.txt found! This could be interesting!\n+ would you like me to display it? (y/n) ? ");

			if($Opt =~ /y/i){
				print OUTFILE "+ robots.txt Contents: \n";
				my $roboConent = $roboTXT->decoded_content;
				while ($roboConent =~ /\n\n/) {	$roboConent =~ s/\n\n/\n/g;	} # cleaner. some robots have way to much white space
				while ($roboConent =~ /\t/) {	$roboConent =~ s/\t//g;	}

				print OUTFILE $roboConent . "\n\n";
			}
		}



		#lilith 6.0A rework of sub indexable with a cupple additions.

		my @CommonDIRs = (
							'/images',
							'/imgs',
							'/img',
							'/icons',
							'/home',
							'/pictures',
							'/main',
							'/css',
							'/style',
							'/styles',
							'/docs',
							'/pics',
							'/_',
							'/thumbnails',
							'/thumbs',
							'/scripts',
							'/files',
							'/js',
							'/site',
							);
		&checkOpenDirListing(@CommonDIRs);

		sub checkOpenDirListing{
			my (@DIRlist) = @_;
			foreach my $dir (@DIRlist){

				my $IndexFind = $ua->get("http://$Host" . $dir);

				# Apache
				if($IndexFind->content =~ /<H1>Index of \/.*<\/H1>/i){
					# extra checking (<a.*>last modified</a>, ...)
					print OUTFILE "+ Directory indexing found in \"$dir\" - AND it looks like an Apache server!\n";
					&analyzeResponse($IndexFind->as_string() ,$dir);
				}

				# Tomcat
				if($IndexFind->content =~ /<title>Directory Listing For \/.*<\/title>/i and $IndexFind->content =~ /<body><h1>Directory Listing For \/.*<\/h1>/i){
					print OUTFILE "+ Directory indexing found in \"$dir\" - AND it looks like an Apache Tomcat server!\n";
					&analyzeResponse($IndexFind->as_string() ,$dir);
				}

				# iis
				if($IndexFind->content =~ /<body><H1>$Host - $dir/i){
					print OUTFILE "+ Directory indexing found in \"$dir\" - AND it looks like an IIS server!\n";
					&analyzeResponse($IndexFind->as_string() ,$dir);
				}

			}
		}

		# laguage checks
		my $LangReq = $ua->get("http://$Host/");
		my @langSpaceSplit = split(/ / ,$LangReq->decoded_content);

		my $langString = 'lang=';
		my @langGate;

		foreach my $lineIDK (@langSpaceSplit){
			if($lineIDK =~ /$langString('|").*?('|")/i){
				while($lineIDK =~ "\t"){ #make pretty
					$lineIDK =~ s/\t//sg;
				}
				while($lineIDK =~ /(<|>)/i){ #prevent html from sliping in
					chop $lineIDK;
				}


				unless($lineIDK =~ /lang=('|")('|")/){ # empty?
					print OUTFILE "+ page Laguage found: $lineIDK\n";
				}
			}
		}




		# Some servers just give you a 200 with every req. lets see
		my @webExtentions = ('.php','.html','.htm','.aspx','.asp','.jsp','.cgi','.xml');
		foreach my $Extention (@webExtentions){
			my $testErrorString = &genErrorString();
			my $check200 = $ua->get("http://$Host/$testErrorString" . $Extention);

			if($check200->is_success){
				print OUTFILE "+ /$testErrorString" . $Extention . " responded with code: " . $check200->code . " the server might just responde with this code even when the dir, file, or Extention: $Extention doesn't exist! any results from this server may be void\n";
				&analyzeResponse($check200->as_string() ,"$testErrorString" . $Extention);
			}
		}

		#does the site have a mobile page?
		my $MobileUA = LWP::UserAgent->new;
		$MobileUA->agent('Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0');
		my $mobilePage = $MobileUA->get("http://$Host/");
		my $regularPage = $ua->get("http://$Host/");

		unless($mobilePage->content() eq $regularPage->content()){
			print OUTFILE "+ index page reqested with an Iphone UserAgent is diferent then with a regular UserAgent. This Host may have a mobile site\n";
		}
		$mobilePage = undef; $regularPage = undef;

		# is ssl there?
		$ua->ssl_opts(verify_hostname => 1);

		my $sslreq = $ua->get("https://$Host/");
		unless(length($sslreq->content) == 0 or $sslreq->is_error){
			print OUTFILE "+ $Host is SSL enabled\n";
		}
		$sslreq = undef;

}




# I don't know if this method has be used in other tools or has even been discovered before but I think it should allways be fixed
sub ErrorBegging{

		print OUTFILE "**** runnning  Error begging scanner ****\n";

		my $getErrorString = &genErrorString();
		my $_404responseGet = $ua->get("http://$Host/$getErrorString");
		&checkError($_404responseGet);

		my $postErrorString = &genErrorString();
		my $_404responsePost = $ua->post("http://$Host/$postErrorString");
		&checkError($_404responsePost);


		sub checkError{
			my $_404response = shift;

			if($_404response->is_error) {
				my $siteHTML = $_404response->decoded_content;


				### strip html tags and make pretty [very close to perfectly]
				$siteHTML =~ s/<script.*?<\/script>//sgi;
				$siteHTML =~ s/<style.*?<\/style>//sgi;
				$siteHTML =~ s/<(?!--)[^'">]*"[^"]*"/</sgi;
				$siteHTML =~ s/<(?!--)[^'">]*'[^']*'/</sgi;
				$siteHTML =~ s/<(?!--)[^">]*>//sgi;
				$siteHTML =~ s/<!--.*?-->//sgi;
				$siteHTML =~ s/<.*?>//sgi;
				$siteHTML =~ s/\n/ /sg;
				while($siteHTML =~ "  "){
					$siteHTML =~ s/  / /g;
				}
				while($siteHTML =~ "\t"){
					$siteHTML =~ s/\t//sg;
				}


				my $siteNaked = $siteHTML;
				if(length($siteNaked) > 1000){
					my $Opt = &PromtUser("! the Error page was found but its a bit big\n! do you still want to see it (y/n) ? ");
					if($Opt =~ /y/i){
						print OUTFILE $siteNaked . "\n\n";
					} else {
						print OUTFILE "\n+ Found 404 page but not printing. To Big :(\n";
					}
				} else {
					print OUTFILE "+ Error page found  -- " . $siteNaked . "\n\n";
				}
			}
		}

}





sub auth{ # this DB is pretty good but not complete

	print OUTFILE "**** running auth aka login page finder ****\n";

	open(authDB, "+<", 'webserver_files/db/login.db');
	my @parseAUTHdb = <authDB>;

	my @authDirMsg;
	foreach my $lineIDK (@parseAUTHdb){
		push(@authDirMsg, $lineIDK);
	}

	foreach my $authDirAndMsg (@authDirMsg){
		&dataBaseScan($authDirAndMsg,'Login Page Found');
	}


	close(authDB);
}




sub cmsPlugins{ # Plugin databases provided by: Chris Sullo from cirt.net

	print OUTFILE "**** running cms plugin detection scanner ****\n";

	print OUTFILE "+ CMS Plugins takes awhile....\n";
	my @cmsPluginDBlist;

	if($cmsPlugins =~ /dp/i){
		push(@cmsPluginDBlist, 'webserver_files/db/drupal_plugins.db');
	}

	if($cmsPlugins =~ /jm/i){
		push(@cmsPluginDBlist, 'webserver_files/db/joomla_plugins.db');
	}

	if($cmsPlugins =~ /wp/i){
		push(@cmsPluginDBlist, 'webserver_files/db/wp_plugins.db');
	}

	if($cmsPlugins =~ /all/i ){
		@cmsPluginDBlist = ('webserver_files/db/drupal_plugins.db', 
		'webserver_files/db/joomla_plugins.db', 
		'webserver_files/db/wp_plugins.db');
	}

	foreach my $cmsPluginDB (@cmsPluginDBlist){
		print OUTFILE "+ Testing Plugins with Database: $cmsPluginDB\n";

		open(cmsPluginDBFile, "+< $cmsPluginDB");
		my @parsecmsPluginDB = <cmsPluginDBFile>;

		foreach my $JustDir (@parsecmsPluginDB){
			&nonSyntDatabaseScan($JustDir,"CMS Plugin Found");
		}
		close(cmsPluginDBFile);

	}


}

sub FilesAndDirsGoodies{ # databases provided by: raft team
	print OUTFILE "**** running Interesting files and dirs scanner ****\n";

	print OUTFILE "+ interesting Files And Dirs takes awhile....\n";
	my @FilesAndDirsDBlist = ('webserver_files/db/raft-small-files.db',
	'webserver_files/db//raft-small-directories.db',);

	foreach my $FilesAndDirsDB (@FilesAndDirsDBlist){
			print OUTFILE "+ Testing Files And Dirs with Database: $FilesAndDirsDB\n";

			open(FilesAndDirsDBFile, "+< $FilesAndDirsDB");
			my @parseFilesAndDirsDB = <FilesAndDirsDBFile>;

			foreach my $JustDir (@parseFilesAndDirsDB){
				&nonSyntDatabaseScan($JustDir,"interesting File or Dir Found");
			}
		close(FilesAndDirsDBFile);

	}


}

sub webServices{ # as of v 1.2.7 it's acually worth the time typing "-Ws" to use it! HORAYYY

	print OUTFILE "**** running Web Service scanner ****\n";

	open(webServicesDB, "+<", 'webserver_files/db/web-services.db');
	my @parsewebServicesdb = <webServicesDB>;

	my $webServicesTestPage = $ua->get("http://$Host/");

	my @webServicesStringMsg;
	foreach my $lineIDK (@parsewebServicesdb){
		push(@webServicesStringMsg, $lineIDK);
	}



	foreach my $ServiceString (@webServicesStringMsg){
		&matchScan($ServiceString,$webServicesTestPage->content,"Web service Found");
	}


	close(webServicesDB);

	&faviconMD5(); # i'll just make a new sub
	&cms();
}




sub faviconMD5{ # thanks to OWASP

	my $favicon = $ua->get("http://$Host/favicon.ico");

	if($favicon->is_success){
		&analyzeResponse($favicon->as_string() ,"/favicon.ico");

		#make checksum
		my $MD5 = Digest::MD5->new;
		$MD5->add($favicon->content);
		my $checksum = $MD5->hexdigest;


		open(faviconMD5DB, "+<", 'webserver_files/db/favicon.db');
		my @faviconMD5db = <faviconMD5DB>;


		my @faviconMD5StringMsg; # split DB by line
		foreach my $lineIDK (@faviconMD5db){
			push(@faviconMD5StringMsg, $lineIDK);
		}

		foreach my $faviconMD5String (@faviconMD5StringMsg){
			&matchScan($faviconMD5String,$checksum,"Web service Found (favicon.ico)");
		}

		close(faviconMD5DB);
	}
}




sub cms{
	open(cmsDB, "+<", 'webserver_files/db/CMS.db');
	my @parseCMSdb = <cmsDB>;

	my @cmsDirMsg;
	foreach my $lineIDK (@parseCMSdb){
		push(@cmsDirMsg, $lineIDK);
	}

	foreach my $cmsDirAndMsg (@cmsDirMsg){
		&dataBaseScan($cmsDirAndMsg,'Web service Found (cms)'); #this func can only be called when the DB uses the /dir;msg format
	}

	close(cmsDB);
}




sub interesting{ # look for DBs, dirs, login pages, and emails and such
	my $mineShaft = shift;
	my $mineUrl = shift;
	my @InterestingStringsFound;

	my @interestingStings = ( # much thiner cuz was to general and verbose
							'\/cgi-bin',
							'\/wp-content\/plugins\/',
							'@.*?\.(com|org|net|tv|uk|au|edu|mil|gov)', #emails
							'<!--#', #SSI
							);

	foreach my $checkInterestingSting (@interestingStings){
		my @IndexData = split(/</,$mineShaft);

		foreach my $splitIndex (@IndexData){
			if($splitIndex =~ /$checkInterestingSting/i){
				while($splitIndex =~ /(\n|\t|  )/){
					$splitIndex =~ s/\n/ /g;
					$splitIndex =~ s/\t//g;
					$splitIndex =~ s/  / /g;
				}
				# the split chops off < so i just stick it in there to make it look pretty
				push(@InterestingStringsFound, "<$splitIndex\n\t");
			}

		}



		if(defined $InterestingStringsFound[0]){ # if the page contains multi error just put em into the same string
			print OUTFILE "+ Interesting text found in \"$mineUrl\": \n\t@InterestingStringsFound\n";
		}

		while(defined $InterestingStringsFound[0]){  pop @InterestingStringsFound;  } # saves the above if for the next go around

	}
	$mineShaft = undef;
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
