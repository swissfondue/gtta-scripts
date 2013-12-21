#!/usr/bin/perl
# -=-=-=-=-=-=-=-
# JoomlaScan v1.3
# -=-=-=-=-=-=-=-
#
# Pepelux <pepeluxx[at]gmail.com>
# www.pepelux.org
# blog.pepelux.org
# Twitter: @pepeluxx
#
# Initial date : 2010-09-04
# Last revision: 2011-10-30
#
# Changelog at the end

use strict;
use LWP::UserAgent;
use HTTP::Request::Common;
use Switch;

my @data = (
    "admin_en-GB.txt",
    "admin_en-GB_media.txt",
    "adminlists.txt",
    "bugs.txt",
    "en-GB.txt",
    "en-GB_media.txt",
    "admin_en-GB_installer.txt",
    "files.txt",
    "generic.txt",
    "helpsites.txt",
    "htaccess.txt",
    "javascript.txt",
    "metadata.txt",
    "php-dist.txt"
);

my $url = '';                 # url to check
my $proxy = '';               # optional proxy server
my $admin = 'administrator';  # admin folder
my $v = 1;                    # check version
my $c = 1;                    # check components
my $f = 1;                    # check firewall
my $co = 1;                   # check core bugs
my $cm = 1;                   # check components bugs
my $all = 1;                  # check all
my $ot = 0;                   # output to text file
my $oh = 0;                   # output to html file
my $h = 0;                    # usage help
my $about = 0;                # about joomlascan
my $version = 1;              # print version
my $update = 0;               # update program & database
my $forceupdate = 0;          # force update program & database

my $index = '';
my $firewall = '';
my @components;
my $nVerIniTmp = -1;
my $nRevIniTmp = -1;
my $nModIniTmp = -1;
my $nVerFinTmp = -1;
my $nRevFinTmp = -1;
my $nModFinTmp = -1;
my @version = ("x", "x", "x", "", "x", "x", "x", "");
my $isMambo = 0;

my @sVulnerability;
my @sVersion;
my @sFile;
my @sExploit;
my @sUrlExploit;
my @bVulnerability;
my @bVersion;
my @bFile;
my @bExploit;
my @bUrlExploit;
my @bType;
my $webserver = '';

$url = $ARGV[1];

my $ua = LWP::UserAgent->new() or die;
$ua->agent("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008072820 Firefox/3.0.1");
$ua->timeout(10);

init();

close(OUTFILE);


##########################
# check params and start #
##########################

