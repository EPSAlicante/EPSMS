<?php

class Rest_Software
{

	// GET /software
	static public function getSoftware() {
          header('Content-Type: text/html; charset=utf-8');
          readfile("paths/software/software.html");
	}

        // GET /software/IP
        static public function getSoftwareIP() {
          $query = "SELECT Name, IP FROM Server WHERE Auto and End is Null Order by Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Name' => $val['Name'],'IP' => $val['IP']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/distribution
        static public function getSoftwareDistribution() {
	  $query = "SELECT Server, MAX(if(SoftType='Distribution' and Name='Distribution',Value,'')) as 'Distribution', MAX(if(SoftType='Version' and Name='Version',Value,'')) as 'Version' FROM Software WHERE Auto and End is Null and ((SoftType='Distribution' and Name='Distribution') or (SoftType='Version' and Name='Version')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Distribution' => $val['Distribution'], 'Version' => $val['Version']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/kernel
        static public function getSoftwareKernel() {
          $query = "SELECT Server, Value as 'Kernel' FROM Software WHERE Auto and End is Null and SoftType='Kernel' and Name='Kernel' ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Kernel' => $val['Kernel']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/modules
        static public function getSoftwareModules() {
          $query = "SELECT Server, Name, FileName as 'File Name', Author, Description, License, Version, VerMagic as 'Version Magic', SrcVersion as 'Source Version' FROM Module WHERE Auto and End is Null Order by Server, Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'File Name' => $val['File Name'],'Author' => $val['Author'],'Description' => $val['Description'],'License' => $val['License'],'Version' => $val['Version'],'Version Magic' => $val['Version Magic'],'Source Version' => $val['Source Version']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/domain
        static public function getSoftwareDomain() {
          $query = "SELECT Server, Value as 'Domain' FROM Software WHERE Auto and End is Null and SoftType='Domain' and Name='Domain' ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Domain' => $val['Domain']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/resolver
        static public function getSoftwareResolver() {
          $query = "SELECT Server, Domain, Search, NS1 as 'NameServer 1', NS2 as 'NameServer 2', NS3 as 'NameServer 3' FROM Resolver WHERE Auto and End is Null ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT ROption as 'Option' FROM ResolverOption WHERE Auto and End is Null and Server = :idServer Order by ROption";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server']));
            array_push($result, array('Server' => $val['Server'],'Domain' => $val['Domain'],'Search' => $val['Search'],'Nameserver 1' => $val['NameServer 1'],'Nameserver 2' => $val['NameServer 2'],'Nameserver 3' => $val['NameServer 3'],'Options' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/filehost
        static public function getSoftwareFilehost() {
          $query = "SELECT Server, Rule FROM FileHost WHERE Auto and End is Null Order by Server, NumHost";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Rule' => $val['Rule']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/routes
        static public function getSoftwareRoutes() {
          $query = "SELECT Server, Destination, Mask, Gateway, Flags, Interface FROM Route WHERE Auto and End is Null Order by Server, Destination";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Destination' => $val['Destination'],'Gateway' => $val['Gateway'],'Mask' => $val['Mask'],'Flags' => $val['Flags'],'Interface' => $val['Interface']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/swap
        static public function getSoftwareSwap() {
          $query = "SELECT Server, Value as 'Swap' FROM Software WHERE Auto and End is Null and SoftType='Swap' and Name='Swap' ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Swap' => $val['Swap']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/virtualization
        static public function getSoftwareVirtualization() {
          $query = "SELECT Server, MAX(if(SoftType='Virtualization' and Name='Virtualization Role',Value,'')) as 'Virtualization Role', MAX(if(SoftType='Virtualization' and Name='Virtualization Type',Value,'')) as 'Virtualization Type' FROM Software WHERE Auto and End is Null and ((SoftType='Virtualization' and Name='Virtualization Role') or (SoftType='Virtualization' and Name='Virtualization Type')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Virtualization Role' => $val['Virtualization Role'], 'Virtualization Type' => $val['Virtualization Type']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/filesystems
        static public function getSoftwareFilesystems() {
          $query = "SELECT Server, Name, Type, Mount, Options, Size  FROM FileSystem WHERE Auto and End is Null Order by Server, Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Type' => $val['Type'],'Mount' => $val['Mount'],'Options' => $val['Options'],'Size' => $val['Size']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/wlogicaldevices
        static public function getSoftwareWLogicalDevices() {
          $query = "SELECT Server, DeviceID as 'Device ID', Caption, DriveType as 'Drive Type', FileSystem as 'File System', Size, Access, Availability, Compressed, ConfigManagerErrorCode as 'Config Manager Error Code', SupportsDiskQuotas as 'Supports Disk Quotas', QuotasDisabled as 'Quotas Disabled', SupportsFileBasedCompression as 'Supports File Based Compression', VolumeName as 'Volume Name', VolumeSerialNumber as 'Volume Serial Number' FROM  WinLogicalDisk WHERE Auto and End is Null Order by Server, DeviceID";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT PartitionDeviceID as 'Partition Device ID' FROM WinLogicalDiskPartition WHERE Auto and End is Null and Server = :idServer and LogicalDiskDeviceID = :idLogicalDisk Order by PartitionDeviceID";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'],':idLogicalDisk' => $val['Device ID']));
            array_push($result, array('Server' => $val['Server'],'Device ID' => $val['Device ID'],'Caption' => $val['Caption'],'Drive Type' => $val['Drive Type'],'File System' => $val['File System'],'Size' => $val['Size'],'Access' => $val['Access'],'Availability' => $val['Availability'],'Compressed' => $val['Compressed'],'Config Manager Error Code' => $val['Config Manager Error Code'],'Supports Disk Quotas' => $val['Supports Disk Quotas'],'Quotas Disabled' => $val['Quotas Disabled'],'Supports File Based Compression' => $val['Supports File Based Compression'],'Volume Name' => $val['Volume Name'],'Volume Serial Number' => $val['Volume Serial Number'],'Partitions' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/packagemanager
        static public function getSoftwarePackagemanager() {
          $query = "SELECT Server, Value as 'Package Manager' FROM Software WHERE Auto and End is Null and SoftType='Package Manager' and Name='Package Manager' ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Package Manager' => $val['Package Manager']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/woperatingsystem
        static public function getSoftwareWOperatingSystem() {
          $query = "SELECT Server, MAX(if(SoftType='OS' and Name='OSName',Value,'')) as 'OS Name', MAX(if(SoftType='OS' and Name='OSDescription',Value,'')) as 'OS Description', MAX(if(SoftType='BootSystem' and Name='BootDevice',Value,'')) as 'Boot Device', MAX(if(SoftType='OS' and Name='ServicePackMajorMinorVersion',Value,'')) as 'Service Pack Version', MAX(if(SoftType='Architecture' and Name='OSArchitecture',Value,'')) as 'OS Architecture', MAX(if(SoftType='OS' and Name='OSType',Value,'')) as 'OS Type', MAX(if(SoftType='OS' and Name='ProductType',Value,'')) as 'Product Type', MAX(if(SoftType='OS' and Name='Version',Value,'')) as 'Version', MAX(if(SoftType='OS' and Name='SerialNumber',Value,'')) as 'Serial Number', MAX(if(SoftType='OS' and Name='Country',Value,'')) as 'Country', MAX(if(SoftType='OS' and Name='Language',Value,'')) as 'Language', MAX(if(SoftType='OS' and Name='PAEEnabled',Value,'')) as 'PAE Enabled', MAX(if(SoftType='OS' and Name='Manufacturer',Value,'')) as 'Manufacturer', MAX(if(SoftType='TimeZone' and Name='CurrentTimeZone',Value,'')) as 'Current Time Zone', MAX(if(SoftType='OS' and Name='EncryptionLevel',Value,'')) as 'Encryption Level', MAX(if(SoftType='OS' and Name='NumberOfLicensedUsers',Value,'')) as 'Number Of Licensed Users', MAX(if(SoftType='OS' and Name='OperatingSystemSKU',Value,'')) as 'Operating System SKU', MAX(if(SoftType='OS' and Name='Organization',Value,'')) as 'Organization', MAX(if(SoftType='OS' and Name='RegisteredUser',Value,'')) as 'Registered User', MAX(if(SoftType='Processes' and Name='MaxNumberOfProcesses',Value,'')) as 'Max Number Of Processes', MAX(if(SoftType='OS' and Name='SystemDevice',Value,'')) as 'System Device', MAX(if(SoftType='OS' and Name='SystemDrive',Value,'')) as 'System Drive', MAX(if(SoftType='OS' and Name='WindowsDirectory',Value,'')) as 'Windows Directory', MAX(if(SoftType='OS' and Name='SystemDirectory',Value,'')) as 'System Directory', MAX(if(SoftType='Memory' and Name='TotalVisibleMemorySize',Value,'')) as 'Total Visible Memory Size', MAX(if(SoftType='Memory' and Name='TotalSwapSpaceSize',Value,'')) as 'Total Swap Space Size', MAX(if(SoftType='Memory' and Name='TotalVirtualMemorySize',Value,'')) as 'Total Virtual Memory Size', MAX(if(SoftType='OS' and Name='Distributed',Value,'')) as 'Distributed' FROM Software WHERE Auto and End is Null and ((SoftType='OS' and Name='OSName') or (SoftType='OS' and Name='OSDescription') or (SoftType='BootSystem' and Name='BootDevice') or (SoftType='OS' and Name='ServicePackMajorMinorVersion') or (SoftType='Architecture' and Name='OSArchitecture') or (SoftType='OS' and Name='OSType') or (SoftType='OS' and Name='ProductType') or (SoftType='OS' and Name='Version') or (SoftType='OS' and Name='SerialNumber') or (SoftType='OS' and Name='Country') or (SoftType='OS' and Name='Language') or (SoftType='OS' and Name='PAEEnabled') or (SoftType='OS' and Name='Manufacturer') or (SoftType='TimeZone' and Name='CurrentTimeZone') or (SoftType='OS' and Name='EncryptionLevel') or (SoftType='OS' and Name='NumberOfLicensedUsers') or (SoftType='OS' and Name='OperatingSystemSKU') or (SoftType='OS' and Name='Organization') or (SoftType='OS' and Name='RegisteredUser') or (SoftType='Processes' and Name='MaxNumberOfProcesses') or (SoftType='OS' and Name='SystemDevice') or (SoftType='OS' and Name='SystemDrive') or (SoftType='OS' and Name='WindowsDirectory') or (SoftType='OS' and Name='SystemDirectory') or (SoftType='Memory' and Name='TotalVisibleMemorySize') or (SoftType='Memory' and Name='TotalSwapSpaceSize') or (SoftType='Memory' and Name='TotalVirtualMemorySize') or (SoftType='OS' and Name='Distributed')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'OS Name' => $val['OS Name'], 'OS Description' => $val['OS Description'], 'Boot Device' => $val['Boot Device'], 'Service Pack Version' => $val['Service Pack Version'], 'OS Architecture' => $val['OS Architecture'], 'OS Type' => $val['OS Type'], 'Product Type' => $val['Product Type'], 'Version' => $val['Version'], 'Serial Number' => $val['Serial Number'], 'Country' => $val['Country'], 'Language' => $val['Language'], 'PAE Enabled' => $val['PAE Enabled'], 'Manufacturer' => $val['Manufacturer'], 'Current Time Zone' => $val['Current Time Zone'], 'Encryption Level' => $val['Encryption Level'], 'Number Of Licensed Users' => $val['Number Of Licensed Users'], 'Operating System SKU' => $val['Operating System SKU'], 'Organization' => $val['Organization'], 'Registered User' => $val['Registered User'], 'Max Number Of Processes' => $val['Max Number Of Processes'], 'System Device' => $val['System Device'], 'System Drive' => $val['System Drive'], 'Windows Directory' => $val['Windows Directory'], 'System Directory' => $val['System Directory'], 'Total Visible Memory Size' => $val['Total Visible Memory Size'], 'Total Swap Space Size' => $val['Total Swap Space Size'], 'Total Virtual Memory Size' => $val['Total Virtual Memory Size'], 'Distributed' => $val['Distributed']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /software/wdomain
        static public function getSoftwareWDomain() {
          $query = "SELECT Server, MAX(if(SoftType='WinDomain' and Name='Domain',Value,'')) as 'Domain', MAX(if(SoftType='WinDomain' and Name='DomainRole',Value,'')) as 'Domain Role', MAX(if(SoftType='WinDomain' and Name='PartOfDomain',Value,'')) as 'Part Of Domain' FROM Software WHERE Auto and End is Null and ((SoftType='WinDomain' and Name='Domain') or (SoftType='WinDomain' and Name='DomainRole') or (SoftType='WinDomain' and Name='PartOfDomain')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Domain' => $val['Domain'], 'Domain Role' => $val['Domain Role'], 'Part Of Domain' => $val['Part Of Domain']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

}

?>
