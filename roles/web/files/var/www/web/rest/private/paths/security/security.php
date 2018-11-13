<?php

class Rest_Security
{

	// GET /security
	static public function getSecurity() {
          header('Content-Type: text/html; charset=utf-8');
          readfile("paths/security/security.html");
	}

        // GET /security/servers
        static public function getSecurityServers() {
          $query = "SELECT Name, IP, Node FROM Server WHERE Auto and End is Null Order by Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Name' => $val['Name'],'IP' => $val['IP'],'Node' => $val['Node']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/inports
        static public function getSecurityInPorts() {
          $query = "SELECT C.Server, Protocol, Port, IP4, BindIP4 as 'Bind IP4', IP6, BindIP6 as 'Bind IP6', Process FROM ServerPort as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null and Access='IN' Order by C.Server, Protocol, Port";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Protocol' => $val['Protocol'],'Port' => $val['Port'],'IP4' => $val['IP4'],'Bind IP4' => $val['Bind IP4'],'IP6' => $val['IP6'],'Bind IP6' => $val['Bind IP6'],'Process' => $val['Process']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/outports
        static public function getSecurityOutPorts() {
          $query = "SELECT C.Server, Protocol, Port FROM ServerPort as C, Server as S WHERE C.Server=S.Name and S.Auto and S.End is Null and C.Auto and C.End is Null and Access='OUT' Order by C.Server, Protocol, Port";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Protocol' => $val['Protocol'],'Port' => $val['Port']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/packages
        static public function getSecurityPackages() {
          $query = "SELECT C.Server, C.Name, Version, Size FROM Package as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Name, Version";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Version' => $val['Version'],'Size' => $val['Size']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/exes
        static public function getSecurityExes() {
          $query = "SELECT C.Server, C.Name, Package, FileSize as 'File Size', FileUser as 'File User', FileGroup as 'File Group', FilePerms as 'File Perms', Signature FROM Exe as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Name, Signature";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Package' => $val['Package'],'File Size' => $val['File Size'],'File User' => $val['File User'],'File Group' => $val['File Group'],'File Permissions' => $val['File Perms'],'Signature' => $val['Signature']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/exes/nopackage
        static public function getSecurityExesNoPackage() {
          $query = "SELECT C.Server, C.Name, FileSize as 'File Size', FileUser as 'File User', FileGroup as 'File Group', FilePerms as 'File Permssions' from Exe as C, Server as S where C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is null and Package='' order by C.Server, C.Name, Signature";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'File Size' => $val['File Size'],'File User' => $val['File User'],'File Group' => $val['File Group'],'File Permissions' => $val['File Permissions']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/exes/setuid
        static public function getSecurityExesSetuid() {
          $query = "SELECT C.Server, C.Name, Package, FileSize as 'File Size', FileUser as 'File User', FileGroup as 'File Group', FilePerms as 'File Permissions' from Exe as C, Server as S where S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is null and FilePerms like '-__s%' order by C.Server, C.Name, Signature";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Package' => $val['Package'],'File Size' => $val['File Size'],'File User' => $val['File User'],'File Group' => $val['File Group'],'File Permissions' => $val['File Permissions']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/exes/setgid
        static public function getSecurityExesSetgid() {
          $query = "SELECT C.Server, C.Name, Package, FileSize as 'File Size', FileUser as 'File User', FileGroup as 'File Group', FilePerms as 'File Permissions' from Exe as C, Server as S where C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is null and FilePerms like '-_____s%' order by C.Server, C.Name, Signature";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Package' => $val['Package'],'File Size' => $val['File Size'],'File User' => $val['File User'],'File Group' => $val['File Group'],'File Permissions' => $val['File Permissions']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/users
        static public function getSecurityUsers() {
          $query = "SELECT C.Server, C.Name, UID, GID, PasswdType as 'Password Type', LastChange as 'Last Change', Description, Home, Shell FROM LocalUser as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, UID";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'UID' => $val['UID'],'GID' => $val['GID'],'Password Type' => $val['Password Type'],'Last Change' => $val['Last Change'],'Description' => $val['Description'],'Home' => $val['Home'],'Shell' => $val['Shell']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/waccounts
        static public function getSecurityWAccounts() {
          $query = "SELECT C.Server, C.Domain, C.Name, SystemAccount as 'System Account', Caption, AccountType as 'Account Type', Disabled, FullName as 'Full Name', LocalAccount as 'Local Account', Lockout, PasswordChangeable as 'Password Changeable', PasswordExpires as 'Password Expires', PasswordRequired as 'Password Required', SID, SIDType as 'SID Type' FROM WinAccount as C, Server as S WHERE C.Server=S.Name and S.Node='2' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Domain, C.Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Domain' => $val['Domain'],'Name' => $val['Name'],'System Account' => $val['System Account'],'Caption' => $val['Caption'],'Account Type' => $val['Account Type'],'Disabled' => $val['Disabled'],'Full Name' => $val['Full Name'],'Local Account' => $val['Local Account'],'Lockout' => $val['Lockout'],'Password Changeable' => $val['Password Changeable'],'Password Expires' => $val['Password Expires'],'Password Required' => $val['Password Required'],'SID' => $val['SID'],'SID Type' => $val['SID Type']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/groups
        static public function getSecurityGroups() {
          $query = "SELECT C.Server, C.Name, GID FROM LocalGroup as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null ORDER BY C.Server, GID";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT UserName as User FROM LocalGroupUser WHERE Auto and End is Null and Server = :idServer and GroupName = :idGroupName Order by UserName";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'],':idGroupName' => $val['Name']));
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'GID' => $val['GID'],'Users' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/wgroups
        static public function getSecurityWGroups() {
          $query = "SELECT C.Server, C.Domain, C.Name, Caption, LocalAccount as 'Local Account', SID, SIDType as 'SID Type' FROM WinGroup as C, Server as S WHERE C.Server=S.Name and S.Node='2' and S.Auto and S.End is Null and C.Auto and C.End is Null ORDER BY C.Server, C.Domain, C.Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT UserDomain as 'User Domain', UserName as 'User Name' FROM WinGroupUser WHERE Auto and End is Null and Server = :idServer and GroupDomain = :idGroupDomain and GroupName = :idGroupName Order by UserDomain, UserName";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'],'idGroupDomain' => $val['Domain'],':idGroupName' => $val['Name']));
            array_push($result, array('Server' => $val['Server'],'Domain' => $val['Domain'],'Name' => $val['Name'],'Caption' => $val['Caption'],'Local Account' => $val['Local Account'],'SID' => $val['SID'],'SID Type' => $val['SID Type'],'Users' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/sudo
        static public function getSecuritySudo() {
          $query = "SELECT C.Server FROM SudoUserSpec as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null GROUP BY C.Server ORDER BY C.Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery1 = "SELECT Rule FROM SudoDefault WHERE Auto and End is Null and Server = :idServer Order by Num";
            $subdata1 = getDatabase()->all($subquery1, array(':idServer' => $val['Server']));
            $subquery2 = "SELECT Rule as Alias FROM SudoAlias WHERE Auto and End is Null and TypeAlias='userAlias' and Server = :idServer Order by NumAlias";
            $subdata2 = getDatabase()->all($subquery2, array(':idServer' => $val['Server']));
            $subquery3 = "SELECT Rule as Alias FROM SudoAlias WHERE Auto and End is Null and TypeAlias='cmndAlias' and Server = :idServer Order by NumAlias";
            $subdata3 = getDatabase()->all($subquery3, array(':idServer' => $val['Server']));
            $subquery4 = "SELECT Rule as Alias FROM SudoAlias WHERE Auto and End is Null and TypeAlias='runasAlias' and Server = :idServer Order by NumAlias";
            $subdata4 = getDatabase()->all($subquery4, array(':idServer' => $val['Server']));
            $subquery5 = "SELECT Rule FROM SudoUserSpec WHERE Auto and End is Null and Server = :idServer Order by Num";
            $subdata5 = getDatabase()->all($subquery5, array(':idServer' => $val['Server']));
            array_push($result, array('Server' => $val['Server'],'Defaults' => $subdata1,'User Alias' => $subdata2,'Cmnd Alias' => $subdata3,'Runas Alias' => $subdata4,'Rules' => $subdata5));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/crontab
        static public function getSecurityCrontab() {
          $query = "SELECT C.Server, User, Minute, Hour, Day, Month, DayWeek, Command FROM Crontab as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, Num";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'User' => $val['User'],'Minute' => $val['Minute'],'Hour' => $val['Hour'],'Day' => $val['Day'],'Month' => $val['Month'],'DayWeek' => $val['DayWeek'],'Command' => $val['Command']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/iptables
        static public function getSecurityIPtables() {
          $query = "SELECT C.Server, IPTable, Chain, Policy FROM IPTablesPolicy as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null ORDER BY C.Server, IPTable, Chain";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT Rule FROM IPTables WHERE Auto and End is Null and Server = :idServer and IPTable = :idIPTable and Chain = :idChain Order by Num";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'],':idIPTable' => $val['IPTable'],':idChain' => $val['Chain']));
            array_push($result, array('Server' => $val['Server'],'IPTable' => $val['IPTable'],'Chain' => $val['Chain'],'Policy' => $val['Policy'],'Rules' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/wrappers
        static public function getSecurityWrappers() {
          $query = "SELECT C.Server, Type, Service FROM TCPWrappers as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null ORDER BY C.Server, Type, Service";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT Host FROM TCPWrappersHost WHERE Auto and End is Null and Server = :idServer and Type = :idType and Service = :idService Order by Host";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'],':idType' => $val['Type'],':idService' => $val['Service']));
            array_push($result, array('Server' => $val['Server'],'Type' => $val['Type'],'Service' => $val['Service'],'Hosts' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/pamaccess
        static public function getSecurityPAMaccess() {
          $query = "SELECT C.Server FROM PAMAccessRule as C, Server as S WHERE C.Server=S.Name and S.Node='1' and S.Auto and S.End is Null and C.Auto and C.End is Null GROUP BY C.Server ORDER BY C.Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery1 = "SELECT Module FROM PAMAccessModule WHERE Auto and End is Null and Server = :idServer Order by Module";
            $subdata1 = getDatabase()->all($subquery1, array(':idServer' => $val['Server']));
            $subquery2 = "SELECT Rule FROM PAMAccessRule WHERE Auto and End is Null and Server = :idServer Order by Num";
            $subdata2 = getDatabase()->all($subquery2, array(':idServer' => $val['Server']));
            array_push($result, array('Server' => $val['Server'],'Modules' => $subdata1,'Rules' => $subdata2));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/wdrivers
        static public function getSecurityWDrivers() {
          $query = "SELECT C.Server, C.Name, Caption, ErrorControl as 'Error Control', PathName as 'Path Name', ServiceType as 'Service Type', StartMode as 'Start Mode', State, TagId as 'Tag ID' FROM WinDriver as C, Server as S WHERE C.Server=S.Name and S.Node='2' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Caption' => $val['Caption'],'Error Control' => $val['Error Control'],'Path Name' => $val['Path Name'],'Service Type' => $val['Service Type'],'Start Mode' => $val['Start Mode'],'State' => $val['State'],'Tag ID' => $val['Tag ID']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/wservices
        static public function getSecurityWServices() {
          $query = "SELECT C.Server, C.Name, Caption, ErrorControl as 'Error Control', PathName as 'Path Name', ProcessId as 'Process ID', StartMode as 'Start Mode', State, TagId as 'Tag ID' FROM WinService as C, Server as S WHERE C.Server=S.Name and S.Node='2' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Caption' => $val['Caption'],'Error Control' => $val['Error Control'],'Path Name' => $val['Path Name'],'Process ID' => $val['Process ID'],'Start Mode' => $val['Start Mode'],'State' => $val['State'],'Tag ID' => $val['Tag ID']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/wshares
        static public function getSecurityWShares() {
          $query = "SELECT C.Server, C.Name, Caption, PathShare as 'Path Share', TypeShare as 'Type Share' FROM WinShare as C, Server as S WHERE C.Server=S.Name and S.Node='2' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Caption' => $val['Caption'],'Path Share' => $val['Path Share'],'Type Share' => $val['Type Share']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/wpackages
        static public function getSecurityWPackages() {
          $query = "SELECT C.Server, C.Name, Caption, Description, InstallDate as 'Install Date' , InstallLocation as 'Install Location', InstallState as 'Install State', Vendor, Version FROM WinPackage as C, Server as S WHERE C.Server=S.Name and S.Node='2' and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, C.Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Caption' => $val['Caption'],'Description' => $val['Description'],'Install Date' => $val['Install Date'], 'Install Location' => $val['Install Location'], 'Install State' => $val['Install State'], 'Vendor' => $val['Vendor'], 'Version' => $val['Version']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /security/openvas
        static public function getSecurityOpenvas() {
	  $query = "SELECT C.Server, C.IP, StartScan as 'Start Scan', CVSS, Severity, TotalHigh as 'Total High', TotalMedium as 'Total Medium', TotalLow as 'Total Low', TotalLog as 'Total Log', TotalFalsePositive as 'Total False Positive', ReportHTML as 'Report HTML', ReportPDF as 'Report PDF', ReportTXT as 'Report TXT', ReportXML as 'Report XML' FROM OpenvasHost as C, Server as S WHERE C.Server=S.Name and S.Auto and S.End is Null and C.Auto and C.End is Null Order by C.Server, StartScan desc";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'IP' => $val['IP'],'Start Scan' => $val['Start Scan'],'CVSS' => $val['CVSS'],'Total High' => $val['Total High'],'Total Medium' => $val['Total Medium'],'Total Low' => $val['Total Low'],'Total Log' => $val['Total Log'],'Total False Positive' => $val['Total False Positive'],'Report HTML' => $val['Report HTML'],'Report PDF' => $val['Report PDF'],'Report TXT' => $val['Report TXT'],'Report XML' => $val['Report XML']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

}

?>
