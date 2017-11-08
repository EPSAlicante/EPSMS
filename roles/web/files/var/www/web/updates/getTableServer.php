<?php
require_once("conn.php");

$q=$_GET["q"];
$s=$_GET["s"];

if ($q=="1Day") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 1 DAY )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 1 DAY )";
} elseif ($q=="2Days") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 2 DAY )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 2 DAY )";
} elseif ($q=="3Days") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 3 DAY )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 3 DAY )";
} elseif ($q=="4Days") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 4 DAY )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 4 DAY )";
} elseif ($q=="1Week") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 1 WEEK )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 1 WEEK )";
} elseif ($q=="2Weeks") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 2 WEEK )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 2 WEEK )";
} elseif ($q=="1Month") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 1 MONTH )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 1 MONTH )";
} elseif ($q=="2Months") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 2 MONTH )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 2 MONTH )";
} elseif ($q=="3Months") {
  $sqlFilterNew = "Init >= ( CURDATE() - INTERVAL 3 MONTH )";
  $sqlFilterOld = "End >= ( CURDATE() - INTERVAL 3 MONTH )";
} else {
  $sqlFilterNew = "False";
  $sqlFilterOld = "False";
}

$sqlFilterNew = " Auto and " . $sqlFilterNew;
$sqlFilterOld = " Auto and " . $sqlFilterOld;


