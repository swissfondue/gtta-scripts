# Dual Edition Admin Login Finder
# ---
# CODING BY : gunslinger_
# EMAIL     : gunslinger.devilzc0de@gmail.com

use MooseX::Declare;
use core::task qw(execute);

# Login pages
class Login_Pages extends Task {
    use constant TIMEOUT => 3600;
    use HTTP::Request;
    use LWP::UserAgent;

    # Process
    method _process(Str $target, Str $proto, Str $code) {
        my ($UserAgent, $hasil, $Path, $TargetURL);

        $target = "$proto://$target";

        if ($target !~ /\/$/) {
            $target = $target . '/';
        }

        $self->_write_result("\n");
        $self->_write_result("->[+] Target : $target\n");
        $self->_write_result("->[+] Basic c0de of the site : $code\n");
        $self->_write_result("->[+] Scanning control panel page...\n\n\n");

        if ($code eq "asp") {
            my @path_Asp = (
                'administrator.asp','admin.asp','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/','private/',
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

            foreach $Path (@path_Asp){
                $TargetURL = $target.$Path;
                my $source = HTTP::Request->new(GET => $TargetURL);
                $UserAgent = LWP::UserAgent->new;
                $UserAgent->agent("checking");
                $UserAgent->timeout(30);
                my $response = $UserAgent->get($TargetURL);
                $hasil = $response->status_line;
                $self->_write_result("\n[+] $TargetURL \n[!] status => $hasil\n");
                my $View_Source = $UserAgent->request($source);

                if ($View_Source->content =~ /Username/ ||
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
                ) {
                    $self->_write_result("[!] Admin page Login Possibilities => YES !!\n\n");
                } else {
                    $self->_write_result("[!] Admin page Login Possibilities => NO...\n\n");
                }
            }
        }

        if ($code eq "php") {
            my @path_Php = (
                'administrator.php','admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
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

            foreach $Path (@path_Php) {
                $TargetURL = $target.$Path;
                my $source = HTTP::Request->new(GET => $TargetURL);
                $UserAgent = LWP::UserAgent->new;
                $UserAgent->agent("checking");
                $UserAgent->timeout(30);
                my $response = $UserAgent->get($TargetURL);
                $hasil = $response->status_line;
                $self->_write_result("\n[+] $TargetURL \n[!] status => $hasil\n");
                my $View_Source = $UserAgent->request($source);

                if ($View_Source->content =~ /Username/ ||
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
                ) {
                    $self->_write_result("[!] Admin page Login Possibilities => YES !!\n\n");
                } else {
                    $self->_write_result("[!] Admin page Login Possibilities => NO...\n\n");
                }
            }
        }

        if ($code eq "cfm") {
            my @path_Cfm = (
                'administrator.cfm','admin.php','admin/','administrator/','moderator/','webadmin/','adminarea/','bb-admin/','adminLogin/','admin_area/','panel-administracion/','instadmin/',
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

            foreach $Path (@path_Cfm) {
                $TargetURL = $target.$Path;
                my $source = HTTP::Request->new(GET => $TargetURL);
                $UserAgent = LWP::UserAgent->new;
                $UserAgent->agent("checking");
                $UserAgent->timeout(30);
                my $response = $UserAgent->get($TargetURL);
                $hasil = $response->status_line;
                $self->_write_result("\n[+] $TargetURL \n[!] status => $hasil\n");
                my $View_Source = $UserAgent->request($source);

                if ($View_Source->content =~ /Username/ ||
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
                ) {
                    $self->_write_result("[!] Admin page Login Possibilities => YES !!\n\n");
                } else {
                    $self->_write_result("[!] Admin page Login Possibilities => NO...\n\n");
                }
            }
        }
    }

    # Main function
    method main($args) {
        my $code = $self->_get_arg_scalar($args, 0, "php");
        $self->_process($self->target, $self->proto || "http", $code);
    }

    # Test function
    method test {
        $self->_process("google.com", "http", "php");
    }
}

execute(Login_Pages->new());
