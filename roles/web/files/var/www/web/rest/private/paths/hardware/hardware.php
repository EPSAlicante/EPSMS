<?php

class Rest_Hardware
{

	// GET /hardware
	static public function getHardware() {
          header('Content-Type: text/html; charset=utf-8');
          readfile("paths/hardware/hardware.html");
	}
	
        // GET /hardware/system
        static public function getHardwareSystem() {
	  $query = "SELECT H.Server, MAX(if(HardType='Architecture' and H.Name='Architecture',Value,'')) as 'Architecture', MAX(if(HardType='System' and H.Name='Manufacturer',Value,'')) as 'Manufacturer', MAX(if(HardType='System' and H.Name='Product Name',Value,'')) as 'Product Name', MAX(if(HardType='System' and H.Name='Version',Value,'')) as 'Version', MAX(if(HardType='System' and H.Name='Serial Number',Value,'')) as 'Serial Number', MAX(if(HardType='System' and H.Name='UUID',Value,'')) as 'UUID', MAX(if(HardType='System' and H.Name='Wake-Up Type',Value,'')) as 'Wake-Up Type' FROM Hardware as H, Server as S WHERE H.Server=S.Name and S.Node='1' and H.Auto and H.End is Null and ((HardType='Architecture' and H.Name='Architecture') or (HardType='System' and H.Name='Manufacturer') or (HardType='System' and H.Name='Product Name') or (HardType='System' and H.Name='Version') or (HardType='System' and H.Name='Serial Number') or (HardType='System' and H.Name='UUID') or (HardType='System' and H.Name='Wake-Up Type')) GROUP BY 1 ORDER BY H.Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Architecture' => $val['Architecture'], 'Manufacturer' => $val['Manufacturer'], 'Product Name' => $val['Product Name'], 'Version' => $val['Version'], 'Serial Number' => $val['Serial Number'], 'UUID' => $val['UUID'], 'Wake-Up Type' => $val['Wake-Up Type']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wsystem
        static public function getHardwareWSystem() {
          $query = "SELECT H.Server, MAX(if(HardType='System' and H.Name='Description',Value,'')) as 'Description', MAX(if(HardType='System' and H.Name='SystemType',Value,'')) as 'System Type', MAX(if(HardType='System' and H.Name='PCSystemType',Value,'')) as 'PC System Type', MAX(if(HardType='System' and H.Name='Manufacturer',Value,'')) as 'Manufacturer', MAX(if(HardType='System' and H.Name='Model',Value,'')) as 'Model', MAX(if(HardType='System' and H.Name='InfraredSupported',Value,'')) as 'Infrared Supported', MAX(if(HardType='System' and H.Name='WakeUp Type',Value,'')) as 'Wake-Up Type' FROM Hardware as H, Server as S WHERE H.Server=S.Name and S.Node='2' and H.Auto and H.End is Null and ((HardType='System' and H.Name='Description') or (HardType='System' and H.Name='SystemType') or (HardType='System' and H.Name='PCSystemType') or (HardType='System' and H.Name='Manufacturer') or (HardType='System' and H.Name='Model') or (HardType='System' and H.Name='InfraredSupported') or (HardType='System' and H.Name='WakeUpType')) GROUP BY 1 ORDER BY H.Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Description' => $val['Description'], 'System Type' => $val['System Type'], 'PC System Type' => $val['PC System Type'], 'Manufacturer' => $val['Manufacturer'], 'Model' => $val['Model'], 'Infrared Supported' => $val['Infrared Supported'], 'Wake-Up Type' => $val['Wake-Up Type']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/processor
        static public function getHardwareProcessor() {
          $query = "SELECT Server, MAX(if(HardType='Processor' and Name='Processor Type',Value,'')) as 'Processor Type', MAX(if(HardType='Processor' and Name='Processor count',Value,'')) as 'Processor count', MAX(if(HardType='Processor' and Name='Processor cores',Value,'')) as 'Processor cores', MAX(if(HardType='Processor' and Name='Core threads',Value,'')) as 'Core threads', MAX(if(HardType='Processor' and Name='Total virtual CPUs',Value,'')) as 'Total virtual CPUs' FROM Hardware WHERE Auto and End is Null and ((HardType='Processor' and Name='Processor Type') or (HardType='Processor' and Name='Processor count') or (HardType='Processor' and Name='Processor cores') or (HardType='Processor' and Name='Core threads') or (HardType='Processor' and Name='Total virtual CPUs')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery1 = "SELECT Socket, Type, Family, Vendor, Signature, ID, Version, Voltage, ExternalClock, MaxSpeed, CurrentSpeed, Status, Upgrade, L1Cache, L2Cache, L3Cache, SerialNumber FROM Processor WHERE Auto and End is Null and Server = :idServer Order by Socket";
            $subdata1 = getDatabase()->all($subquery1, array(':idServer' => $val['Server']));
            foreach ($subdata1 as $subval) {
              $subquery2 = "SELECT Flag, Value FROM ProcessorFlag WHERE Auto and End is Null and Server = :idServer and Socket = :idSocket Order by Flag";
              $subdata2 = getDatabase()->all($subquery2, array(':idServer' => $val['Server'], ':idSocket' => $subval['Socket']));
              array_push($result, array('Server' => $val['Server'],'Processor Type' => $val['Processor Type'],'Processor Count' => $val['Processor count'],'Processor Cores' => $val['Processor cores'],'Core Threads' => $val['Core threads'],'Total virtual CPUs' => $val['Total virtual CPUs'],'Sockets' => array(array('Socket' => $subval['Socket'],'Type' => $subval['Type'],'Family' => $subval['Family'],'Vendor' => $subval['Vendor'],'Signature' => $subval['Signature'],'ID' => $subval['ID'],'Version' => $subval['Version'],'Voltage' => $subval['Voltage'],'External Clock' => $subval['ExternalClock'],'Maximum Speed' => $subval['MaxSpeed'],'Current Speed' => $subval['CurrentSpeed'],'Status' => $subval['Status'],'Upgrade' => $subval['Upgrade'],'L1 Cache' => $subval['L1Cache'],'L2 Cache' => $subval['L2Cache'],'L3 Cache' => $subval['L3Cache'],'Serial Number' => $subval['SerialNumber'],'Flags' => $subdata2))));
            }
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wprocessor
        static public function getHardwareWProcessor() {
          $query = "SELECT Server, MAX(if(HardType='Processor' and Name='NumberOfProcessors',Value,'')) as 'Number Of Processors', MAX(if(HardType='Processor' and Name='NumberOfLogicalProcessors',Value,'')) as 'Number Of Logical Processors' FROM Hardware WHERE Auto and End is Null and ((HardType='Processor' and Name='NumberOfProcessors') or (HardType='Processor' and Name='NumberOfLogicalProcessors')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery1 = "SELECT DeviceID, Name, Caption, ConfigManagerErrorCode, CPUStatus, CurrentClockSpeed, DataWidth, Family, L2CacheSize, L2CacheSpeed, L3CacheSize, L3CacheSpeed, Manufacturer, MaxClockSpeed, NumberOfCores, NumberOfLogicalProcessors, ProcessorID, ProcessorType FROM WinProcessor WHERE Auto and End is Null and Server = :idServer Order by DeviceID";
            $subdata1 = getDatabase()->all($subquery1, array(':idServer' => $val['Server']));
            foreach ($subdata1 as $subval) {
              array_push($result, array('Server' => $val['Server'],'Number Of Processors' => $val['Number Of Processors'],'Number Of Logical Processors' => $val['Number Of Logical Processors'],'Sockets' => array(array('Device ID' => $subval['DeviceID'],'Name' => $subval['Name'],'Caption' => $subval['Caption'],'Config Manager Error Code' => $subval['ConfigManagerErrorCode'],'CPU Status' => $subval['CPUStatus'],'Current Clock Speed' => $subval['CurrentClockSpeed'],'Data Width' => $subval['DataWidth'],'Family' => $subval['Family'],'L2 Cache Size' => $subval['L2CacheSize'],'L2 Cache Speed' => $subval['L2CacheSpeed'],'L3 Cache Size' => $subval['L3CacheSize'],'L3 Cache Speed' => $subval['L3CacheSpeed'],'Manufacturer' => $subval['Manufacturer'],'Max Clock Speed' => $subval['MaxClockSpeed'],'Number Of Cores' => $subval['NumberOfCores'],'Number Of Logical Processors' => $subval['NumberOfLogicalProcessors'],'Processor ID' => $subval['ProcessorID'],'Processor Type' => $subval['ProcessorType']))));
            }
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/memory
        static public function getHardwareMemory() {
          $query = "SELECT Server, MAX(if(HardType='Memory' and Name='Memory',Value,'')) as 'Memory', MAX(if(HardType='Memory' and Name='Maximum Memory Module Size',Value,'')) as 'Maximum Memory Module Size', MAX(if(HardType='Memory' and Name='Associated Memory Slots',Value,'')) as 'Associated Memory Slots' FROM Hardware WHERE Auto and End is Null and ((HardType='Memory' and Name='Memory') or (HardType='Memory' and Name='Maximum Memory Module Size') or (HardType='Memory' and Name='Associated Memory Slots')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery1 = "SELECT Handle, Location, MemoryUse, ErrorCorrectionType, MaxCapacity, NumberDevices FROM MemoryArray WHERE Auto and End is Null and Server = :idServer Order by Handle";
            $subdata1 = getDatabase()->all($subquery1, array(':idServer' => $val['Server']));
	    foreach ($subdata1 as $subval) {
              $subquery2 = "SELECT Handle, Locator, BankLocator as 'Bank Locator', Size, Speed, Type FROM Memory WHERE Auto and End is Null and Server = :idServer and Array = :idArray Order by Handle";
              $subdata2 = getDatabase()->all($subquery2, array(':idServer' => $val['Server'], ':idArray' => $subval['Handle']));
              array_push($result, array('Server' => $val['Server'],'Total Memory' => $val['Memory'],'Maximum Memory Module Size' => $val['Maximum Memory Module Size'],'Associated Memory Slots' => $val['Associated Memory Slots'],'Arrays' => array(array('Handle' => $subval['Handle'],'Location' => $subval['Location'],'Use' => $subval['MemoryUse'],'Error Correction Type' => $subval['ErrorCorrectionType'],'Maximum Capacity' => $subval['MaxCapacity'],'Number Of Devices' => $subval['NumberDevices'],'Slots' => $subdata2))));
	    }
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wmemory
        static public function getHardwareWMemory() {
          $query = "SELECT Server, MAX(if(HardType='Memory' and Name='TotalPhysicalMemory',Value,'')) as 'Total Physical Memory' FROM Hardware WHERE Auto and End is Null and (HardType='Memory' and Name='TotalPhysicalMemory') GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery1 = "SELECT Tag, Caption, HotSwappable as 'Hot Swappable', Location, MaxCapacity as 'Max Capacity', MemoryDevices as 'Memory Of Devices', MemoryErrorCorrection as 'Memory Error Correction', MemoryUse as 'Memory Use' FROM WinMemoryArray WHERE Auto and End is Null and Server = :idServer Order by Tag";
            $subdata1 = getDatabase()->all($subquery1, array(':idServer' => $val['Server']));
            foreach ($subdata1 as $subval) {
              $subquery2 = "SELECT Tag, Caption, Capacity, DataWidth as 'Data Width', TotalWidth as 'Total Width', DeviceLocator as 'Device Locator', FormFactor as 'Form Factor', HotSwappable as 'Hot Swappable', Manufacturer, MemoryType as 'Memory Type', PositionInRow as 'Position In Row', Speed FROM WinMemory as M, WinMemoryLocation as L WHERE M.Server = L.Server and M.Tag = L.PartTag and M.Auto and M.End is Null and M.Server = :idServer and L.GroupTag = :idArray Order by Tag";
              $subdata2 = getDatabase()->all($subquery2, array(':idServer' => $val['Server'], ':idArray' => $subval['Tag']));
              array_push($result, array('Server' => $val['Server'],'Total Physical Memory' => $val['Total Physical Memory'],'Arrays' => array(array('Tag' => $subval['Tag'],'Caption' => $subval['Caption'],'Hot Swappable' => $subval['Hot Swappable'],'Location' => $subval['Location'],'Max Capacity' => $subval['Max Capacity'],'Memory Of Devices' => $subval['Memory Of Devices'],'Memory Error Correction' => $subval['Memory Error Correction'],'Memory Use' => $subval['Memory Use'],'Slots' => $subdata2))));
            }
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/bios
        static public function getHardwareBios() {
	  $query = "SELECT Server, MAX(if(HardType='bios' and Name='Vendor',Value,'')) as 'Vendor', MAX(if(HardType='bios' and Name='Release Date',Value,'')) as 'Release Date', MAX(if(HardType='bios' and Name='Version',Value,'')) as 'Version',  MAX(if(HardType='bios' and Name='ROM Size',Value,'')) as 'ROM Size', MAX(if(HardType='bios' and Name='Runtime Size',Value,'')) as 'Runtime Size' FROM Hardware WHERE Auto and End is Null and ((HardType='bios' and Name='Vendor') or (HardType='bios' and Name='Release Date') or (HardType='bios' and Name='Version') or (HardType='bios' and Name='ROM Size') or (HardType='bios' and Name='Runtime Size')) GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT Characteristic, Value FROM Bios WHERE Auto and End is Null and Server = :idServer Order by Characteristic";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server']));
            array_push($result, array('Server' => $val['Server'],'Vendor' => $val['Vendor'],'Release Date' => $val['Release Date'],'Version' => $val['Version'],'ROM Size' => $val['ROM Size'],'Runtime Size' => $val['Runtime Size'],'Characteristics' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wbios
        static public function getHardwareWBios() {
          $query = "SELECT Server, Name, Caption, SoftwareElementID as 'Software Element ID', SoftwareElementState as 'Software Element State', TargetOperatingSystem as 'Target Operating System', Version as 'Version', BuildNumber as 'Build Number', CodeSet as 'Code Set', CurrentLanguage as 'Current Language', IdentificationCode as 'Identification Code', LanguageEdition as 'Language Edition', Manufacturer, PrimaryBIOS as 'Primary BIOS', ReleaseDate as 'Release Date', SerialNumber as 'Serial Number', Status FROM WinBios WHERE Auto and End is Null GROUP BY 1 ORDER BY Server";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT CharCode as 'Char Code', Description FROM WinBiosChar WHERE Auto and End is Null and Server = :idServer and Name = :idName Order by CharCode";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'], ':idName' => $val['Name']));
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Caption' => $val['Caption'],'Software Element ID' => $val['Software Element ID'],'Software Element State' => $val['Software Element State'],'Target Operating System' => $val['Target Operating System'],'Version' => $val['Version'],'Build Number' => $val['Build Number'],'Code Set' => $val['Code Set'],'Current Language' => $val['Current Language'],'Identification Code' => $val['Identification Code'],'Language Edition' => $val['Language Edition'],'Manufacturer' => $val['Manufacturer'],'Primary BIOS' => $val['Primary BIOS'],'Characteristics' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/baseboard
        static public function getHardwareBaseboard() {
          $query = "SELECT Server, Handle, Manufacturer, ProductName as 'Product Name', Version, SerialNumber as 'Serial Number' FROM Baseboard WHERE Auto and End is Null ORDER BY Server, Handle";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT Handle, Type, Description, Enabled FROM BaseboardDevice WHERE Auto and End is Null and Server = :idServer Order by Handle";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server']));
            array_push($result, array('Server' => $val['Server'],'Handle' => $val['Handle'],'Manufacturer' => $val['Manufacturer'],'Product Name' => $val['Product Name'],'Version' => $val['Version'],'Serial Number' => $val['Serial Number'],'Devices' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wbaseboard
        static public function getHardwareWBaseboard() {
          $query = "SELECT Server, Tag, Caption, Manufacturer, Product, Model, Version, SerialNumber as 'Serial Number', HostingBoard as 'Hosting Board', HotSwappable as 'Hot Swappable', PoweredOn as 'Powered On' FROM WinBaseBoard WHERE Auto and End is Null ORDER BY Server, Tag";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT Tag, Caption, Description, DeviceType as 'Device Type', Manufacturer, Model, Version, SerialNumber as 'Serial Number', Enabled, HotSwappable as 'Hot Swappable', PoweredOn as 'Powered On' FROM WinOnBoardDevice WHERE Auto and End is Null and Server = :idServer Order by Tag";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server']));
            array_push($result, array('Server' => $val['Server'],'Tag' => $val['Tag'],'Caption' => $val['Caption'],'Manufacturer' => $val['Manufacturer'],'Product' => $val['Product'],'Model' => $val['Model'],'Version' => $val['Version'],'Serial Number' => $val['Serial Number'],'Hosting Board' => $val['Hosting Board'],'Hot Swappable' => $val['Hot Swappable'],'Powered On' => $val['Powered On'],'Devices' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/chassis
        static public function getHardwareChassis() {
          $query = "SELECT Server, MAX(if(HardType='chassis' and Name='Manufacturer',Value,'')) as 'Manufacturer', MAX(if(HardType='chassis' and Name='Type',Value,'')) as 'Type', MAX(if(HardType='chassis' and Name='Version',Value,'')) as 'Version',  MAX(if(HardType='chassis' and Name='Serial Number',Value,'')) as 'Serial Number' FROM Hardware WHERE Auto and End is Null and ((HardType='chassis' and Name='Manufacturer') or (HardType='chassis' and Name='Type') or (HardType='chassis' and Name='Version') or (HardType='chassis' and Name='Serial Number')) GROUP BY 1 ORDER BY Server";
	  $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Manufacturer' => $val['Manufacturer'], 'Type' => $val['Type'], 'Version' => $val['Version'], 'Serial Number' => $val['Serial Number']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/devices
        static public function getHardwareDevices() {
	  $query = "SELECT Server, Name, Model, Scheduler, Size, Vendor FROM Device WHERE Auto and End is Null ORDER BY Server, Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
	    $subquery = "SELECT Name, Size FROM Partition WHERE Auto and End is Null and Server = :idServer and Device = :idDevice Order by Name";
	    $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'], 'idDevice' => $val['Name']));
            array_push($result, array('Server' => $val['Server'],'Name' => $val['Name'],'Model' => $val['Model'],'Scheduler' => $val['Scheduler'],'Size' => $val['Size'],'Vendor' => $val['Vendor'],'Partitions' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wdevices
        static public function getHardwareWDevices() {
          $query = "SELECT Server, DeviceID as 'Device ID', Caption, DiskIndex as 'Disk Index', InterfaceType as 'Interface Type', Model, Size, Availability, TotalHeads as 'Total Heads', TotalCylinders as 'Total Cylinders', TracksPerCylinder as 'Tracks Per Cylinder', TotalTracks as 'Total Tracks', SectorsPerTrack as 'Sectors Per Track', TotalSectors as 'Total Sectors', BytesPerSector as 'Bytes Per Sector', DefaultBlockSize as 'Default Block Size', MediaType as 'Media Type', Partitions as 'Partition ID', ConfigManagerErrorCode as 'Config Manager Error Code', SerialNumber as 'Serial Number', SCSIBus as 'SCSI Bus', SCSIPort as 'SCSI Port', SCSITargetID as 'SCSI Target ID', SCSILogicalUnit as 'SCSI Logical Unit' FROM WinDiskDrive WHERE Auto and End is Null ORDER BY Server, DeviceID";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT DeviceID as 'Device ID', Caption, DiskIndex as 'Disk Index', PartitionIndex as 'Partition Index', PartitionType as 'Partition Type', Size, BlockSize as 'Block Size', NumberOfBlocks as 'Number Of Blocks', Access, Availability, Bootable, BootPartition as 'Boot Partition', PrimaryPartition as 'Primary Partition' FROM WinDiskPartition as P, WinDiskDrivePartition D WHERE P.Server = D.Server and P.DeviceID = D.PartitionDeviceID and P.Auto and P.End is Null and P.Server = :idServer and D.DiskDeviceID = :idDevice Order by DeviceID";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'], 'idDevice' => $val['Device ID']));
            array_push($result, array('Server' => $val['Server'],'Device ID' => $val['Device ID'],'Caption' => $val['Caption'],'Disk Index' => $val['Disk Index'],'Interface Type' => $val['Interface Type'],'Model' => $val['Model'],'Size' => $val['Size'],'Availability' => $val['Availability'],'Total Heads' => $val['Total Heads'],'Total Cylinders' => $val['Total Cylinders'],'Tracks Per Cylinder' => $val['Tracks Per Cylinder'],'Total Tracks' => $val['Total Tracks'],'Sectors Per Track' => $val['Sectors Per Track'],'Total Sectors' => $val['Total Sectors'],'Bytes Per Sector' => $val['Bytes Per Sector'],'Default Block Size' => $val['Default Block Size'],'Media Type' => $val['Media Type'],'Partition ID' => $val['Partition ID'],'Config Manager Error Code' => $val['Config Manager Error Code'],'Serial Number' => $val['Serial Number'],'SCSI Bus' => $val['SCSI Bus'],'SCSI Port' => $val['SCSI Port'],'SCSI Target ID' => $val['SCSI Target ID'],'SCSI Logical Unit' => $val['SCSI Logical Unit'],'Partitions' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/interfaces
        static public function getHardwareInterfaces() {
          $query = "SELECT Server, Name, Address, NameDNS as 'Name DNS', Network, Netmask, MAC, Type, Module, Active FROM Interface WHERE Auto and End is null Order by Server, Name";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Name' => $val['Name'],'Address' => $val['Address'],'Name DNS' => $val['Name DNS'],'Network' => $val['Network'],'Netmask' => $val['Netmask'],'MAC' => $val['MAC'],'Type' => $val['Type'],'Module' => $val['Module'],'Active' => $val['Active']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }
	
        // GET /hardware/winterfaces
        static public function getHardwareWInterfaces() {
          $query = "SELECT Server, DeviceID as 'Device ID', Name, AdapterType as 'Adapter Type', Manufacturer, MACAddress as 'MAC Address', Availability, ConfigManagerErrorCode as 'Config Manager Error Code', AdapterIndex as 'Adapter Index', NetConnectionID as 'Net Connection ID', NetConnectionStatus as 'Net Connection Status', ServiceName as 'Service Name' FROM WinNetworkAdapter WHERE Auto and End is null Order by Server, DeviceID";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            $subquery = "SELECT C.NetIndex as 'Net Index', Description, IPAddress as 'IP Address', IPSubnet as 'IP Subnet', DefaultIPGateway as 'Default IP Gateway', DefaultTOS as 'Default TOS', DefaultTTL as 'Default TTL', DHCPEnabled as 'DHCP Enabled', DHCPServer as 'DHCP Server', DNSDomain as 'DNS Domain', DNSDomainSuffixSearchOrder as 'DNS Domain Suffix Search Order', DNSEnabledForWINSResolution as 'DNS Enabled For WINS Resolution', DNSDomainSearchOrder as 'DNS Domain Search Order', IGMPLevel as 'IGMP Level', MACAddress as 'MAC Address', WINSEnableLMHostsLookup as 'WINS Enable LMHosts Lookup', WINSPrimaryServer as 'WINS Primary Server', WINSSecondaryServer as 'WINS Secondary Server' FROM WinNetworkAdapterConfig as C, WinNetworkAdapterSetting S WHERE C.Server = S.Server and C.NetIndex = S.NetIndex and C.Auto and C.End is Null and C.Server = :idServer and S.DeviceID = :idDevice Order by C.NetIndex";
            $subdata = getDatabase()->all($subquery, array(':idServer' => $val['Server'], 'idDevice' => $val['Device ID']));
            array_push($result, array('Server' => $val['Server'],'Device ID' => $val['Device ID'],'Name' => $val['Name'],'Adapter Type' => $val['Adapter Type'],'Manufacturer' => $val['Manufacturer'],'MAC Address' => $val['MAC Address'],'Availability' => $val['Availability'],'Config Manager Error Code' => $val['Config Manager Error Code'],'Adapter Index' => $val['Adapter Index'],'Net Connection ID' => $val['Net Connection ID'],'Net Connection Status' => $val['Net Connection Status'],'Service Name' => $val['Service Name'],'Settings' => $subdata));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/cache
        static public function getHardwareCache() {
          $query = "SELECT Server, Designation as 'Socket Designation', Handle, Level, Enabled, Mode, Location, InstSize as 'Installed Size', MaxSize as 'Maximum Size' FROM Cache WHERE Auto and End is null Order by Server, Designation";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Socket Designation' => $val['Socket Designation'],'Handle' => $val['Handle'],'Level' => $val['Level'],'Enabled' => $val['Enabled'],'Operational Mode' => $val['Mode'],'Location' => $val['Location'],'Installed Size' => $val['Installed Size'],'Maximum Size' => $val['Maximum Size']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/connectors
        static public function getHardwareConnectors() {
          $query = "SELECT Server, IntDesignator as 'Internal Reference Designator', Handle, IntType as 'Internal Connector Type', ExtDesignator as 'External Reference Designator', ExtType as 'External Connector Type', PortType as 'Port Type' FROM Connector WHERE Auto and End is Null Order by Server, IntDesignator";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Internal Reference Designator' => $val['Internal Reference Designator'],'Handle' => $val['Handle'],'Internal Connector Type' => $val['Internal Connector Type'],'External Reference Designator' => $val['External Reference Designator'],'External Connector Type' => $val['External Connector Type'],'Port Type' => $val['Port Type']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wconnectors
        static public function getHardwareWConnectors() {
          $query = "SELECT Server, Tag, ConnectorType as 'Connector Type', ExternalReferenceDesignator as 'External Reference Designator', InternalReferenceDesignator as 'Internal Reference Designator', PortType as 'Port Type' FROM WinPortConnector WHERE Auto and End is Null Order by Server, Tag";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Tag' => $val['Tag'],'Connector Type' => $val['Connector Type'],'External Reference Designator' => $val['External Reference Designator'],'Internal Reference Designator' => $val['Internal Reference Designator'],'Port Type' => $val['Port Type']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/slots
        static public function getHardwareSlots() {
          $query = "SELECT Server, Designation, Handle, SlotType as 'Slot Type', SlotBusWidth as 'Slot Bus Width', CurrentUsage as 'Current Usage', SlotLength as 'Slot Length', SlotId as 'Slot ID' FROM Slot WHERE Auto and End is Null Order by Server, Designation";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Designation' => $val['Designation'],'Handle' => $val['Handle'],'Slot Type' => $val['Slot Type'],'Slot Bus Width' => $val['Slot Bus Width'],'Current Usage' => $val['Current Usage'],'Slot Length' => $val['Slot Length'],'Slot ID' => $val['Slot ID']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

        // GET /hardware/wbuses
        static public function getHardwareWBuses() {
          $query = "SELECT Server, DeviceID as 'Device ID', Caption, BusType as 'Bus Type', BusNum as 'Bus Num', Availability, ConfigManagerErrorCode as 'Config Manager Error Code' FROM WinBus WHERE Auto and End is Null Order by Server, DeviceID";
          $data = getDatabase()->all($query);
          $result = array();
          foreach ($data as $val) {
            array_push($result, array('Server' => $val['Server'], 'Device ID' => $val['Device ID'],'Caption' => $val['Caption'],'Bus Type' => $val['Bus Type'],'Bus Num' => $val['Bus Num'],'Availability' => $val['Availability'],'Config Manager Error Code' => $val['Config Manager Error Code']));
          }

          $json_string = json_encode($result);
          //header("Content-Type: application/json");
          echo $json_string;
        }

}

?>