sub init {
	$url = $url . '/' if ($url !~ /$\//);

	checkdatafiles();
	$webserver = checkwebserver($url);
	scanfirewall();
	scancomponents();
	scanversion();
	scantips("generic");
	scanbugs("bugs", "Core");
	scanbugs("bugs", "Component");
	print "Scan finished\n";

	printscreen();
}


#############################
# search for possibles bugs #
#############################

sub scanbugs {
	my $file = shift;
	my $type = shift;
	my @tmp;
	my @verTmp;
	my @versionTmp = @version;

	$file .= ".txt";

	if ($#versionTmp > 6) {
		for (my $i = 0; $i < 8; $i++) {
			if ($versionTmp[$i] eq "x") {
				$versionTmp[$i] = "0";
			}
		}
	}

	# print "Scanning " . $file . " in " . $type . " ";
	print 'search for possibles bugs',"($type)\n";
	open(DAT, "files/" . $file) || die("File " . $file . " not found. Try --force-update\n");

	while (<DAT>) {
		if (($_ !~ /^#/)) {
			if ($all eq 1 || ($co eq 1 && $_ =~ /^Core/) || ($cm eq 1 && $_ =~ /^Component/)) {
				@tmp = split(/\|/, $_);

				if ($#tmp > 4) {
					my $v1 = $tmp[3];
					my $v2 = $tmp[4];
					my $v = '';

					if ($v1 eq $v2 && $v1 ne "x.x.x") {
						$v = $v1;
					}
					elsif ($v1 ne "x.x.x") {
						$v = "[" . $v1 . "-" . $v2 . "]";
					}
					elsif ($v2 ne "x.x.x") {
						$v = "<= " . $v2;
					}
					else {
						$v = "";
					}

					if ($v ne "") {
						$v = "Joomla! " . $v;
					}

					if ($tmp[5] ne "") {
						if ($v1 ne "x.x.x" || $v2 ne "x.x.x") {
							$v .= " - ";
						}

						$v .= $tmp[5];
					}

					my @aux1 = split(/\./, $v1);
					my @aux2 = split(/\./, $v2);

					$aux1[0] = "0" if ($aux1[0] eq "x");
					$aux1[1] = "0" if ($aux1[1] eq "x");
					$aux1[2] = "0" if ($aux1[2] eq "x");
					$aux2[0] = "0" if ($aux2[0] eq "x");
					$aux2[1] = "0" if ($aux2[1] eq "x");
					$aux2[2] = "0" if ($aux2[2] eq "x");

					@verTmp = ($aux1[0], $aux1[1], $aux1[2], "");
					push @verTmp, $aux2[0], $aux2[1], $aux2[2], "";

					my $tipo = $tmp[0];
					my $modVuln = 0;

					if ($tmp[1] ne "") {
						if ($tmp[1] !~ m/\//) {
							$tipo .= " - " . $tmp[1];
							$tipo =~ s/joomla//g;
						}

						if ($tmp[1] =~ m/ /) {
							my @aux = split(/ /, $tmp[1]);

							foreach (@aux) {
								if (checkcomp($_) eq 1 || $_ eq "joomla") {
									$modVuln = 1;
								}
							}
						}
						elsif (($tmp[1] =~ m/.php/ || $tmp[1] =~ m/.htm/) && $tmp[1] !~ m/index.php/) {
							if ($index =~ m/$tmp[1]/ || checkpage($url . $tmp[1]) eq 1) {
								$modVuln = 1;
							}
						}
						elsif ($tmp[1] =~ m/\//) {
							if ($tmp[1] !~ m/index.php/) {
								if ($index =~ m/$tmp[1]/ || checkpage($url . $tmp[1])) {
									$modVuln = 1;
								}
							}
							elsif ($index =~ m/$tmp[1]/) {
								$modVuln = 1;
							}
						}
						elsif (checkcomp($tmp[1]) eq 1) {
							$modVuln = 1;
						}
					}
					else {
						$modVuln = 1;
					}

					if ($modVuln eq 1) {
						if (($verTmp[0] <= $versionTmp[0] && $verTmp[1] <= $versionTmp[1] &&
							 $verTmp[2] <= $versionTmp[2] &&
							 $verTmp[4] >= $versionTmp[0] && $verTmp[5] >= $versionTmp[1] &&
							 $verTmp[6] >= $versionTmp[6]) ||
							($verTmp[0] >= $versionTmp[4] && $verTmp[1] >= $versionTmp[5] &&
							 $verTmp[2] >= $versionTmp[6] &&
							 $verTmp[4] <= $versionTmp[4] && $verTmp[5] <= $versionTmp[5] &&
							 $verTmp[6] <= $versionTmp[6]) ||
							($verTmp[0] eq 0 && $verTmp[1] eq 0 && $verTmp[2] eq 0 &&
							 $verTmp[4] eq 0 && $verTmp[5] eq 0 && $verTmp[6] eq 0)) {
								if ($_ =~ /$type/) {
									push @bVulnerability, $tmp[2];
									push @bType, $type;
									push @bVersion, $v;
									push @bExploit, $tmp[6];
									push @bUrlExploit, $tmp[7];
								}
						}
					}
				}
			}
		}
	}

	close(DAT);
	print "\n";
}

sub checkcomp {
	my $comp = shift;

	foreach (@components) {
		if ($_ eq $comp) {
			return 1;
		}
	}

	return 0;
}

################################
# search for unprotected files #
################################

sub scantips {
	my $file = shift;
	my @tmp;

	$file .= ".txt";

	# print "Scanning " . $file . " ";
	print 'search for unprotected files',"($file)\n";
	open(DAT, "files/" . $file) || die("File " . $file . " not found. Try --force-update\n");

	while (<DAT>) {
		if (($_ !~ /^#/)) {
			@tmp = split(/\|/, $_);

			if ($#tmp > 3 && getpage($url . $tmp[0])) {
				push @sVulnerability, $tmp[1];
				push @sVersion, $tmp[2];
				push @sFile, $url . $tmp[0];
				push @sExploit, $tmp[3];
				push @sUrlExploit, $tmp[4];
				print 'found:',"\n",
					  'file: ', $url . $tmp[0],"\n",
					  'URL: ', $tmp[4],"\n",
					  'exploit: ', $tmp[3],"\n",
					  'version: ', $tmp[2],"\n";
			} # else { print 'no unprotected files found',"\n"; }
		}
	}

	close(DAT);
	print "\n";
}


######################
# search for version #
######################

sub scanversion {
	scancopyrigth();

	my $pag = getpage($url . "htaccess.txt");
	die ("This website is Mambo") if ($pag =~ m/package Mambo/);
	scanconfigfile($pag, "htaccess") if ($pag ne "");

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . $admin . "/manifests/files/joomla.xml");
		scanmanifestfile($pag) if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "language/en-GB/en-GB.ini");
		scanlanguagefile($pag, "en-GB") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . $admin . "/language/en-GB/en-GB.ini");
		scanlanguagefile($pag, "admin_en-GB") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . $admin . "/language/en-GB/en-GB.com_media.ini");
		scanconfigfile($pag, "admin_en-GB_media") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "configuration.php-dist");
		scanconfigfile($pag, "php-dist") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "includes/js/joomla.javascript.js");
		scanconfigfile($pag, "javascript") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "libraries/joomla/template/tmpl/adminlists.html");
		scanconfigfile($pag, "adminlists") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "components/com_contact/metadata.xml");
		scanconfigfile($pag, "metadata") if ($pag ne "");
	}

	# 1.5 => helpsites-15.xml -- 1.6 => helpsites-16.xml -- 1.7 => helpsites.xml
	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . $admin . "/help/helpsites-15.xml");
		scanconfigfile($pag, "helpsites") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "language/en-GB/en-GB.com_media.ini");
		scanconfigfile($pag, "en-GB_media") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . $admin . "/language/en-GB/en-GB.com_installer.ini");
		scanconfigfile($pag, "admin_en-GB_installer") if ($pag ne "");
	}

	if ($version[0] eq "x" || $version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		scanforfiles("files");
	}

	if ($version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "language/en-GB/en-GB.ini");
		scanspecialcases($pag);
	}

	# more special cases
	if ($version[0] eq "1" && $version[1] eq "7" && $version[2] eq "1" && $version[4] eq "1" && $version[5] eq "7" && $version[6] eq "2") {
		$pag = getpage($url . $admin . "/components/com_admin/sql/updates/mysql/1.7.0-2011-06-06-2.sql");

		if (length($pag) == 161) {
			$version[2] = "2";
		}
		if (length($pag) == 162) {
			$version[6] = "1";
		}
	}
	if ($version[0] eq "1" && $version[1] eq "6" && $version[2] eq "3" && $version[4] eq "1" && $version[5] eq "6" && $version[6] eq "6") {
		$pag = getpage($url . $admin . "/language/en-GB/en-GB.lib_joomla.ini");

		if ($pag =~ m/JLIB_INSTALLER_ABORT_FILE_INSTALL_CUSTOM_INSTALL_FAILURE/) {
			$version[2] = "4";
		}
		else {
			$version[6] = "3";
		}
	}
	if ($version[0] eq "1" && $version[1] eq "6" && $version[2] eq "4" && $version[4] eq "1" && $version[5] eq "6" && $version[6] eq "6") {
		$pag = getpage($url . "/language/en-GB/en-GB.files_joomla.sys.ini");

		if ($pag =~ m/1\.6\.4 Content Management System/) {
			$version[6] = "4";
		}
		else {
			$version[2] = "5";
		}
	}
}

