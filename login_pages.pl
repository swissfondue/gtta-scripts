#!perl
################################################################
#       .___             __          _______       .___        #
#     __| _/____ _______|  | __ ____ \   _  \    __| _/____    #
#    / __ |\__  \\_  __ \  |/ // ___\/  /_\  \  / __ |/ __ \   #
#   / /_/ | / __ \|  | \/    <\  \___\  \_/   \/ /_/ \  ___/   #
#   \____ |(______/__|  |__|_ \\_____>\_____  /\_____|\____\   #
#        \/                  \/             \/                 #
#                   ___________   ______  _  __                #
#                 _/ ___\_  __ \_/ __ \ \/ \/ /                #
#                 \  \___|  | \/\  ___/\     /                 #
#                  \___  >__|    \___  >\/\_/                  #
#      est.2007        \/            \/   forum.darkc0de.com   #
################################################################
# This is Dual Edition Admin Login Finder .
# This was written for educational purpose and pentest only. Use it at your own risk.
# CODING BY : gunslinger_
# EMAIL     : gunslinger.devilzc0de@gmail.com
# TOOL NAME : AdminLoginFinder.pl
# Version   : 2.0
# Language  : Perl
# Big thanks darkc0de member : d3hydr8, Kopele, icedzomby, VMw4r3 and all member
# Special thanks to devilzc0de crew : mywisdom, petimati, peneter, flyff666, rotlez, 7460, xtr0nic, devil_nongkrong, cruzen and all devilzc0de family
# Author will not be responsible for any damage !!
# Use it with your own risk

# use Tk;
use HTTP::Request;
use LWP::UserAgent;

# $Version    = "1.0";
# $Programmer = "gunslinger_";
# $system="$^O";
#
# if ($system eq linux){
# 	$ClsCR="clear";
# 	} else {
# 	$ClsCR="cls";
# }
#
# system($ClsCR);
# print q{
#   _______     __            __            ___                   __            _______  __            __
#  |   _   |.--|  |.--------.|__|.-----.   |   |   .-----..-----.|__|.-----.   |   _   ||__|.-----..--|  |.-----..----.
#  |.  |   ||  _  ||        ||  ||     |   |.  |   |  _  ||  _  ||  ||     |   |.  |___||  ||     ||  _  ||  -__||   _|
#  |.  _   ||_____||__|__|__||__||__|__|   |.  |___|_____||___  ||__||__|__|   |.  __)  |__||__|__||_____||_____||__|
#  |:  |   |                               |:  |   |      |_____|              |:  |
#  |::.|:. |                               |::.. . |                           |::.|
#  `--- ---'                               `-------'                           `---'
#
#
#   ______                  __     ___ ___                      __
#  |   _  \  .--.--..---.-.|  |   |   Y   |.-----..----..-----.|__|.-----..-----.
#  |.  |   \ |  |  ||  _  ||  |   |.  |   ||  -__||   _||__ --||  ||  _  ||     | __  __  __
#  |.  |    \|_____||___._||__|   |.  |   ||_____||__|  |_____||__||_____||__|__||__||__||__|
#  |:  |    /                     |:  |   |
#  |::.. . /                       \:.. ./
#  `------'                         `---'
#                                                                                           Programmer : gunslinger_
# };
#
#
#
# print "\n What do you like \"CLI\" (Command Line Interpreter) or \"GUI\" (Graphic User Interface) Version to use ? \n -> ";
# 	$Question=<STDIN>;
# 	chomp $Question;

unless ( @ARGV ) { print q[Error: argument list is empty], "\n"; exit(0); };

my @target			= &getinput( $ARGV[0] ) if ( $ARGV[0] );
my $outfile = $ARGV[1];
my @sourcecode		= &getinput( $ARGV[2] ) if ( $ARGV[2] );

# protocol
if (!$target[1])
{
    $target[1] = 'http';
}

my $targethostname	= $target[1] . '://' . $target[0];
my $source			= $sourcecode[0];

open(OUTFILE, ">>$outfile");

$Question = 'cli';

if( $Question eq "gui" || $Question eq "GUI"){
	&GUI()
	}
if( $Question eq "cli" || $Question eq "CLI"){
	&CLI( $targethostname, $source );
	}
else {
	exit;
}

close(OUTFILE);