if ($s=="All Servers") {

  $sql = "Select Init as TimeUpdate, Server, Concat('New baseboard (', Handle, '): ', ProductName) as Event from Baseboard where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted baseboard (', Handle, '): ', ProductName) as Event from Baseboard where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New baseboard device (', Handle, '): ', Description) as Event from BaseboardDevice where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted baseboard device (', Handle, '): ', Description) as Event from BaseboardDevice where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Bios Characteristic: ', Characteristic) as Event from Bios where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Bios Characteristic: ', Characteristic) as Event from Bios where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Cache (', Handle, '): ', Designation) as Event from Cache where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Cache (', Handle, '): ', Designation) as Event from Cache where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Connector (', Handle, '): ', IntDesignator) as Event from Connector where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Connector (', Handle, '): ', IntDesignator) as Event from Connector where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Crontab (', User, '): ', Minute, ' ', Hour, ' ', Day, ' ', Month, ' ', DayWeek, ' ', Command) as Event from Crontab where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End TimeUpdate, Server, Concat('Deleted Crontab (', User, '): ', Minute, ' ', Hour, ' ', Day, ' ', Month, ' ', DayWeek, ' ', Command) as Event from Crontab where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New device (', Name, '): ', Model) as Event from Device where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted device (', Name, '): ', Model) as Event from Device where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New executable: ', Name, ' (', Package, ' package)') as Event from Exe where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted executable: ', Name, ' (', Package, ' package)') as Event from Exe where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New /etc/hosts line: ', Rule) as Event from FileHost where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted /etc/hosts line: ', Rule) as Event from FileHost where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New file system: ', Name, ' (', Type, ') ', Mount, ' ', Size, ' bytes') as Event from FileSystem where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted file system: ', Name, ' (', Type, ') ', Mount, ' ', Size, ' bytes') as Event from FileSystem where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New hardware: ', Name, ' (', Value, ')') as Event from Hardware where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted hardware: ', Name, ' (', Value, ')') as Event from Hardware where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New interface (', Name, '): ', Address, ' (', NameDNS, ') ', Network, ' ', Netmask, ' ', MAC, ' ', Type, ' ', Module) as Event from Interface where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted interface (', Name, '): ', Address, ' (', NameDNS, ') ', Network, ' ', Netmask, ' ', MAC, ' ', Type, ' ', Module) as Event from Interface where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New IPTables rule (', IPTable, ' ', Chain, '): ', Rule) as Event from IPTables  where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted IPTables rule (', IPTable, ' ', Chain, '): ', Rule) as Event from IPTables where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New IPTables policy (', IPTable, ' ', Chain, '): ', Policy) as Event from IPTablesPolicy  where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted IPTables policy (', IPTable, ' ', Chain, '): ', Policy) as Event from IPTablesPolicy where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New local user: ', Name, ' (UID ', UID, ' GID', GID, ') ', Home, ' ', Shell) as Event from LocalUser where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted local user: ', Name, ' (UID ', UID, ' GID', GID, ') ', Home, ' ', Shell) as Event from LocalUser where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New local group: ', Name, ' (GID ', GID, ')') as Event from LocalGroup where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted local group: ', Name, ' (GID ', GID, ')') as Event from LocalGroup where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New local group (user): ', GroupName, ' (', UserName, ')') as Event from LocalGroupUser where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted local group (user): ', GroupName, ' (', UserName, ')') as Event from LocalGroupUser where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New memory array (', Handle, '): ', MemoryUse, ' (Max ', MaxCapacity, ', Devices ', NumberDevices, ')') as Event from MemoryArray where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted memory array (', Handle, '): ', MemoryUse, ' (Max ', MaxCapacity, ', Devices ', NumberDevices, ')') as Event from MemoryArray where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New memory (', Handle, '): ', Type, ' ', Size, ' (Array ', Array, ')') as Event from Memory where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted memory (', Handle, '): ', Type, ' ', Size, ' (Array ', Array, ')') as Event from Memory where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New module (', Name, '): ', FileName) as Event from Module where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted module (', Name, '): ', FileName) as Event from Module where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Openvas Scan (', IP, '): ', StartScan, ' (CVSS ', CVSS, ' Severity ', Severity, ')') as Event from OpenvasHost where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Openvas Scan (', IP, '): ', StartScan, ' (CVSS ', CVSS, ' Severity ', Severity, ')') as Event from OpenvasHost where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New package: ', Name, ' ', Version) as Event from Package where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted package: ', Name, ' ', Version) as Event from Package where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New PAM access module: ', Module) as Event from PAMAccessModule where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted PAM access module: ', Module) as Event from PAMAccessModule where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New PAM access rule: ', Rule) as Event from PAMAccessRule where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted PAM access rule: ', Rule) as Event from PAMAccessRule where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New partition: ', Name, ' (Size ', Size, ' bytes)') as Event from Partition where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted partition: ', Name, ' (Size ', Size, ' bytes)') as Event from Partition where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New processor (', Socket, '): ', Type, ' (', CurrentSpeed, ')') as Event from Processor where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted processor (', Socket, '): ', Type, ' (', CurrentSpeed, ')') as Event from Processor where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New processor flag (', Socket, '): ', Flag, ' (', Value, ')') as Event from ProcessorFlag where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted processor flag (', Socket, '): ', Flag, ' (', Value, ')') as Event from ProcessorFlag where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New DNS resolver: ', NS1, ' ', NS2, ' ', NS3, ' (Domain ', Domain, ' Search ', Search, ')') as Event from Resolver where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted DNS resolver: ', NS1, ' ', NS2, ' ', NS3, ' (Domain ', Domain, ' Search ', Search, ')') as Event from Resolver where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New route: ', Destination, ' ', Mask, ' ', Gateway, ' ', Flags, ' ', Interface) as Event from Route where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted route: ', Destination, ' ', Mask, ' ', Gateway, ' ', Flags, ' ', Interface) as Event from Route where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New port (', Protocol, '/', Port, '): ', Process, ' (', ACCESS, ') IP4/', BindIP4, ' IP6/', BindIP6) as Event from ServerPort where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted port (', Protocol, '/', Port, '): ', Process, ' (', ACCESS, ') IP4/', BindIP4, ' IP6/', BindIP6) as Event from ServerPort where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Slot (', Handle, '): ', Designation) as Event from Slot where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Slot (', Handle, '): ', Designation) as Event from Slot where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New software: ', Name, ' (', Value, ')') as Event from Software where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted software: ', Name, ' (', Value, ')') as Event from Software where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New sudo alias: ', Rule) as Event from SudoAlias where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted sudo alias: ', Rule) as Event from SudoAlias where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New sudo defaults: ', Rule) as Event from SudoDefault where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted sudo default: ', Rule) as Event from SudoDefault where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New sudo user specs: ', Rule) as Event from SudoUserSpec where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted sudo user specs: ', Rule) as Event from SudoUserSpec where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New TCP Wrappers (', Service, '): ', Host, ' (', Type, ')') as Event from TCPWrappersHost where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted TCP Wrappers (', Service, '): ', Host, ' (', Type, ')') as Event from TCPWrappersHost where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows account: ', Caption) as Event from WinAccount where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows account: ', Caption) as Event from WinAccount where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows group: ', Caption) as Event from WinGroup where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows group: ', Caption) as Event from WinGroup where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows group (user): ', GroupName, ' (', UserName, ')') as Event from WinGroupUser where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows group (user): ', GroupName, ' (', UserName, ')') as Event from WinGroupUser where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows baseboard: ', Caption, ' (', Manufacturer, ')') as Event from WinBaseBoard where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows baseboard: ', Caption, ' (', Manufacturer, ')') as Event from WinBaseBoard where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows onboard device (', Tag, '): ', Description, ' (', DeviceType, ')') as Event from WinOnBoardDevice where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows onboard device (', Tag, '): ', Description, ' (', DeviceType, ')') as Event from WinOnBoardDevice where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Bios: ', Caption, ' (', Version, ')' ) as Event from WinBios where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Bios: ', Caption, ' (', Version, ')') as Event from WinBios where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Bios Characteristic: ', Description) as Event from WinBiosChar where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Bios Characteristic: ', Description) as Event from WinBiosChar where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Bus: ', DeviceID, ' (', BusType, ')' ) as Event from WinBus where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Bus: ', DeviceID, ' (', BusType, ')') as Event from WinBus where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Disk Drive (', DeviceID, '): ', Caption, ' (', Size, ' bytes)') as Event from WinDiskDrive where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Disk Drive (', DeviceID, '): ', Caption, ' (', Size, ' bytes)') as Event from WinDiskDrive where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Disk Partition: ', DeviceID, ' (', Size, ' bytes)') as Event from WinDiskPartition where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Disk Partition: ', DeviceID, ' (', Size, ' bytes)') as Event from WinDiskPartition where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Disk Drive (Partition): ', DiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinDiskDrivePartition where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Disk Drive (Partition): ', DiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinDiskDrivePartition where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Logical Disk (', DeviceID, '): ', DriveType, ' ', FileSystem, ' (', Size, ' bytes)') as Event from WinLogicalDisk where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Logical Disk (', DeviceID, '): ', DriveType, ' ', FileSystem, ' (', Size, ' bytes)') as Event from WinLogicalDisk where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Logical Disk (Partition): ', LogicalDiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinLogicalDiskPartition where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Logical Disk (Partition): ', LogicalDiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinLogicalDiskPartition where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Driver (', Name, '): ', Caption, ' (', ServiceType, ')') as Event from WinDriver where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Driver (', Name, '): ', Caption, ' (', ServiceType, ' )') as Event from WinDriver where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Memory Array (', Tag, '): ', Caption, ' (', MaxCapacity, ' KBytes)') as Event from WinMemoryArray where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Memory Array (', Tag, '): ', Caption, ' (', MaxCapacity, ' KBytes)') as Event from WinMemoryArray where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Memory (', Tag, '): ', Caption, ' (', Capacity, ' bytes)') as Event from WinMemory where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Memory (', Tag, '): ', Caption, ' (', Capacity, ' bytes)') as Event from WinMemory where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Memory Array (Memory): ', GroupTag, ' (', PartTag, ')') as Event from WinMemoryLocation where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Memory Array (Memory): ', GroupTag, ' (', PartTag, ')') as Event from WinMemoryLocation where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Network Adapter (', DeviceID, '): ', Name, ' ', AdapterType, ' (', MACAddress, ')') as Event from WinNetworkAdapter where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Network Adapter (', DeviceID, '): ', Name, ' ', AdapterType, ' (', MACAddress, ')') as Event from WinNetworkAdapter where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Network Adapter Config (', NetIndex, '): ', Description, ' ', IPAddress, ' ', IPSubnet, ' ', DefaultIPGateway) as Event from WinNetworkAdapterConfig where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Network Adapter Config (', NetIndex, '): ', Description, ' ', IPAddress, ' ', IPSubnet, ' ', DefaultIPGateway) as Event from WinNetworkAdapterConfig where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Network Adapter (Config): ', DeviceID, ' (', NetIndex, ')') as Event from WinNetworkAdapterSetting where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Network Adapter (Config): ', DeviceID, ' (', NetIndex, ')') as Event from WinNetworkAdapterSetting where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Port Connector (', Tag, '): ', PortType, ' (', InternalReferenceDesignator, ')') as Event from WinPortConnector where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Port Connector (', Tag, '): ', PortType, ' (', InternalReferenceDesignator, ')') as Event from WinPortConnector where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Processor (', DeviceID, '): ', Name, ' (', CurrentClockSpeed, ' MHz)') as Event from WinProcessor where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Processor (', DeviceID, '): ', Name, ' (', CurrentClockSpeed, ' MHz)') as Event from WinProcessor where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Service (', Name, '): ', Caption, ' (', State, ')') as Event from WinService where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Service (', Name, '): ', Caption, ' (', State, ')') as Event from WinService where " . $sqlFilterOld;
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Share (', Name, '): ', Caption, ' ', PathShare, ' (', TypeShare, ')') as Event from WinShare where " . $sqlFilterNew;
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Share (', Name, '): ', Caption, ' ', PathShare, ' (', TypeShare, ')') as Event from WinShare where " . $sqlFilterOld;
  $sql = $sql . " ORDER BY 1 DESC, 2";

} else {

  $sql = "Select Init as TimeUpdate, Server, Concat('New baseboard (', Handle, '): ', ProductName) as Event from Baseboard where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted baseboard (', Handle, '): ', ProductName) as Event from Baseboard where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New baseboard device (', Handle, '): ', Description) as Event from BaseboardDevice where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted baseboard device (', Handle, '): ', Description) as Event from BaseboardDevice where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Bios Characteristic: ', Characteristic) as Event from Bios where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Bios Characteristic: ', Characteristic) as Event from Bios where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Cache (', Handle, '): ', Designation) as Event from Cache where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Cache (', Handle, '): ', Designation) as Event from Cache where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Connector (', Handle, '): ', IntDesignator) as Event from Connector where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Connector (', Handle, '): ', IntDesignator) as Event from Connector where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Crontab (', User, '): ', Minute, ' ', Hour, ' ', Day, ' ', Month, ' ', DayWeek, ' ', Command) as Event from Crontab where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End TimeUpdate, Server, Concat('Deleted Crontab (', User, '): ', Minute, ' ', Hour, ' ', Day, ' ', Month, ' ', DayWeek, ' ', Command) as Event from Crontab where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New device (', Name, '): ', Model) as Event from Device where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted device (', Name, '): ', Model) as Event from Device where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New executable: ', Name, ' (', Package, ' package)') as Event from Exe where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted executable: ', Name, ' (', Package, ' package)') as Event from Exe where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New /etc/hosts line: ', Rule) as Event from FileHost where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted /etc/hosts line: ', Rule) as Event from FileHost where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New file system: ', Name, ' (', Type, ') ', Mount, ' ', Size, ' bytes') as Event from FileSystem where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted file system: ', Name, ' (', Type, ') ', Mount, ' ', Size, ' bytes') as Event from FileSystem where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New hardware: ', Name, ' (', Value, ')') as Event from Hardware where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted hardware: ', Name, ' (', Value, ')') as Event from Hardware where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New interface (', Name, '): ', Address, ' (', NameDNS, ') ', Network, ' ', Netmask, ' ', MAC, ' ', Type, ' ', Module) as Event from Interface where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted interface (', Name, '): ', Address, ' (', NameDNS, ') ', Network, ' ', Netmask, ' ', MAC, ' ', Type, ' ', Module) as Event from Interface where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New IPTables rule (', IPTable, ' ', Chain, '): ', Rule) as Event from IPTables  where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted IPTables rule (', IPTable, ' ', Chain, '): ', Rule) as Event from IPTables where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New IPTables policy (', IPTable, ' ', Chain, '): ', Policy) as Event from IPTablesPolicy  where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted IPTables policy (', IPTable, ' ', Chain, '): ', Policy) as Event from IPTablesPolicy where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New local user: ', Name, ' (UID ', UID, ' GID', GID, ') ', Home, ' ', Shell) as Event from LocalUser where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted local user: ', Name, ' (UID ', UID, ' GID', GID, ') ', Home, ' ', Shell) as Event from LocalUser where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New local group: ', Name, ' (GID ', GID, ')') as Event from LocalGroup where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted local group: ', Name, ' (GID ', GID, ')') as Event from LocalGroup where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New local group (user): ', GroupName, ' (', UserName, ')') as Event from LocalGroupUser where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted local group (user): ', GroupName, ' (', UserName, ')') as Event from LocalGroupUser where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New memory array (', Handle, '): ', MemoryUse, ' (Max ', MaxCapacity, ', Devices ', NumberDevices, ')') as Event from MemoryArray where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted memory array (', Handle, '): ', MemoryUse, ' (Max ', MaxCapacity, ', Devices ', NumberDevices, ')') as Event from MemoryArray where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New memory (', Handle, '): ', Type, ' ', Size, ' (Array ', Array, ')') as Event from Memory where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted memory (', Handle, '): ', Type, ' ', Size, ' (Array ', Array, ')') as Event from Memory where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New module (', Name, '): ', FileName) as Event from Module where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted module (', Name, '): ', FileName) as Event from Module where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Openvas Scan (', IP, '): ', StartScan, ' (CVSS ', CVSS, ' Severity ', Severity, ')') as Event from OpenvasHost where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Openvas Scan (', IP, '): ', StartScan, ' (CVSS ', CVSS, ' Severity ', Severity, ')') as Event from OpenvasHost where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New package: ', Name, ' ', Version) as Event from Package where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted package: ', Name, ' ', Version) as Event from Package where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New PAM access module: ', Module) as Event from PAMAccessModule where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted PAM access module: ', Module) as Event from PAMAccessModule where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New PAM access rule: ', Rule) as Event from PAMAccessRule where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted PAM access rule: ', Rule) as Event from PAMAccessRule where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New partition: ', Name, ' (Size ', Size, ' bytes)') as Event from Partition where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted partition: ', Name, ' (Size ', Size, ' bytes)') as Event from Partition where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New processor (', Socket, '): ', Type, ' (', CurrentSpeed, ')') as Event from Processor where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted processor (', Socket, '): ', Type, ' (', CurrentSpeed, ')') as Event from Processor where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New processor flag (', Socket, '): ', Flag, ' (', Value, ')') as Event from ProcessorFlag where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted processor flag (', Socket, '): ', Flag, ' (', Value, ')') as Event from ProcessorFlag where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New DNS resolver: ', NS1, ' ', NS2, ' ', NS3, ' (Domain ', Domain, ' Search ', Search, ')') as Event from Resolver where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted DNS resolver: ', NS1, ' ', NS2, ' ', NS3, ' (Domain ', Domain, ' Search ', Search, ')') as Event from Resolver where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New route: ', Destination, ' ', Mask, ' ', Gateway, ' ', Flags, ' ', Interface) as Event from Route where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted route: ', Destination, ' ', Mask, ' ', Gateway, ' ', Flags, ' ', Interface) as Event from Route where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New port (', Protocol, '/', Port, '): ', Process, ' (', ACCESS, ') IP4/', BindIP4, ' IP6/', BindIP6) as Event from ServerPort where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted port (', Protocol, '/', Port, '): ', Process, ' (', ACCESS, ') IP4/', BindIP4, ' IP6/', BindIP6) as Event from ServerPort where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Slot (', Handle, '): ', Designation) as Event from Slot where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Slot (', Handle, '): ', Designation) as Event from Slot where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New software: ', Name, ' (', Value, ')') as Event from Software where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted software: ', Name, ' (', Value, ')') as Event from Software where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New sudo alias: ', Rule) as Event from SudoAlias where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted sudo alias: ', Rule) as Event from SudoAlias where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New sudo defaults: ', Rule) as Event from SudoDefault where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted sudo default: ', Rule) as Event from SudoDefault where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New sudo user specs: ', Rule) as Event from SudoUserSpec where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted sudo user specs: ', Rule) as Event from SudoUserSpec where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New TCP Wrappers (', Service, '): ', Host, ' (', Type, ')') as Event from TCPWrappersHost where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted TCP Wrappers (', Service, '): ', Host, ' (', Type, ')') as Event from TCPWrappersHost where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows account: ', Caption) as Event from WinAccount where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows account: ', Caption) as Event from WinAccount where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows group: ', Caption) as Event from WinGroup where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows group: ', Caption) as Event from WinGroup where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows group (user): ', GroupName, ' (', UserName, ')') as Event from WinGroupUser where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows group (user): ', GroupName, ' (', UserName, ')') as Event from WinGroupUser where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows baseboard: ', Caption, ' (', Manufacturer, ')') as Event from WinBaseBoard where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows baseboard: ', Caption, ' (', Manufacturer, ')') as Event from WinBaseBoard where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows onboard device (', Tag, '): ', Description, ' (', DeviceType, ')') as Event from WinOnBoardDevice where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows onboard device (', Tag, '): ', Description, ' (', DeviceType, ')') as Event from WinOnBoardDevice where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Bios: ', Caption, ' (', Version, ')' ) as Event from WinBios where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Bios: ', Caption, ' (', Version, ')') as Event from WinBios where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Bios Characteristic: ', Description) as Event from WinBiosChar where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Bios Characteristic: ', Description) as Event from WinBiosChar where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Bus: ', DeviceID, ' (', BusType, ')' ) as Event from WinBus where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Bus: ', DeviceID, ' (', BusType, ')') as Event from WinBus where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Disk Drive (', DeviceID, '): ', Caption, ' (', Size, ' bytes)') as Event from WinDiskDrive where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Disk Drive (', DeviceID, '): ', Caption, ' (', Size, ' bytes)') as Event from WinDiskDrive where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Disk Partition: ', DeviceID, ' (', Size, ' bytes)') as Event from WinDiskPartition where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Disk Partition: ', DeviceID, ' (', Size, ' bytes)') as Event from WinDiskPartition where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Disk Drive (Partition): ', DiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinDiskDrivePartition where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Disk Drive (Partition): ', DiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinDiskDrivePartition where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Logical Disk (', DeviceID, '): ', DriveType, ' ', FileSystem, ' (', Size, ' bytes)') as Event from WinLogicalDisk where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Logical Disk (', DeviceID, '): ', DriveType, ' ', FileSystem, ' (', Size, ' bytes)') as Event from WinLogicalDisk where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Logical Disk (Partition): ', LogicalDiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinLogicalDiskPartition where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Logical Disk (Partition): ', LogicalDiskDeviceID, ' (', PartitionDeviceID, ')') as Event from WinLogicalDiskPartition where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Driver (', Name, '): ', Caption, ' (', ServiceType, ')') as Event from WinDriver where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Driver (', Name, '): ', Caption, ' (', ServiceType, ' )') as Event from WinDriver where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Memory Array (', Tag, '): ', Caption, ' (', MaxCapacity, ' KBytes)') as Event from WinMemoryArray where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Memory Array (', Tag, '): ', Caption, ' (', MaxCapacity, ' KBytes)') as Event from WinMemoryArray where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Memory (', Tag, '): ', Caption, ' (', Capacity, ' bytes)') as Event from WinMemory where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Memory (', Tag, '): ', Caption, ' (', Capacity, ' bytes)') as Event from WinMemory where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Memory Array (Memory): ', GroupTag, ' (', PartTag, ')') as Event from WinMemoryLocation where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Memory Array (Memory): ', GroupTag, ' (', PartTag, ')') as Event from WinMemoryLocation where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Network Adapter (', DeviceID, '): ', Name, ' ', AdapterType, ' (', MACAddress, ')') as Event from WinNetworkAdapter where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Network Adapter (', DeviceID, '): ', Name, ' ', AdapterType, ' (', MACAddress, ')') as Event from WinNetworkAdapter where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Network Adapter Config (', NetIndex, '): ', Description, ' ', IPAddress, ' ', IPSubnet, ' ', DefaultIPGateway) as Event from WinNetworkAdapterConfig where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Network Adapter Config (', NetIndex, '): ', Description, ' ', IPAddress, ' ', IPSubnet, ' ', DefaultIPGateway) as Event from WinNetworkAdapterConfig where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Network Adapter (Config): ', DeviceID, ' (', NetIndex, ')') as Event from WinNetworkAdapterSetting where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Network Adapter (Config): ', DeviceID, ' (', NetIndex, ')') as Event from WinNetworkAdapterSetting where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Port Connector (', Tag, '): ', PortType, ' (', InternalReferenceDesignator, ')') as Event from WinPortConnector where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Port Connector (', Tag, '): ', PortType, ' (', InternalReferenceDesignator, ')') as Event from WinPortConnector where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Processor (', DeviceID, '): ', Name, ' (', CurrentClockSpeed, ' MHz)') as Event from WinProcessor where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Processor (', DeviceID, '): ', Name, ' (', CurrentClockSpeed, ' MHz)') as Event from WinProcessor where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Service (', Name, '): ', Caption, ' (', State, ')') as Event from WinService where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Service (', Name, '): ', Caption, ' (', State, ')') as Event from WinService where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select Init as TimeUpdate, Server, Concat('New Windows Share (', Name, '): ', Caption, ' ', PathShare, ' (', TypeShare, ')') as Event from WinShare where " . $sqlFilterNew . " and Server = '" . $s . "'";
  $sql = $sql . " UNION Select End as TimeUpdate, Server, Concat('Deleted Windows Share (', Name, '): ', Caption, ' ', PathShare, ' (', TypeShare, ')') as Event from WinShare where " . $sqlFilterOld . " and Server = '" . $s . "'";
  $sql = $sql . " ORDER BY 1 DESC, 2";

}


$resultUpdate = mysql_query($sql);
$nrowsUpdate = mysql_num_rows($resultUpdate);


if ($s == "All Servers") {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Last Events ($s)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Time</th>
  <th>Server</th>
  <th>Event</th>
  </tr>";

  while($row = mysql_fetch_array($resultUpdate)) { 
    echo "<tr>";
    echo "<td>" . (isset($row['TimeUpdate']) ? $row['TimeUpdate'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Server']) ? $row['Server'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Event']) ? $row['Event'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='3'>Total: " . $nrowsUpdate . " events.</td></tr></table>"; 

} else {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Last Events ($s)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Time</th>
  <th>Event</th>
  </tr>";

  while($row = mysql_fetch_array($resultUpdate)) {
    echo "<tr>";
    echo "<td>" . (isset($row['TimeUpdate']) ? $row['TimeUpdate'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Event']) ? $row['Event'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='2'>Total: " . $nrowsUpdate . " events.</td></tr></table>";

}


mysql_close($con);
?>