sub scanforfiles() {
	my $file = shift;
	my $pag;
	my @tmp;
	my $aux = '';
	my @verTmp;
	my @lFile;
	my @lVersion;
	my @lVersionAlt;

	$file .= ".txt";

	print "Scanning " . $file . " ";
	open(DAT, "files/" . $file) || die("File " . $file . " not found. Try --force-update\n");

	while (<DAT>) {
		if (($_ !~ /^#/)) {
			@tmp = split(/\|/, $_);

			if ($#tmp > 1) {
				push @lFile, $tmp[0];
				push @lVersion, $tmp[1];
				push @lVersionAlt, $tmp[2];
			}
		}
	}

	close(DAT);

	for (my $i = 0; $i <= $#lFile; $i++) {
		if ($lFile[$i] =~ m/\$admin/) {
			$lFile[$i] =~ s/\$admin//g;
			$pag = checkpage($url . $admin . $lFile[$i]);
		}
		else {
			$pag = checkpage($url . $lFile[$i]);
		}

		if ($pag eq 1) {
			my @aux1 = split(/\-/, $lVersion[$i]);

			if ($#aux1 > 0) {
				my @aux2 = split(/\./, $aux1[0]);
				my @aux3 = split(/\./, $aux1[1]);

				push @aux2, "" if ($#aux2 eq 2);
				push @aux3, "" if ($#aux3 eq 2);

				@verTmp = ($aux2[0], $aux2[1], $aux2[2], $aux2[3]);
				push @verTmp, $aux3[0], $aux3[1], $aux3[2], $aux3[3];

				if ($verTmp[2] ne "x" && ($version[2] eq "x" || $verTmp[2] > $version[2] || ($verTmp[2] eq $version[2] && $verTmp[3] ne $version[3])) && $version[6] ne "x" && $verTmp[2] <= $version[6]) {
					$version[0] = $verTmp[0];
					$version[1] = $verTmp[1];
					$version[2] = $verTmp[2];
					$version[3] = $verTmp[3];
				}

				if ($verTmp[6] ne "x" && ($version[6] eq "x" || $verTmp[6] < $version[6] || ($verTmp[6] eq $version[6] && $verTmp[7] ne $version[7]))) {
					if ($version[5] eq $verTmp[5]) {
						$version[4] = $verTmp[4];
						$version[5] = $verTmp[5];
						$version[6] = $verTmp[6];
						$version[7] = $verTmp[7];
					}
				}
			}
		}
		elsif ($lVersionAlt[$i] ne "") {
			my @aux1 = split(/\-/, $lVersionAlt[$i]);

			if ($#aux1 > 0) {
				my @aux2 = split(/\./, $aux1[0]);
				my @aux3 = split(/\./, $aux1[1]);

				push @aux2, "" if ($#aux2 eq 2);
				push @aux3, "" if ($#aux3 eq 2);

				@verTmp = ($aux2[0], $aux2[1], $aux2[2], $aux2[3]);
				push @verTmp, $aux3[0], $aux3[1], $aux3[2], $aux3[3];

				if ($verTmp[2] ne "x" && ($version[2] eq "x" || $verTmp[2] > $version[2] || ($verTmp[2] eq $version[2] && $verTmp[3] ne $version[3])) && $version[6] ne "x" && $verTmp[2] <= $version[6]) {
					$version[0] = $verTmp[0];
					$version[1] = $verTmp[1];
					$version[2] = $verTmp[2];
					$version[3] = $verTmp[3];
				}

				if ($verTmp[6] ne "x" && ($version[6] eq "x" || $verTmp[6] < $version[6] || ($verTmp[6] eq $version[6] && $verTmp[7] ne $version[7]))) {
					if ($version[5] eq $verTmp[5]) {
						$version[4] = $verTmp[4];
						$version[5] = $verTmp[5];
						$version[6] = $verTmp[6];
						$version[7] = $verTmp[7];
					}
				}
			}
		}
	}

	print "\n";
}

sub scanspecialcases() {
	my $pag = shift;
	my @tmp;
	my $aux = '';
	my @verTmp;
	my @lContent;
	my @lVersion;

	if ($pag =~ m/Problem with Joomla site/) {
		if ($version[2] ne "x" && $version[2] ne $version[6]) {
			$version[0] = "1";
			$version[4] = "1";
			$version[1] = "5";
			$version[5] = "5";
			$version[2] = "17";
			$version[6] = "17";
			$version[3] = "Stable";
			$version[7] = "Stable";
		}
	}
    else {
		if ($version[0] eq "1" && $version[1] == "5") {
			if ($version[2] ne $version[6]) {
				if ($version[2] eq "17" && $version[6] > "17") {
					$version[2] = "18";
				}

				if ($version[6] == "17" && $version[2] < "17") {
					$version[6] = "16";
				}
			}
		}
	}

	if ($version[0] ne $version[4] || $version[1] ne $version[5] || $version[2] ne $version[6] || $version[3] ne $version[7]) {
		$pag = getpage($url . "libraries/joomla/template/tmpl/adminlists.html");

		if ($pag eq "" && ($version[1] eq "x" || $version[1] eq "6") && ($version[3] ne "Stable")) {
			@verTmp = ("1", "6", "0", "beta1");
			push @verTmp, "1", "6", "0", "beta8";

			if ($verTmp[6] ne "x" && ($version[2] eq "x" || $verTmp[6] > $version[2]) && $version[1] eq $verTmp[5]) {
				$version[0] = $verTmp[0];
				$version[1] = $verTmp[1];
				$version[2] = $verTmp[2];
				$version[3] = $verTmp[3];
			}

			if ($verTmp[6] ne "x" && ($version[6] eq "x" || $verTmp[6] < $version[6])) {
				$version[4] = $verTmp[4];
				$version[5] = $verTmp[5];
				$version[6] = $verTmp[6];
				$version[7] = $verTmp[7];
			}
		}
	}
}

sub scanlanguagefile() {
	my $pag = shift;
	my $file = shift;
	my @tmp;
	my $aux = '';
	my @verTmp;
	my @lContent;
	my @lVersion;

	$file .= ".txt";

	print "Scanning " . $file . " ";
	open(DAT, "files/" . $file) || die("File " . $file . " not found. Try --force-update\n");

	while (<DAT>) {
		if (($_ !~ /^#/)) {
			@tmp = split(/\|/, $_);

			push @lContent, $tmp[0];
			push @lVersion, $tmp[1];
		}
	}

	close(DAT);

	for (my $i = 0; $i <= $#lContent; $i++) {
		if ($lContent[$i] =~ m/\&/) {
			@tmp = split(/\&/, $lContent[$i]);

			if ($#tmp > 0) {
				$aux = $lVersion[$i] if ($pag =~ m/$tmp[0]/ && $pag =~ m/$tmp[1]/);
			}
		}
		else {
			$aux = $lVersion[$i] if ($pag =~ m/$lContent[$i]/);
		}
	}

	my @aux1 = split(/\-/, $aux);

	if ($#aux1 > 0) {
		my @aux2 = split(/\./, $aux1[0]);
		my @aux3 = split(/\./, $aux1[1]);

		push @aux2, "" if ($#aux2 eq 2);
		push @aux3, "" if ($#aux3 eq 2);

		@verTmp = ($aux2[0], $aux2[1], $aux2[2], $aux2[3]);
		push @verTmp, $aux3[0], $aux3[1], $aux3[2], $aux3[3];

		if ($version[2] eq "x" || $verTmp[1] > $version[1] || ($verTmp[2] > $version[2] && $verTmp[1] eq $version[1]) || ($verTmp[2] eq $version[2] && $verTmp[3] ne $version[3])) {
			$version[0] = $verTmp[0];
			$version[1] = $verTmp[1];
			$version[2] = $verTmp[2];
			$version[3] = $verTmp[3];
		}

		if ($verTmp[6] ne "x" && ($version[6] eq "x" || $verTmp[5] < $version[5] || ($verTmp[6] < $version[6] && $verTmp[5] eq $version[5]) || ($verTmp[6] eq $version[6] && $verTmp[7] ne $version[7]))) {
			$version[4] = $verTmp[4];
			$version[5] = $verTmp[5];
			$version[6] = $verTmp[6];
			$version[7] = $verTmp[7];
		}
	}

	print "\n";
}

sub scanconfigfile() {
	my $pag = shift;
	my $file = shift;
	my @tmp;
	my $aux = '';
	my @verTmp;
	my @lContent;
	my @lVersion;
	my @lVersionAlt;
	my @lInverse;

	$file .= ".txt";

	print "Scanning " . $file . " ";
	open(DAT, "files/" . $file) || die("File " . $file . " not found. Try --force-update\n");

	while (<DAT>) {
		if (($_ !~ /^#/)) {
			@tmp = split(/\|/, $_);

			if (($tmp[0] =~ /^!/)) {
				push @lContent, substr $tmp[0], 1;
				push @lInverse, "1";
			}
			else {
				push @lContent, $tmp[0];
				push @lInverse, "0";
			}

			push @lVersion, $tmp[1];
			push @lVersionAlt, $tmp[2] if ($#tmp > 1);
		}
	}

	close(DAT);

	for (my $i = 0; $i <= $#lContent; $i++) {
		if ($pag =~ m/$lContent[$i]/) {
			$aux = $lVersion[$i];
		}
		else {
			$aux = $lVersionAlt[$i] if ($lInverse[$i] eq "1");
		}
	}

	my @aux1 = split(/\-/, $aux);

	if ($#aux1 > 0) {
		my @aux2 = split(/\./, $aux1[0]);
		my @aux3 = split(/\./, $aux1[1]);

		push @aux2, "" if ($#aux2 eq 2);
		push @aux3, "" if ($#aux3 eq 2);

		@verTmp = ($aux2[0], $aux2[1], $aux2[2], $aux2[3]);
		push @verTmp, $aux3[0], $aux3[1], $aux3[2], $aux3[3];

		if ($version[2] eq "x" || $verTmp[1] > $version[1] || ($verTmp[2] > $version[2] && $verTmp[1] eq $version[1]) || ($verTmp[2] eq $version[2] && $verTmp[3] ne $version[3])) {
			$version[0] = $verTmp[0];
			$version[1] = $verTmp[1];
			$version[2] = $verTmp[2];
			$version[3] = $verTmp[3];
		}

		if ($verTmp[6] ne "x" && ($version[6] eq "x" || $verTmp[5] < $version[5] || ($verTmp[6] < $version[6] && $verTmp[5] eq $version[5]) || ($verTmp[6] eq $version[6] && $verTmp[7] ne $version[7]))) {
			$version[4] = $verTmp[4];
			$version[5] = $verTmp[5];
			$version[6] = $verTmp[6];
			$version[7] = $verTmp[7];
		}
	}

	print "\n";
}

sub scanmanifestfile {
	my $pag = shift;

		if ($pag =~ m/\<version\>/) {
			$pag =~ /\<version\>([0-9|\.]*)\<\/version\>/;
			my $aux = $1;
			my @tmp = split(/\./, $aux);
			$version[0] = $tmp[0];
			$version[1] = $tmp[1];
			$version[2] = $tmp[2];
			$version[3] = "Stable";
			$version[4] = $tmp[0];
			$version[5] = $tmp[1];
			$version[6] = $tmp[2];
			$version[7] = "Stable";
		}
}

sub scancopyrigth {
	my @aux;

	# search for version 1.0
	@version = search_meta("1.0");

	# search for version 1.5
	@aux = search_meta("1.5");
	@version = @aux if ($aux[2] ne "x");
}

sub search_meta {
	my $check = shift;
	my @ver;

	print "Searching for copyright of version " . $check . "\n";

	switch ($check) {
		case "1.0" {
		    if ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\sOpen\sSource\sMatters/) {
				push @ver,  "1", "0", "0", "", "1", "0", "8", "";
			}
			elsif ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\-\2006\sOpen\sSource\sMatters/) {
				push @ver,  "1", "0", "9", "", "1", "0", "12", "";
			}
			elsif ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\-\2006\-\2007\sOpen\sSource\sMatters/) {
				push @ver,  "1", "0", "13", "", "1", "0", "15", "";
			}
			else {
				push @ver,  "x", "x", "x", "", "x", "x", "x", "";
			}
		}

		case "1.5" {
		    if ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\-\2006\-\2007\sOpen\sSource\sMatters/) {
				push @ver,  "1", "5", "0", "RC1", "1", "5", "0", "RC4";
			}
			elsif ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\-\2008\sOpen\sSource\sMatters/) {
				push @ver,  "1", "5", "0", "Stable", "1", "5", "12", "Stable";
			}
			elsif ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\-\2009\sOpen\sSource\sMatters/) {
				push @ver,  "1", "5", "13", "Stable", "1", "5", "15", "Stable";
			}
			elsif ($index =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\-\2010\sOpen\sSource\sMatters/) {
				push @ver,  "1", "5", "16", "Stable", "1", "5", "20", "Stable";
			}
			else {
				push @ver,  "x", "x", "x", "", "x", "x", "x", "";
			}
		}
		else {
			push @ver,  "x", "x", "x", "", "x", "x", "x", "";
		}
	}

	return @ver;
}


#########################
# search for components #
#########################

sub scancomponents {
	my $html = $index;

	print "Searching for components ";

	# search for com_ ... end with &, ", ' /
	while ($html =~ m{com_(.*?)(&|"|'|/)}ig) {
		if (checkcomponent("com_" . $1, @components) eq 0) {
			push @components, "com_" . $1;
		}
	}

	print "\n";
}

sub checkcomponent {
	my($what, @array) = @_;

	foreach (0..$#array) {
		if ($what eq $array[$_]) {
			return 1;
		}
	}

	0;
}


#######################
# search for firewall #
#######################

sub scanfirewall {
	print "Searching for firewall\n";

    $firewall = "com_rsfirewall" if( checkpage($url . $admin . "/components/com_rsfirewall/") eq 1 or
		                             checkpage($url . "/components/com_rsfirewall/") eq 1 or
		                             checkpage($url . $admin . "/components/com_firewall/") eq 1 or
                                     checkpage($url . "/components/com_firewall/") eq 1)
}


####################
# check data files #
####################

sub checkdatafiles {
	for (my $i = 0; $i <= $#data; $i++) {
		open(DAT, "files/" . $data[$i]) || die("File " . $data[$i] . " not found. Try --force-update\n");
		close(DAT);
	}

	$index = getpage($url);
}

###################
# download a page #
###################

sub getpage {
	my $pageurl = shift;

	if (checkpage($pageurl) eq 1) {
		my $req = HTTP::Request->new(GET => $pageurl);
		$req->content_type('application/x-www-form-urlencoded');
		my $res = $ua->request($req);
		my $response = $res->content;

		return $response;
	}

	"";
}


#########################
# check if exist a page #
#########################

sub checkpage {
	my $pageurl = shift;
	my $req = HEAD "$pageurl";
	my $res = $ua->request($req);

	return 1 if ($res->status_line =~ /(200|301|302|403)/);

    0;
}


####################
# check web server #
####################

sub checkwebserver {
	my $pageurl = shift;
	my $req = HEAD $pageurl;
	my $res = $ua->simple_request($req);
	return $res->header('server');
}


######################
# print final report #
######################

sub printscreen {
	if ($webserver ne "") {
		print "Running on " . $webserver . "\n\n";
	}

	if ($all eq 1) {
		if ($firewall ne "") { print "Firewall: " . $firewall . "\n\n"; }
		else { print "No firewall detected\n\n"; }
	}

	if ($all eq 1) {
		print "\nComponents:\n";

		foreach (@components) {
			print "\t" . $_ . "\n";
		}

		print "\n";
	}

	if ($all eq 1) {
		my $jversion = getversion();
		print $jversion . "\n\n";
	}

	if ($all eq 1) {
		print "Security tips:\n";
		print "=============\n";

		for (my $i = 0; $i <= $#sVulnerability; $i++) {
			print "Info: " . $sVulnerability[$i] . "\n";
			print "Versions affected: " . $sVersion[$i] . "\n";
			print "Files affected: " . $sFile[$i] . "\n";
			print "Detail: " . $sExploit[$i] . "\n";

			if ($sUrlExploit[$i] =~ m/ /) {
				print "More info: ";

				my @aux = split(/ /, $sUrlExploit[$i]);

				foreach (@aux) {
					print $_ . "\n";
				}
			}
			else {
				print "More info: " . $sUrlExploit[$i] . "\n";
			}

			print "\n";
		}
	}

	if ($all eq 1) {
		print "Possible vulnerabilities in core:\n";
		print "================================\n";

		for (my $i = 0; $i <= $#bVulnerability; $i++) {
			if ($bType[$i] eq "Core") {
				print "Possible vulnerability: " . $bVulnerability[$i] . "\n";
				print "Versions affected: " . $bVersion[$i] . "\n";
				print "Detail: " . $bExploit[$i] . "\n";

				if ($bUrlExploit[$i] =~ m/ /) {
					print "More info: ";

					my @aux = split(/ /, $bUrlExploit[$i]);

					foreach (@aux) {
						print $_ . "\n";
					}
				}
				else {
					print "More info: " . $bUrlExploit[$i] . "\n";
				}
			}
		}

		print "\n";
	}

	if ($all eq 1) {
		print "Possible vulnerabilities in components:\n";
		print "======================================\n";

		for (my $i = 0; $i <= $#bVulnerability; $i++) {
			if ($bType[$i] eq "Component") {
				print "Possible vulnerability: " . $bVulnerability[$i] . "\n";
				print "Versions affected: " . $bVersion[$i] . "\n";
				print "Detail: " . $bExploit[$i] . "\n";

				if ($bUrlExploit[$i] =~ m/ /) {
					print "More info: ";

					my @aux = split(/ /, $bUrlExploit[$i]);

					foreach (@aux) {
						print $_ . "\n";
					}
				}
				else {
					print "More info: " . $bUrlExploit[$i] . "\n";
				}
			}
		}

		print "\n";
	}
}

sub getversion {
	my $jversion = '';

	$version[3] = "." . trim($version[3]) if ($version[3] ne "");
	$version[7] = "." . trim($version[7]) if ($version[7] ne "");

	if ($version[5] eq "x") { # generic version
		if ($version[0] ne "x") { # exact
			if ($version[1] ne "x" && $version[2] ne "x") {
				$jversion = "Joomla! version [" . $version[0] . "." + $version[1] . "." . $version[2] . $version[3] . "]";
			}
			else {
				$jversion = "Generic version family [" . $version[0] . "." . $version[1] . "." . $version[2] . $version[3] . "]";
			}
		}
		else { # unknown
			$jversion = "Version unknown";
		}
	}
	else { # exact
		if ($version[0] eq $version[4] && $version[1] eq $version[5] && $version[2] eq $version[6] && $version[3] eq $version[7]) {
			$jversion = "Joomla! version [" . $version[0] . "." . $version[1] . "." . $version[2] . $version[3] . "]";
		}
		else { # by ranks
			$jversion = "Version family " . $version[0] . "." . $version[1] . ".x ";
			$jversion .= "[" . $version[0] . "." . $version[1] . "." . $version[2] . $version[3];
			$jversion .= "-" . $version[4] . "." . $version[5].+ "." . $version[6] . $version[7] . "]";
		}
	}

	return $jversion;
}

sub trim($) {
	my $string = shift;

	$string =~ s/^\s+//;
	$string =~ s/\s+$//;

	return $string;
}