sub GUI(){
# $main = MainWindow->new(-bg=>'black', -cursor=> "crosshair", -foreground => "green");
# $main -> title("Admin login finder $Version Black Gui Edition");
#
# # Yeah i got center..
# $main -> geometry("800x750+300+50");
#
# $header = $main->Photo(-file=>"alf.gif",
# 		-format=>"gif");
# $header = $main->Label(-image=>$header,
# 		-borderwidth=>0, -width=>1000, -bg=>'#000000')
# 		->pack(-side=>'top');
#
# # Lets Bind control key ;)
#
# $main ->bind('<Key-Escape>', sub { MsgExitApp(); });
#
# # Head text
#
# $space1 = $main->Frame(-bg=>'#000000')
# 		->pack(-side=>'top');
#
# $MyHead = $space1->Label(-text=>"By $Programmer",
# 		-bg=>'black',-foreground=>'#cccccc',
# 		-font=>'bold')
# 		->pack(-side=>'top');
#
# $Next = $space1->Label(-text=>"",
# 		-bg=>'#000000',-foreground=>'#cccccc')
# 		->pack(-side=>'top');
#
# $texty2 = $main->Frame(-bg=>'black')
# 	->pack(-side=>'top');
#
# $texty2->Label(-text=>" Target URL :",-bg=>'black',
# 		-foreground=>'#0cff00')
# 		->pack(-side=>'left');
#
# $hostname = $texty2->Entry(-width=>30,
# 		-bg=>'black', -foreground=>'#0cff00',
# 		-text=>'http://www.devilc0de.com')
# 		->pack(-side=>'left');
#
# $space2 = $main->Frame(-bg=>'#000000')
# 	->pack(-side=>'top');
#
# $Center = $space2->Label(-text=>"",
# 		-bg=>'#000000',-foreground=>'#cccccc')
# 		->pack(-side=>'top');
#
# #Taking source
#
# $frame_c = $main->Frame(-bg=>'black')
# 		->pack(-side=>'top');
#
# $frame_c->Label(-text=>" Source :",-bg=>'#000000',
# 		-foreground=>'#0cff00')
# 		->pack(-side=>'top');
#
# $rdb_m = $frame_c -> Radiobutton(-text=>"Php",
# 			-value=>"php",  -variable=>\$source,
# 			-bg=>'#000000', -foreground=>'#0cff00',
# 			-activebackground=>'#0cfff0')
# 			->pack(-side=>'left');
#
# $rdb_f = $frame_c -> Radiobutton(-text=>"Asp",
# 			-value=>"asp",-variable=>\$source,
# 			-bg=>'#000000', -foreground=>'#0cff00',
# 			-activebackground=>'#0cfff0')
# 			->pack(-side=>'left');
#
# $rdb_f = $frame_c -> Radiobutton(-text=>"Cfm",
# 			-relief=>"raised", -value=>"cfm",
# 			-variable=>\$source, -bg=>'#000000',
# 			-foreground=>'#0cff00', -activebackground=>'#0cfff0')
# 			->pack(-side=>'left');
#
# # Eof Taking source
#
# $space3 = $main->Frame(-bg=>'#000000')
# 	->pack(-side=>'top');
#
# $Next2 = $space3->Label(-text=>"",
# 		-bg=>'#000000',-foreground=>'#cccccc')
# 		->pack(-side=>'top');
#
# $id2 = $main->Frame(-bg=>'#000000')
# 	->pack(-side=>'top');
#
# $scan_start = $id2->Button(-width=>30, -text=>'Start scan',
# 		-bg=>'black', -activebackground=>'#0000ff',
# 		-foreground=>'#0cff00',-command=>\&start_scan)
# 		->pack(-side=>'left', -pady=>5);
#
# $closer = $id2->Button(-width=>30,
# 		-text=>'Close', -bg=>'black',
# 		-activebackground=>'#0000ff', -foreground=>'#0cff00',
# 		-command=>\&MsgExitApp)
# 	->pack(-side=>'right', -pady=>5);
#
# $MyFoot = $main->Frame(-bg=>'#000000')
# 		->pack(-side=>'top');
#
# $End = $MyFoot->Label(-text=>"",
# 		-bg=>'black',-foreground=>'#cccccc')
# 		->pack(-side=>'top');
#
# $space4 = $main->Frame(-bg=>'#000000',
# 		-relief=>'flat')
# 		->pack(-side=>'top');
#
# $box = $space4->Scrolled('Text',
# 		-bg=>'black', -foreground=>'#0cff00',
# 		-width=>100, -height=>30,
# 		-scrollbars => 'oe')
# 		->pack(-side=>'top', -pady=>3);
#
# $MyFooter = $main->Frame(-bg=>'#000000')
# 		->pack(-side=>'bottom');
#
# $Ends = $MyFooter->Label(-text=>"",
# 		-bg=>'black',-foreground=>'#cccccc')
# 		->pack(-side=>'bottom');

# MainLoop;

sub MsgExitApp() {
	$response = $main -> messageBox(-message=>"Quit Admin Login Finder ?",
		-type=>'yesno',-icon=>'question',
		-bg=>"#000000", -foreground=>'#0cff00',
		-activebackground=>"red", -title=>"Quit Admin Login Finder");

	if( $response eq "Yes" ) {
		exit;
	} else {
		$main -> messageBox(-type=>"ok",
		-message=>"Keep trying...", -bg=>"#000000",
		-foreground=>'#0cff00', -activebackground=>'#0cff00',
		-title=>"back 2 program...", -width=>"30");
	}
}

sub start_scan(){

# $targethostname = $hostname  -> get;

if ( $targethostname !~ /^http:/ ) {
	$targethostname = 'http://' . $targethostname;
	}
if ( $targethostname !~ /\/$/ ) {
	$targethostname = $targethostname . '/';
	}

$box->insert("end","\n");
$box->insert("end","->[+] Target : $targethostname\n");
$box->insert("end","->[+] Basic c0de of the site : $source\n");
$box->insert("end","->[+] Scanning control panel page...\n\n\n");
$main->update;

if($source eq "asp"){

@path_Asp=('administrator.asp','admin.asp','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/','private/',
'memberadmin/','administratorlogin/','adm/','account.asp','admin/account.asp','admin/index.asp','admin/login.asp','admin/admin.asp',
'admin_area/admin.asp','admin_area/login.asp','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.asp','bb-admin/index.asp','bb-admin/login.asp','bb-admin/admin.asp',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
'admin/home.asp','admin/controlpanel.asp','admin.asp','pages/admin/admin-login.asp','admin/admin-login.asp','admin-login.asp','admin/cp.asp','cp.asp',
'administrator/account.asp','administrator.asp','login.asp','modelsearch/login.asp','moderator.asp','moderator/login.asp','administrator/login.asp',
'moderator/admin.asp','controlpanel.asp','admin/account.html','adminpanel.html','webadmin.html','pages/admin/admin-login.html','admin/admin-login.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.asp','user.html','admincp/index.asp','admincp/login.asp','admincp/index.html',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
'admincontrol/login.html','adm/index.html','adm.html','admincontrol.asp','admin/account.asp','adminpanel.asp','webadmin.asp','webadmin/index.asp',
'webadmin/admin.asp','webadmin/login.asp','admin/admin_login.asp','admin_login.asp','panel-administracion/login.asp','adminLogin.asp',
'admin/adminLogin.asp','home.asp','admin.asp','adminarea/index.asp','adminarea/admin.asp','adminarea/login.asp','admin-login.html',
'panel-administracion/index.asp','panel-administracion/admin.asp','modelsearch/index.asp','modelsearch/admin.asp','administrator/index.asp',
'admincontrol/login.asp','adm/admloginuser.asp','admloginuser.asp','admin2.asp','admin2/login.asp','admin2/index.asp','adm/index.asp',
'adm.asp','affiliate.asp','adm_auth.asp','memberadmin.asp','administratorlogin.asp','siteadmin/login.asp','siteadmin/index.asp','siteadmin/login.html','admin2009.asp',
'cekadmin.asp','admin2009.asp','logon.asp','secure.asp','securelogon.asp','admiin.asp','secure.asp','secure/index.asp','checkadministrator.asp','administratorlogon.asp',
'checker,asp','securewebadministrator.asp','testadmin.asp','logonadministratorweb.asp','log.php','secure/','area52.asp','adminzone.asp','oneadmin.asp','zoneadmin.asp',
'administratoor.asp','checkerinput.asp','account.asp','accountlogon.asp','secureaccount.php','akun.php','control.php','webcontrol/','controlweb/','webcontoller.php',
);

foreach $Path(@path_Asp){
$TargetURL=$targethostname.$Path;
my $source=HTTP::Request->new(GET=>$TargetURL);
$UserAgent=LWP::UserAgent->new;
$UserAgent->agent("checking");
$UserAgent->timeout(30);
my $response=$UserAgent->get($TargetURL);
$hasil=$response->status_line;
$box->insert("end","\n[+] $TargetURL \n[!] status => $hasil\n");
$main->update;
my $View_Source=$UserAgent->request($source);

if($View_Source->content =~ /Username/ ||
	$View_Source->content =~ /Password/ ||
	$View_Source->content =~ /username/ ||
	$View_Source->content =~ /password/ ||
	$View_Source->content =~ /USERNAME/ ||
	$View_Source->content =~ /PASSWORD/ ||
	$View_Source->content =~ /Senha/ ||
	$View_Source->content =~ /senha/ ||
	$View_Source->content =~ /Personal/ ||
	$View_Source->content =~ /Usuario/ ||
	$View_Source->content =~ /Clave/ ||
	$View_Source->content =~ /Usager/ ||
	$View_Source->content =~ /usager/ ||
	$View_Source->content =~ /Sing/ ||
	$View_Source->content =~ /passe/ ||
	$View_Source->content =~ /P\/W/
){
$box->insert("end","[!] Admin page Login Possibilities => YES !!\n\n");
$main->update;
}else{
$box->insert("end","[!] Admin page Login Possibilities => NO...\n\n");
$main->update;
}
}
}

if($source eq "php"){

@path_Php=('administrator.php','admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
'memberadmin/','administratorlogin/','adm/','admin/account.php','admin/index.php','admin/login.php','admin/admin.php','admin/account.php',
'admin_area/admin.php','admin_area/login.php','siteadmin/login.php','siteadmin/index.php','siteadmin/login.html','admin/account.html','admin/index.html',
'admin login.html','admin/admin.html',
'admin_area/index.php','bb-admin/index.php','bb-admin/login.php','bb-admin/admin.php','admin/home.php','admin_area/login.html','admin_area/index.html',
'admin/controlpanel.php','admin.php','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
'admin/cp.php','cp.php','administrator/index.php','administrator/login.php','nsw/admin/login.php','webadmin/login.php','admin/admin_login.php','admin_login.php',
'administrator/account.php','administrator.php','admin_area/admin.html','pages/admin/admin-login.php','admin/admin-login.php','admin-login.php',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.php','modelsearch/login.php','moderator.php','moderator/login.php',
'moderator/admin.php','account.php','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.php','admincontrol.php',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.php','adminarea/index.html','adminarea/admin.html',
'webadmin.php','webadmin/index.php','webadmin/admin.php','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.php','moderator.html',
'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.php','account.html','controlpanel.html','admincontrol.html',
'panel-administracion/login.php','wp-login.php','adminLogin.php','admin/adminLogin.php','home.php','secureadmin.php','adminarea/index.php',
'adminarea/admin.php','adminarea/login.php','panel-administracion/index.php','panel-administracion/admin.php','modelsearch/index.php',
'modelsearch/admin.php','admincontrol/login.php','adm/admloginuser.php','admloginuser.php','admin2.php','admin2/login.php','admin2/index.php',
'adm/index.php','adm.php','affiliate.php','adm_auth.php','memberadmin.php','administratorlogin.php','secureadmin.php','secureadmin/','verysecure.php','securelogon.php',
'admin2009.php','webadministration/','webadministrasi.php','admininput.php','secure.php','secureadministration.php','phpmyadmin/','sosecure.php','hardfound.php',
'dificultadmin.php/','administracion/','root.php','locked.php','locked/','adminnn.php','adminsitus.php','adminsitus/','adminsite/','adminsite.php','administratorsite/',
'adminpageonly/','adminonly.php','admin-site.php','admin-site/','administratorsite.php','usersite.php','maintenance.php','reconstruct.php','pageadmin.php','usersdatabase.php',
'databaseuser.php','databaseusers/','webdatalogin.php','dataadministration.php','homeadmin/','fjk.php','database.php','database/','dataweb/','qwerty.php','account.php',
'account.php','testaccount.php','accountlogon.php','account2009/','accountlogin.php','webaccount.php','databaseuserlogin.php','databaseadministration/','database.php',
'loggon.php','myadmin.php','webadmin.php','checkadmin.php','homeweb.php','webhome.php','adminarea.php','logonpanel.php','loginwebadmin.php'
);

foreach $Path(@path_Php){
$TargetURL=$targethostname.$Path;
my $source=HTTP::Request->new(GET=>$TargetURL);
$UserAgent=LWP::UserAgent->new;
$UserAgent->agent("checking");
$UserAgent->timeout(30);
my $response=$UserAgent->get($TargetURL);
$hasil=$response->status_line;
$box->insert("end","\n[+] $TargetURL \n[!] status => $hasil\n");
$main->update;
my $View_Source=$UserAgent->request($source);

if($View_Source->content =~ /Username/ ||
	$View_Source->content =~ /Password/ ||
	$View_Source->content =~ /username/ ||
	$View_Source->content =~ /password/ ||
	$View_Source->content =~ /USERNAME/ ||
	$View_Source->content =~ /PASSWORD/ ||
	$View_Source->content =~ /Senha/ ||
	$View_Source->content =~ /senha/ ||
	$View_Source->content =~ /Personal/ ||
	$View_Source->content =~ /Usuario/ ||
	$View_Source->content =~ /Clave/ ||
	$View_Source->content =~ /Usager/ ||
	$View_Source->content =~ /usager/ ||
	$View_Source->content =~ /Sing/ ||
	$View_Source->content =~ /passe/ ||
	$View_Source->content =~ /P\/W/
){
$box->insert("end","[!] Admin page Login Possibilities => YES !!\n\n");
$main->update;
}else{
$box->insert("end","[!] Admin page Login Possibilities => NO...\n\n");
$main->update;
}
}
}

if($source eq "cfm"){
@path_Cfm=('administrator.cfm','admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
'memberadmin/','administratorlogin/','adm/','account.cfm','admin/account.cfm','admin/index.cfm','admin/login.cfm','admin/admin.cfm',
'admin_area/admin.cfm','admin_area/login.cfm','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.cfm','bb-admin/index.cfm','bb-admin/login.cfm','bb-admin/admin.cfm',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
'admin/home.cfm','admin/controlpanel.cfm','admin.cfm','pages/admin/admin-login.cfm','admin/admin-login.cfm','admin-login.cfm','admin/cp.cfm','cp.cfm',
'administrator/account.cfm','administrator.cfm','login.cfm','modelsearch/login.cfm','moderator.cfm','moderator/login.cfm','administrator/login.cfm',
'moderator/admin.cfm','controlpanel.cfm','admin/account.html','adminpanel.html','webadmin.html','pages/admin/admin-login.html','admin/admin-login.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.cfm','user.html','admincp/index.cfm','admincp/login.cfm','admincp/index.html',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
'admincontrol/login.html','adm/index.html','adm.html','admincontrol.cfm','admin/account.cfm','adminpanel.cfm','webadmin.cfm','webadmin/index.cfm',
'webadmin/admin.cfm','webadmin/login.cfm','admin/admin_login.cfm','admin_login.cfm','panel-administracion/login.cfm','adminLogin.cfm',
'admin/adminLogin.cfm','home.cfm','admin.cfm','adminarea/index.cfm','adminarea/admin.cfm','adminarea/login.cfm','admin-login.html',
'panel-administracion/index.cfm','panel-administracion/admin.cfm','modelsearch/index.cfm','modelsearch/admin.cfm','administrator/index.cfm',
'admincontrol/login.cfm','adm/admloginuser.cfm','admloginuser.cfm','admin2.cfm','admin2/login.cfm','admin2/index.cfm','adm/index.cfm',
'adm.cfm','affiliate.cfm','adm_auth.cfm','memberadmin.cfm','administratorlogin.cfm','siteadmin/login.cfm','siteadmin/index.cfm','siteadmin/login.html'
);

foreach $Path(@path_Cfm){
my $source=HTTP::Request->new(GET=>$TargetURL);
$UserAgent=LWP::UserAgent->new;
$UserAgent->agent("checking");
$UserAgent->timeout(30);
my $response=$UserAgent->get($TargetURL);
$hasil=$response->status_line;
$box->insert("end","\n[+] $TargetURL \n[!] status => $hasil\n");
$main->update;
my $View_Source=$UserAgent->request($source);

if($View_Source->content =~ /Username/ ||
	$View_Source->content =~ /Password/ ||
	$View_Source->content =~ /username/ ||
	$View_Source->content =~ /password/ ||
	$View_Source->content =~ /USERNAME/ ||
	$View_Source->content =~ /PASSWORD/ ||
	$View_Source->content =~ /Senha/ ||
	$View_Source->content =~ /senha/ ||
	$View_Source->content =~ /Personal/ ||
	$View_Source->content =~ /Usuario/ ||
	$View_Source->content =~ /Clave/ ||
	$View_Source->content =~ /Usager/ ||
	$View_Source->content =~ /usager/ ||
	$View_Source->content =~ /Sing/ ||
	$View_Source->content =~ /passe/ ||
	$View_Source->content =~ /P\/W/
){
$box->insert("end","[!] Admin page Login Possibilities => YES !!\n\n");
$main->update;
}else{
$box->insert("end","[!] Admin page Login Possibilities => NO...\n\n");
$main->update;
}
}
}
}

sub CLI(){
# system($ClsCR);
# system('title Admin Control Panel Finder.....');
# print"\n";
# print "\t+=======================================+\n";
# print "\t+ Control Panel Finder                  +\n";
# print "\t+ Command Line Interpreter (CLI) Edition+\n";
# print "\t+ Version 2.0	                        +\n";
# print "\t+ Programmer : gunslinger_              +\n";
# print "\t+=======================================+\n";
# print "\n";;

# print " Input site address \n ex: \"www.target.com\" or \"http://www.target.com/path\"\n -> ";
$targethostname= shift;
# chomp CLI;

print OUTFILE "\n";
# print " Input basic c0de of the site \n ex : \"asp\" or \"php\" or \"cfm\" \n -> ";
$source= shift;
chomp($source);

if ( $targethostname !~ /\/$/ ) {
	$targethostname = $targethostname . '/';
	}

print OUTFILE "\n";
print OUTFILE "->[+] Target : $targethostname\n";
print OUTFILE "->[+] Basic c0de of the site : $source\n";
print OUTFILE "->[+] Scanning control panel page...\n\n\n";

if($source eq "asp"){

@path_Asp=('administrator.asp','admin.asp','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/','private/',
'memberadmin/','administratorlogin/','adm/','account.asp','admin/account.asp','admin/index.asp','admin/login.asp','admin/admin.asp',
'admin_area/admin.asp','admin_area/login.asp','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.asp','bb-admin/index.asp','bb-admin/login.asp','bb-admin/admin.asp',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
'admin/home.asp','admin/controlpanel.asp','admin.asp','pages/admin/admin-login.asp','admin/admin-login.asp','admin-login.asp','admin/cp.asp','cp.asp',
'administrator/account.asp','administrator.asp','login.asp','modelsearch/login.asp','moderator.asp','moderator/login.asp','administrator/login.asp',
'moderator/admin.asp','controlpanel.asp','admin/account.html','adminpanel.html','webadmin.html','pages/admin/admin-login.html','admin/admin-login.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.asp','user.html','admincp/index.asp','admincp/login.asp','admincp/index.html',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
'admincontrol/login.html','adm/index.html','adm.html','admincontrol.asp','admin/account.asp','adminpanel.asp','webadmin.asp','webadmin/index.asp',
'webadmin/admin.asp','webadmin/login.asp','admin/admin_login.asp','admin_login.asp','panel-administracion/login.asp','adminLogin.asp',
'admin/adminLogin.asp','home.asp','admin.asp','adminarea/index.asp','adminarea/admin.asp','adminarea/login.asp','admin-login.html',
'panel-administracion/index.asp','panel-administracion/admin.asp','modelsearch/index.asp','modelsearch/admin.asp','administrator/index.asp',
'admincontrol/login.asp','adm/admloginuser.asp','admloginuser.asp','admin2.asp','admin2/login.asp','admin2/index.asp','adm/index.asp',
'adm.asp','affiliate.asp','adm_auth.asp','memberadmin.asp','administratorlogin.asp','siteadmin/login.asp','siteadmin/index.asp','siteadmin/login.html','admin2009.asp',
'cekadmin.asp','admin2009.asp','logon.asp','secure.asp','securelogon.asp','admiin.asp','secure.asp','secure/index.asp','checkadministrator.asp','administratorlogon.asp',
'checker,asp','securewebadministrator.asp','testadmin.asp','logonadministratorweb.asp','log.php','secure/','area52.asp','adminzone.asp','oneadmin.asp','zoneadmin.asp',
'administratoor.asp','checkerinput.asp','account.asp','accountlogon.asp','secureaccount.php','akun.php','control.php','webcontrol/','controlweb/','webcontoller.php',
);

foreach $Path(@path_Asp){
$TargetURL=$targethostname.$Path;
my $source=HTTP::Request->new(GET=>$TargetURL);
$UserAgent=LWP::UserAgent->new;
$UserAgent->agent("checking");
$UserAgent->timeout(30);
my $response=$UserAgent->get($TargetURL);
$hasil=$response->status_line;
print OUTFILE "\n[+] $TargetURL \n[!] status => $hasil\n";
my $View_Source=$UserAgent->request($source);

if($View_Source->content =~ /Username/ ||
	$View_Source->content =~ /Password/ ||
	$View_Source->content =~ /username/ ||
	$View_Source->content =~ /password/ ||
	$View_Source->content =~ /USERNAME/ ||
	$View_Source->content =~ /PASSWORD/ ||
	$View_Source->content =~ /Senha/ ||
	$View_Source->content =~ /senha/ ||
	$View_Source->content =~ /Personal/ ||
	$View_Source->content =~ /Usuario/ ||
	$View_Source->content =~ /Clave/ ||
	$View_Source->content =~ /Usager/ ||
	$View_Source->content =~ /usager/ ||
	$View_Source->content =~ /Sing/ ||
	$View_Source->content =~ /passe/ ||
	$View_Source->content =~ /P\/W/
){
print OUTFILE "[!] Admin page Login Possibilities => YES !!\n\n";
}else{
print OUTFILE "[!] Admin page Login Possibilities => NO...\n\n";
}
}
}

if($source eq "php"){

@path_Php=('administrator.php','admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
'memberadmin/','administratorlogin/','adm/','admin/account.php','admin/index.php','admin/login.php','admin/admin.php','admin/account.php',
'admin_area/admin.php','admin_area/login.php','siteadmin/login.php','siteadmin/index.php','siteadmin/login.html','admin/account.html','admin/index.html',
'admin login.html','admin/admin.html',
'admin_area/index.php','bb-admin/index.php','bb-admin/login.php','bb-admin/admin.php','admin/home.php','admin_area/login.html','admin_area/index.html',
'admin/controlpanel.php','admin.php','admincp/index.asp','admincp/login.asp','admincp/index.html','admin/account.html','adminpanel.html','webadmin.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','admin/admin_login.html','admin_login.html','panel-administracion/login.html',
'admin/cp.php','cp.php','administrator/index.php','administrator/login.php','nsw/admin/login.php','webadmin/login.php','admin/admin_login.php','admin_login.php',
'administrator/account.php','administrator.php','admin_area/admin.html','pages/admin/admin-login.php','admin/admin-login.php','admin-login.php',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','login.php','modelsearch/login.php','moderator.php','moderator/login.php',
'moderator/admin.php','account.php','pages/admin/admin-login.html','admin/admin-login.html','admin-login.html','controlpanel.php','admincontrol.php',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','rcjakar/admin/login.php','adminarea/index.html','adminarea/admin.html',
'webadmin.php','webadmin/index.php','webadmin/admin.php','admin/controlpanel.html','admin.html','admin/cp.html','cp.html','adminpanel.php','moderator.html',
'administrator/index.html','administrator/login.html','user.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html',
'moderator/login.html','adminarea/login.html','panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html',
'admincontrol/login.html','adm/index.html','adm.html','moderator/admin.html','user.php','account.html','controlpanel.html','admincontrol.html',
'panel-administracion/login.php','wp-login.php','adminLogin.php','admin/adminLogin.php','home.php','secureadmin.php','adminarea/index.php',
'adminarea/admin.php','adminarea/login.php','panel-administracion/index.php','panel-administracion/admin.php','modelsearch/index.php',
'modelsearch/admin.php','admincontrol/login.php','adm/admloginuser.php','admloginuser.php','admin2.php','admin2/login.php','admin2/index.php',
'adm/index.php','adm.php','affiliate.php','adm_auth.php','memberadmin.php','administratorlogin.php','secureadmin.php','secureadmin/','verysecure.php','securelogon.php',
'admin2009.php','webadministration/','webadministrasi.php','admininput.php','secure.php','secureadministration.php','phpmyadmin/','sosecure.php','hardfound.php',
'dificultadmin.php/','administracion/','root.php','locked.php','locked/','adminnn.php','adminsitus.php','adminsitus/','adminsite/','adminsite.php','administratorsite/',
'adminpageonly/','adminonly.php','admin-site.php','admin-site/','administratorsite.php','usersite.php','maintenance.php','reconstruct.php','pageadmin.php','usersdatabase.php',
'databaseuser.php','databaseusers/','webdatalogin.php','dataadministration.php','homeadmin/','fjk.php','database.php','database/','dataweb/','qwerty.php','account.php',
'account.php','testaccount.php','accountlogon.php','account2009/','accountlogin.php','webaccount.php','databaseuserlogin.php','databaseadministration/','database.php',
'loggon.php','myadmin.php','webadmin.php','checkadmin.php','homeweb.php','webhome.php','adminarea.php','logonpanel.php','loginwebadmin.php'
);



foreach $Path(@path_Php){
$TargetURL=$targethostname.$Path;
my $source=HTTP::Request->new(GET=>$TargetURL);
$UserAgent=LWP::UserAgent->new;
$UserAgent->agent("checking");
$UserAgent->timeout(30);
my $response=$UserAgent->get($TargetURL);
$hasil=$response->status_line;
print OUTFILE "\n[+] $TargetURL \n[!] status => $hasil\n";
my $View_Source=$UserAgent->request($source);

if($View_Source->content =~ /Username/ ||
	$View_Source->content =~ /Password/ ||
	$View_Source->content =~ /username/ ||
	$View_Source->content =~ /password/ ||
	$View_Source->content =~ /USERNAME/ ||
	$View_Source->content =~ /PASSWORD/ ||
	$View_Source->content =~ /Senha/ ||
	$View_Source->content =~ /senha/ ||
	$View_Source->content =~ /Personal/ ||
	$View_Source->content =~ /Usuario/ ||
	$View_Source->content =~ /Clave/ ||
	$View_Source->content =~ /Usager/ ||
	$View_Source->content =~ /usager/ ||
	$View_Source->content =~ /Sing/ ||
	$View_Source->content =~ /passe/ ||
	$View_Source->content =~ /P\/W/
){
print OUTFILE "[!] Admin page Login Possibilities => YES !!\n\n";
}else{
print OUTFILE "[!] Admin page Login Possibilities => NO...\n\n";
}
}
}


if($source eq "cfm"){
@path_Cfm=('administrator.cfm','admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
'memberadmin/','administratorlogin/','adm/','account.cfm','admin/account.cfm','admin/index.cfm','admin/login.cfm','admin/admin.cfm',
'admin_area/admin.cfm','admin_area/login.cfm','admin/account.html','admin/index.html','admin/login.html','admin/admin.html',
'admin_area/admin.html','admin_area/login.html','admin_area/index.html','admin_area/index.cfm','bb-admin/index.cfm','bb-admin/login.cfm','bb-admin/admin.cfm',
'bb-admin/index.html','bb-admin/login.html','bb-admin/admin.html','admin/home.html','admin/controlpanel.html','admin.html','admin/cp.html','cp.html',
'administrator/index.html','administrator/login.html','administrator/account.html','administrator.html','login.html','modelsearch/login.html','moderator.html',
'moderator/login.html','moderator/admin.html','account.html','controlpanel.html','admincontrol.html','admin_login.html','panel-administracion/login.html',
'admin/home.cfm','admin/controlpanel.cfm','admin.cfm','pages/admin/admin-login.cfm','admin/admin-login.cfm','admin-login.cfm','admin/cp.cfm','cp.cfm',
'administrator/account.cfm','administrator.cfm','login.cfm','modelsearch/login.cfm','moderator.cfm','moderator/login.cfm','administrator/login.cfm',
'moderator/admin.cfm','controlpanel.cfm','admin/account.html','adminpanel.html','webadmin.html','pages/admin/admin-login.html','admin/admin-login.html',
'webadmin/index.html','webadmin/admin.html','webadmin/login.html','user.cfm','user.html','admincp/index.cfm','admincp/login.cfm','admincp/index.html',
'admin/adminLogin.html','adminLogin.html','admin/adminLogin.html','home.html','adminarea/index.html','adminarea/admin.html','adminarea/login.html',
'panel-administracion/index.html','panel-administracion/admin.html','modelsearch/index.html','modelsearch/admin.html','admin/admin_login.html',
'admincontrol/login.html','adm/index.html','adm.html','admincontrol.cfm','admin/account.cfm','adminpanel.cfm','webadmin.cfm','webadmin/index.cfm',
'webadmin/admin.cfm','webadmin/login.cfm','admin/admin_login.cfm','admin_login.cfm','panel-administracion/login.cfm','adminLogin.cfm',
'admin/adminLogin.cfm','home.cfm','admin.cfm','adminarea/index.cfm','adminarea/admin.cfm','adminarea/login.cfm','admin-login.html',
'panel-administracion/index.cfm','panel-administracion/admin.cfm','modelsearch/index.cfm','modelsearch/admin.cfm','administrator/index.cfm',
'admincontrol/login.cfm','adm/admloginuser.cfm','admloginuser.cfm','admin2.cfm','admin2/login.cfm','admin2/index.cfm','adm/index.cfm',
'adm.cfm','affiliate.cfm','adm_auth.cfm','memberadmin.cfm','administratorlogin.cfm','siteadmin/login.cfm','siteadmin/index.cfm','siteadmin/login.html'
);
foreach $Path(@path_Cfm){
$TargetURL=$targethostname.$Path;
my $source=HTTP::Request->new(GET=>$TargetURL);
$UserAgent=LWP::UserAgent->new;
$UserAgent->agent("checking");
$UserAgent->timeout(30);
my $response=$UserAgent->get($TargetURL);
$hasil=$response->status_line;
print OUTFILE "\n[+] $TargetURL \n[!] status => $hasil\n";
my $View_Source=$UserAgent->request($source);

if($View_Source->content =~ /Username/ ||
	$View_Source->content =~ /Password/ ||
	$View_Source->content =~ /username/ ||
	$View_Source->content =~ /password/ ||
	$View_Source->content =~ /USERNAME/ ||
	$View_Source->content =~ /PASSWORD/ ||
	$View_Source->content =~ /Senha/ ||
	$View_Source->content =~ /senha/ ||
	$View_Source->content =~ /Personal/ ||
	$View_Source->content =~ /Usuario/ ||
	$View_Source->content =~ /Clave/ ||
	$View_Source->content =~ /Usager/ ||
	$View_Source->content =~ /usager/ ||
	$View_Source->content =~ /Sing/ ||
	$View_Source->content =~ /passe/ ||
	$View_Source->content =~ /P\/W/
){
print OUTFILE "[!] Admin page Login Possibilities => YES !!\n\n";
}else{
print OUTFILE "[!] Admin page Login Possibilities => NO...\n\n";
}
}
}
}
}

sub getinput {

  my $fi = shift;

  if ( open( IN, '<:utf8', $fi ) ) {

	my @fo;

	while( <IN> ){ chomp; push @fo, $_; }

	close( IN );

	return @fo;# if ( scalar @fo > 1 );
	#return $fo[0];

  }
  else { print q[Error: cannot open file ], $fi, "\n"; exit(0); }

};
