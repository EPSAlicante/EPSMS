<?php
require_once("conn.php");

$q=$_GET["q"];
$s=$_GET["s"];

if ($q == "Historical") {
  $sqlServer="SELECT * FROM Server WHERE Name = '" . $s . "' ORDER BY Init";
  $sqlPorts="SELECT * FROM ServerPort WHERE Server = '" . $s . "' ORDER BY Access, Protocol, Port";
  $sqlInterfaces="SELECT * FROM Interface WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlRoutes="SELECT * FROM Route WHERE Server = '" . $s . "' ORDER BY Num";
  $sqlHardware="SELECT * FROM Hardware WHERE Server = '" . $s . "' ORDER BY HardType, Name";
  $sqlSoftware="SELECT * FROM Software WHERE Server = '" . $s . "' ORDER BY SoftType, Name";
  $sqlFileSystems="SELECT * FROM FileSystem WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlDevices="SELECT * FROM Device WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlPartitions="SELECT * FROM Partition WHERE Server = '" . $s . "' ORDER BY Device, Name";
  $sqlMemoryArrays="SELECT * FROM MemoryArray WHERE Server = '" . $s . "' ORDER BY Handle";
  $sqlMemories="SELECT * FROM Memory WHERE Server = '" . $s . "' ORDER BY Array, Handle";
  $sqlProcessor="SELECT * FROM Processor WHERE Server = '" . $s . "' ORDER BY Socket";
  $sqlProcessorFlag="SELECT * FROM ProcessorFlag WHERE Server = '" . $s . "' ORDER BY Socket, Flag";
  $sqlBios="SELECT * FROM Bios WHERE Server = '" . $s . "' ORDER BY Characteristic";
  $sqlBaseboards="SELECT * FROM Baseboard WHERE Server = '" . $s . "' ORDER BY Handle";
  $sqlBaseboardDevices="SELECT * FROM BaseboardDevice WHERE Server = '" . $s . "' ORDER BY Handle";
  $sqlCaches="SELECT * FROM Cache WHERE Server = '" . $s . "' ORDER BY Handle";
  $sqlConnectors="SELECT * FROM Connector WHERE Server = '" . $s . "' ORDER BY Handle";
  $sqlSlots="SELECT * FROM Slot WHERE Server = '" . $s . "' ORDER BY Handle";
  $sqlModules="SELECT * FROM Module WHERE Server = '" . $s . "' ORDER BY Name, SrcVersion";
  $sqlUsers="SELECT * FROM LocalUser WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlGroups="SELECT * FROM LocalGroup WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlGroupsUsers="SELECT * FROM LocalGroupUser WHERE Server = '" . $s . "' ORDER BY GroupName, UserName";
  $sqlSudoDefaults="SELECT * FROM SudoDefault WHERE Server = '" . $s . "' ORDER BY Num";
  $sqlSudoAlias="SELECT * FROM SudoAlias WHERE Server = '" . $s . "' ORDER BY TypeAlias, NumAlias";
  $sqlSudoAliasItems="SELECT * FROM SudoAliasItem WHERE Server = '" . $s . "' ORDER BY TypeAlias, NumAlias, NumItem";
  $sqlSudoUserSpecs="SELECT * FROM SudoUserSpec WHERE Server = '" . $s . "' ORDER BY Num";
  $sqlResolver="SELECT * FROM Resolver WHERE Server = '" . $s . "' ORDER BY Server";
  $sqlResolverOptions="SELECT * FROM ResolverOption WHERE Server = '" . $s . "' ORDER BY ROption";
  $sqlFileHosts="SELECT * FROM FileHost WHERE Server = '" . $s . "' ORDER BY NumHost";
  $sqlFileHostAlias="SELECT * FROM FileHostAlias WHERE Server = '" . $s . "' ORDER BY NumHost, NumAlias";
  $sqlIPTablesPolicies="SELECT * FROM IPTablesPolicy WHERE Server = '" . $s . "' ORDER BY IPTable, Chain";
  $sqlIPTables="SELECT * FROM IPTables WHERE Server = '" . $s . "' ORDER BY IPTable, Chain, Num";
  $sqlTCPWrappers="SELECT * FROM TCPWrappers WHERE Server = '" . $s . "' ORDER BY Type, Service";
  $sqlTCPWrappersHosts="SELECT * FROM TCPWrappersHost WHERE Server = '" . $s . "' ORDER BY Type, Service, Host";
  $sqlPAMAccessModules="SELECT * FROM PAMAccessModule WHERE Server = '" . $s . "' ORDER BY Module";
  $sqlPAMAccessRules="SELECT * FROM PAMAccessRule WHERE Server = '" . $s . "' ORDER BY Num";
  $sqlPAMAccessRulesUsers="SELECT * FROM PAMAccessRuleUser WHERE Server = '" . $s . "' ORDER BY Num, User";
  $sqlPAMAccessRulesOrigins="SELECT * FROM PAMAccessRuleOrigin WHERE Server = '" . $s . "' ORDER BY Num, Origin";
  $sqlCrontabs="SELECT * FROM Crontab WHERE Server = '" . $s . "' ORDER BY Num";
  $sqlOpenvasHosts="SELECT * FROM OpenvasHost WHERE Server = '" . $s . "' ORDER BY ScanId";
  $sqlOpenvasResults="SELECT * FROM OpenvasResult WHERE Server = '" . $s . "' ORDER BY ScanId, Id";
  $sqlPackages="SELECT * FROM Package WHERE Server = '" . $s . "' ORDER BY Name, Version";
  $sqlExes="SELECT * FROM Exe WHERE Server = '" . $s . "' ORDER BY Name, Signature";
  $sqlWinAccounts="SELECT * FROM WinAccount WHERE Server = '" . $s . "' ORDER BY Domain, Name";
  $sqlWinBaseBoards="SELECT * FROM WinBaseBoard WHERE Server = '" . $s . "' ORDER BY Tag";
  $sqlWinBios="SELECT * FROM WinBios WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlWinBiosChars="SELECT * FROM WinBiosChar WHERE Server = '" . $s . "' ORDER BY Name, Charcode";
  $sqlWinBuses="SELECT * FROM WinBus WHERE Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinDiskDrives="SELECT * FROM WinDiskDrive WHERE Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinDiskDrivePartitions="SELECT * FROM WinDiskDrivePartition WHERE Server = '" . $s . "' ORDER BY DiskDeviceID, PartitionDeviceID";
  $sqlWinDiskPartitions="SELECT * FROM WinDiskPartition WHERE Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinDrivers="SELECT * FROM WinDriver WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlWinGroups="SELECT * FROM WinGroup WHERE Server = '" . $s . "' ORDER BY Domain, Name";
  $sqlWinGroupUsers="SELECT * FROM WinGroupUser WHERE Server = '" . $s . "' ORDER BY GroupDomain, GroupName, UserDomain, UserName";
  $sqlWinLogicalDisks="SELECT * FROM WinLogicalDisk WHERE Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinLogicalDiskPartitions="SELECT * FROM WinLogicalDiskPartition WHERE Server = '" . $s . "' ORDER BY LogicalDiskDeviceID, PartitionDeviceID";
  $sqlWinMemories="SELECT * FROM WinMemory WHERE Server = '" . $s . "' ORDER BY Tag";
  $sqlWinMemoryArrays="SELECT * FROM WinMemoryArray WHERE Server = '" . $s . "' ORDER BY Tag";
  $sqlWinMemoryLocations="SELECT * FROM WinMemoryLocation WHERE Server = '" . $s . "' ORDER BY GroupTag, PartTag";
  $sqlWinNetworkAdapters="SELECT * FROM WinNetworkAdapter WHERE Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinNetworkAdapterConfigs="SELECT * FROM WinNetworkAdapterConfig WHERE Server = '" . $s . "' ORDER BY NetIndex";
  $sqlWinNetworkAdapterSettings="SELECT * FROM WinNetworkAdapterSetting WHERE Server = '" . $s . "' ORDER BY DeviceID, NetIndex";
  $sqlWinOnBoardDevices="SELECT * FROM WinOnBoardDevice WHERE Server = '" . $s . "' ORDER BY Tag";
  $sqlWinPortConnectors="SELECT * FROM WinPortConnector WHERE Server = '" . $s . "' ORDER BY Tag";
  $sqlWinProcessors="SELECT * FROM WinProcessor WHERE Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinServices="SELECT * FROM WinService WHERE Server = '" . $s . "' ORDER BY Name";
  $sqlWinShares="SELECT * FROM WinShare WHERE Server = '" . $s . "' ORDER BY Name";
} else {
  $sqlServer="SELECT * FROM Server WHERE End IS NULL AND Name = '" . $s . "' ORDER BY Init";
  $sqlPorts="SELECT * FROM ServerPort WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Access, Protocol, Port";
  $sqlInterfaces="SELECT * FROM Interface WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlRoutes="SELECT * FROM Route WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num";
  $sqlHardware="SELECT * FROM Hardware WHERE End IS NULL AND Server = '" . $s . "' ORDER BY HardType, Name";
  $sqlSoftware="SELECT * FROM Software WHERE End IS NULL AND Server = '" . $s . "' ORDER BY SoftType, Name";
  $sqlFileSystems="SELECT * FROM FileSystem WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlDevices="SELECT * FROM Device WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlPartitions="SELECT * FROM Partition WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Device, Name";
  $sqlMemoryArrays="SELECT * FROM MemoryArray WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Handle";
  $sqlMemories="SELECT * FROM Memory WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Array, Handle";
  $sqlProcessor="SELECT * FROM Processor WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Socket";
  $sqlProcessorFlag="SELECT * FROM ProcessorFlag WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Socket, Flag";
  $sqlBios="SELECT * FROM Bios WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Characteristic";
  $sqlBaseboards="SELECT * FROM Baseboard WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Handle";
  $sqlBaseboardDevices="SELECT * FROM BaseboardDevice WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Handle";
  $sqlCaches="SELECT * FROM Cache WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Handle";
  $sqlConnectors="SELECT * FROM Connector WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Handle";
  $sqlSlots="SELECT * FROM Slot WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Handle";
  $sqlModules="SELECT * FROM Module WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name, SrcVersion";
  $sqlUsers="SELECT * FROM LocalUser WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlGroups="SELECT * FROM LocalGroup WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlGroupsUsers="SELECT * FROM LocalGroupUser WHERE End IS NULL AND Server = '" . $s . "' ORDER BY GroupName, UserName";
  $sqlSudoDefaults="SELECT * FROM SudoDefault WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num";
  $sqlSudoAlias="SELECT * FROM SudoAlias WHERE End IS NULL AND Server = '" . $s . "' ORDER BY TypeAlias, NumAlias";
  $sqlSudoAliasItems="SELECT * FROM SudoAliasItem WHERE End IS NULL AND Server = '" . $s . "' ORDER BY TypeAlias, NumAlias, NumItem";
  $sqlSudoUserSpec="SELECT * FROM SudoUserSpec WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num";
  $sqlResolver="SELECT * FROM Resolver WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Server";
  $sqlResolverOptions="SELECT * FROM ResolverOption WHERE End IS NULL AND Server = '" . $s . "' ORDER BY ROption";
  $sqlFileHosts="SELECT * FROM FileHost WHERE End IS NULL AND Server = '" . $s . "' ORDER BY NumHost";
  $sqlFileHostAlias="SELECT * FROM FileHostAlias WHERE End IS NULL AND Server = '" . $s . "' ORDER BY NumHost, NumAlias";
  $sqlIptablesPolicies="SELECT * FROM IPTablesPolicy WHERE End IS NULL AND Server = '" . $s . "' ORDER BY IPTable, Chain";
  $sqlIptables="SELECT * FROM IPTables WHERE End IS NULL AND Server = '" . $s . "' ORDER BY IPTable, Chain, Num";
  $sqlTCPWrappers="SELECT * FROM TCPWrappers WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Type, Service";
  $sqlTCPWrappersHosts="SELECT * FROM TCPWrappersHost WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Type, Service, Host";
  $sqlPAMAccessModules="SELECT * FROM PAMAccessModule WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Module";
  $sqlPAMAccessRules="SELECT * FROM PAMAccessRule WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num";
  $sqlPAMAccessRulesUsers="SELECT * FROM PAMAccessRuleUser WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num, User";
  $sqlPAMAccessRulesOrigins="SELECT * FROM PAMAccessRuleOrigin WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num, Origin";
  $sqlCrontabs="SELECT * FROM Crontab WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Num";
  $sqlOpenvasHosts="SELECT * FROM OpenvasHost WHERE End IS NULL AND Server = '" . $s . "' ORDER BY ScanId";
  $sqlOpenvasResults="SELECT * FROM OpenvasResult WHERE End IS NULL AND Server = '" . $s . "' ORDER BY ScanId, Id";
  $sqlPackages="SELECT * FROM Package WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name, Version";
  $sqlExes="SELECT * FROM Exe WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name, Signature";
  $sqlWinAccounts="SELECT * FROM WinAccount WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Domain, Name";
  $sqlWinBaseBoards="SELECT * FROM WinBaseBoard WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Tag";
  $sqlWinBios="SELECT * FROM WinBios WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlWinBiosChars="SELECT * FROM WinBiosChar WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name, Charcode";
  $sqlWinBuses="SELECT * FROM WinBus WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinDiskDrives="SELECT * FROM WinDiskDrive WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinDiskDrivePartitions="SELECT * FROM WinDiskDrivePartition WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DiskDeviceID, PartitionDeviceID";
  $sqlWinDiskPartitions="SELECT * FROM WinDiskPartition WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinDrivers="SELECT * FROM WinDriver WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlWinGroups="SELECT * FROM WinGroup WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Domain, Name";
  $sqlWinGroupUsers="SELECT * FROM WinGroupUser WHERE End IS NULL AND Server = '" . $s . "' ORDER BY GroupDomain, GroupName, UserDomain, UserName";
  $sqlWinLogicalDisks="SELECT * FROM WinLogicalDisk WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinLogicalDiskPartitions="SELECT * FROM WinLogicalDiskPartition WHERE End IS NULL AND Server = '" . $s . "' ORDER BY LogicalDiskDeviceID, PartitionDeviceID";
  $sqlWinMemories="SELECT * FROM WinMemory WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Tag";
  $sqlWinMemoryArrays="SELECT * FROM WinMemoryArray WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Tag";
  $sqlWinMemoryLocations="SELECT * FROM WinMemoryLocation WHERE End IS NULL AND Server = '" . $s . "' ORDER BY GroupTag, PartTag";
  $sqlWinNetworkAdapters="SELECT * FROM WinNetworkAdapter WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinNetworkAdapterConfigs="SELECT * FROM WinNetworkAdapterConfig WHERE End IS NULL AND Server = '" . $s . "' ORDER BY NetIndex";
  $sqlWinNetworkAdapterSettings="SELECT * FROM WinNetworkAdapterSetting WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID, NetIndex";
  $sqlWinOnBoardDevices="SELECT * FROM WinOnBoardDevice WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Tag";
  $sqlWinPortConnectors="SELECT * FROM WinPortConnector WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Tag";
  $sqlWinProcessors="SELECT * FROM WinProcessor WHERE End IS NULL AND Server = '" . $s . "' ORDER BY DeviceID";
  $sqlWinServices="SELECT * FROM WinService WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
  $sqlWinShares="SELECT * FROM WinShare WHERE End IS NULL AND Server = '" . $s . "' ORDER BY Name";
}

$resultServer = mysql_query($sqlServer);
$nrowsServer = mysql_num_rows($resultServer);

echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
<caption><H2>Server</H2></caption>
<tr style='background:#2D7297; color:white'>
<th>Name</th>
<th>IP</th>
<th>Init</th>
<th>End</th>
<th>Checked</th>
<th>Node</th>
</tr>";

while($row = mysql_fetch_array($resultServer)) { 
  echo "<tr>";
  echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
  echo "<td>" . (isset($row['IP']) ? $row['IP'] : "&nbsp;") . "</td>";
  echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
  echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
  echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
  echo "<td>" . (isset($row['Node']) ? $row['Node'] : "&nbsp;") . "</td>";
  echo "</tr>";
}
echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsServer . " regs.</td></tr></table>"; 


$resultPorts = mysql_query($sqlPorts);
$nrowsPorts = mysql_num_rows($resultPorts);

if ($nrowsPorts > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Ports</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Access</th>
  <th>Protocol</th>
  <th>Port</th>
  <th>IP4</th>
  <th>Bind IP4</th>
  <th>IP6</th>
  <th>Bind IP6</th>
  <th>Process</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPorts)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Access']) ? $row['Access'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Protocol']) ? $row['Protocol'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Port']) ? $row['Port'] : "&nbsp;") . "</td>";
    echo "<td>" . ($row['IP4']==1 ? "X" : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BindIP4']) ? $row['BindIP4'] : "&nbsp;") . "</td>";
    echo "<td>" . ($row['IP6']==1 ? "X" : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BindIP6']) ? $row['BindIP6'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Process']) ? $row['Process'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsPorts . " regs.</td></tr></table>";

}

  
$resultInterfaces = mysql_query($sqlInterfaces);
$nrowsInterfaces = mysql_num_rows($resultInterfaces);

if ($nrowsInterfaces > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Interfaces</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Address</th>
  <th>Name DNS</th>
  <th>Network</th>
  <th>Netmask</th>
  <th>MAC</th>
  <th>Type</th>
  <th>Module</th>
  <th>Active</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultInterfaces)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Address']) ? $row['Address'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NameDNS']) ? $row['NameDNS'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Network']) ? $row['Network'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Netmask']) ? $row['Netmask'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MAC']) ? $row['MAC'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Module']) ? $row['Module'] : "&nbsp;") . "</td>";
    echo "<td>" . ($row['Active']==1 ? "X" : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='12'>Total: " . $nrowsInterfaces . " regs.</td></tr></table>";

}


$resultRoutes = mysql_query($sqlRoutes);
$nrowsRoutes = mysql_num_rows($resultRoutes);

if ($nrowsRoutes > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Netwok Routes</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>Destination</th>
  <th>Gateway</th>
  <th>Mask</th>
  <th>Flags</th>
  <th>Interface</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultRoutes)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Destination']) ? $row['Destination'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Gateway']) ? $row['Gateway'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Mask']) ? $row['Mask'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Flags']) ? $row['Flags'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Interface']) ? $row['Interface'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsRoutes . " regs.</td></tr></table>";

}


$resultHardware = mysql_query($sqlHardware);
$nrowsHardware = mysql_num_rows($resultHardware);

if ($nrowsHardware > 0) {

  echo "<table border='1' cellpadding='6' style='background:#75B9E4'>
  <caption><H2>Hardware</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>HardType</th>
  <th>Name</th>
  <th>Value</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultHardware)) {
    echo "<tr>";
    echo "<td>" . (isset($row['HardType']) ? $row['HardType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Value']) ? $row['Value'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsHardware . " regs.</td></tr></table>";

}


$resultSoftware = mysql_query($sqlSoftware);
$nrowsSoftware = mysql_num_rows($resultSoftware);

if ($nrowsSoftware > 0) {

  echo "<table border='1' cellpadding='6' style='background:#75B9E4'>
  <caption><H2>Software</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>SoftType</th>
  <th>Name</th>
  <th>Value</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultSoftware)) {
    echo "<tr>";
    echo "<td>" . (isset($row['SoftType']) ? $row['SoftType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Value']) ? $row['Value'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsSoftware . " regs.</td></tr></table>";

}


$resultFileSystems = mysql_query($sqlFileSystems);
$nrowsFileSystems = mysql_num_rows($resultFileSystems);

if ($nrowsFileSystems > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>FileSystems</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Type</th>
  <th>Mount</th>
  <th>Options</th>
  <th>Size</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultFileSystems)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Mount']) ? $row['Mount'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Options']) ? $row['Options'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='8'>Total: " . $nrowsFileSystems . " regs.</td></tr></table>";

}


$resultDevices = mysql_query($sqlDevices);
$nrowsDevices = mysql_num_rows($resultDevices);

if ($nrowsDevices > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Devices</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Model</th>
  <th>Host</th>
  <th>Scheduler</th>
  <th>Size</th>
  <th>Vendor</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultDevices)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Model']) ? $row['Model'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Host']) ? $row['Host'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Scheduler']) ? $row['Scheduler'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Vendor']) ? $row['Vendor'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsDevices . " regs.</td></tr></table>";

}


$resultPartitions = mysql_query($sqlPartitions);
$nrowsPartitions = mysql_num_rows($resultPartitions);

if ($nrowsPartitions > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Partitions</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Device</th>
  <th>Size</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPartitions)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Device']) ? $row['Device'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsPartitions . " regs.</td></tr></table>";

}


$resultMemoryArrays = mysql_query($sqlMemoryArrays);
$nrowsMemoryArrays = mysql_num_rows($resultMemoryArrays);

if ($nrowsMemoryArrays > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Memory Arrays</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Handle</th>
  <th>Location</th>
  <th>Use</th>
  <th>Error Correction Type</th>
  <th>Maximum Capacity</th>
  <th>Number Of Devices</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultMemoryArrays)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Location']) ? $row['Location'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MemoryUse']) ? $row['MemoryUse'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ErrorCorrectionType']) ? $row['ErrorCorrectionType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MaxCapacity']) ? $row['MaxCapacity'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumberDevices']) ? $row['NumberDevices'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsMemoryArrays . " regs.</td></tr></table>";

}


$resultMemories = mysql_query($sqlMemories);
$nrowsMemories = mysql_num_rows($resultMemories);

if ($nrowsMemories > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Memory Slots</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Array</th>
  <th>Handle</th>
  <th>Locator</th>
  <th>Bank Locator</th>
  <th>Size</th>
  <th>Speed</th>
  <th>Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultMemories)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Array']) ? $row['Array'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Locator']) ? $row['Locator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BankLocator']) ? $row['BankLocator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Speed']) ? $row['Speed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='10'>Total: " . $nrowsMemories . " regs.</td></tr></table>";

}


$resultProcessor = mysql_query($sqlProcessor);
$nrowsProcessor = mysql_num_rows($resultProcessor);

if ($nrowsProcessor > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Processors</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Socket</th>
  <th>Type</th>
  <th>Family</th>
  <th>Vendor</th>
  <th>Signature</th>
  <th>ID</th>
  <th>Version</th>
  <th>Voltage</th>
  <th>ExternalClock</th>
  <th>MaxSpeed</th>
  <th>CurrentSpeed</th>
  <th>Status</th>
  <th>Upgrade</th>
  <th>L1Cache</th>
  <th>L2Cache</th>
  <th>L3Cache</th>
  <th>SerialNumber</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultProcessor)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Socket']) ? $row['Socket'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Family']) ? $row['Family'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Vendor']) ? $row['Vendor'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Signature']) ? $row['Signature'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ID']) ? $row['ID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Voltage']) ? $row['Voltage'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ExternalClock']) ? $row['ExternalClock'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MaxSpeed']) ? $row['MaxSpeed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CurrentSpeed']) ? $row['CurrentSpeed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Status']) ? $row['Status'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Upgrade']) ? $row['Upgrade'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L1Cache']) ? $row['L1Cache'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L2Cache']) ? $row['L2Cache'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L3Cache']) ? $row['L3Cache'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SerialNumber']) ? $row['SerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='20'>Total: " . $nrowsProcessor . " regs.</td></tr></table>";

}


$resultProcessorFlag = mysql_query($sqlProcessorFlag);
$nrowsProcessorFlag = mysql_num_rows($resultProcessorFlag);

if ($nrowsProcessorFlag > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Processor Flags</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Socket</th>
  <th>Flag</th>
  <th>Value</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultProcessorFlag)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Socket']) ? $row['Socket'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Flag']) ? $row['Flag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Value']) ? $row['Value'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsProcessorFlag . " regs.</td></tr></table>";

}


$resultBios = mysql_query($sqlBios);
$nrowsBios = mysql_num_rows($resultBios);

if ($nrowsBios > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Bios</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Characteristic</th>
  <th>Value</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultBios)) {
    echo "<tr>";
    echo "<td>" . ($row['Characteristic'] ? $row['Characteristic'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Value']) ? $row['Value'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsBios . " regs.</td></tr></table>";

}


$resultBaseboards = mysql_query($sqlBaseboards);
$nrowsBaseboards = mysql_num_rows($resultBaseboards);

if ($nrowsBaseboards > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Baseboards</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Handle</th>
  <th>Manufacturer</th>
  <th>Product Name</th>
  <th>Version</th>
  <th>Serial Number</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultBaseboards)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Product Name']) ? $row['Product Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SerialNumber']) ? $row['SerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='8'>Total: " . $nrowsBaseboards . " regs.</td></tr></table>";

}


$resultBaseboardDevices = mysql_query($sqlBaseboardDevices);
$nrowsBaseboardDevices = mysql_num_rows($resultBaseboardDevices);

if ($nrowsBaseboardDevices > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Baseboard Devices</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Handle</th>
  <th>Type</th>
  <th>Description</th>
  <th>Enabled</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultBaseboardDevices)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Description']) ? $row['Description'] : "&nbsp;") . "</td>";
    echo "<td>" . ($row['Enabled']==1 ? "X" : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='7'>Total: " . $nrowsBaseboardDevices . " regs.</td></tr></table>";

}


$resultCaches = mysql_query($sqlCaches);
$nrowsCaches = mysql_num_rows($resultCaches);

if ($nrowsCaches > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Caches</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Handle</th>
  <th>Designation</th>
  <th>Level</th>
  <th>Enabled</th>
  <th>Mode</th>
  <th>Location</th>
  <th>Installed Size</th>
  <th>Maximum Size</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultCaches)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Designation']) ? $row['Designation'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Level']) ? $row['Level'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Enabled']) ? $row['Enabled'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Mode']) ? $row['Mode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Location']) ? $row['Location'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['InstSize']) ? $row['InstSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MaxSize']) ? $row['MaxSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsCaches . " regs.</td></tr></table>";

}


$resultConnectors = mysql_query($sqlConnectors);
$nrowsConnectors = mysql_num_rows($resultConnectors);

if ($nrowsConnectors > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Connectors</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Handle</th>
  <th>Internal Designator</th>
  <th>Internal Type</th>
  <th>External Designator</th>
  <th>External Type</th>
  <th>Port Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultConnectors)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IntDesignator']) ? $row['IntDesignator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IntType']) ? $row['IntType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ExtDesignator']) ? $row['ExtDesignator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ExtType']) ? $row['ExtType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PortType']) ? $row['PortType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsConnectors . " regs.</td></tr></table>";

}


$resultSlots = mysql_query($sqlSlots);
$nrowsSlots = mysql_num_rows($resultSlots);

if ($nrowsSlots > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Slots</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Handle</th>
  <th>Designation</th>
  <th>SlotType</th>
  <th>SlotBusWidth</th>
  <th>Current Usage</th>
  <th>SlotLength</th>
  <th>SlotId</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultSlots)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Handle']) ? $row['Handle'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Designation']) ? $row['Designation'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SlotType']) ? $row['SlotType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SlotBusWidth']) ? $row['SlotBusWidth'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CurrentUsage']) ? $row['CurrentUsage'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SlotLength']) ? $row['SlotLength'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SlotId']) ? $row['SlotId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='10'>Total: " . $nrowsSlots . " regs.</td></tr></table>";

}


$resultModules = mysql_query($sqlModules);
$nrowsModules = mysql_num_rows($resultModules);

if ($nrowsModules > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Modules</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>FileName</th>
  <th>Author</th>
  <th>Descrition</th>
  <th>License</th>
  <th>Version</th>
  <th>Version Magic</th>
  <th>Src Version</th>
  <th>Depends</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultModules)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FileName']) ? $row['FileName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Author']) ? $row['Author'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Description']) ? $row['Description'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['License']) ? $row['License'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['VerMagic']) ? $row['VerMagic'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SrcVersion']) ? $row['SrcVersion'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Depends']) ? $row['Depends'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='12'>Total: " . $nrowsModules . " regs.</td></tr></table>";

}


$resultUsers = mysql_query($sqlUsers);
$nrowsUsers = mysql_num_rows($resultUsers);

if ($nrowsUsers > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Users</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>UID</th>
  <th>GID</th>
  <th>Password Type</th>
  <th>Last Change</th>
  <th>Description</th>
  <th>Home</th>
  <td>Shell</td>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultUsers)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['UID']) ? $row['UID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['GID']) ? $row['GID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PasswdType']) ? $row['PasswdType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['LastChange']) ? $row['LastChange'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Description']) ? $row['Description'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Home']) ? $row['Home'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Shell']) ? $row['Shell'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsUsers . " regs.</td></tr></table>";

}


$resultGroups = mysql_query($sqlGroups);
$nrowsGroups = mysql_num_rows($resultGroups);

if ($nrowsGroups > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Groups</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>GID</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultGroups)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['GID']) ? $row['GID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsGroups . " regs.</td></tr></table>";

}


$resultGroupsUsers = mysql_query($sqlGroupsUsers);
$nrowsGroupsUsers = mysql_num_rows($resultGroupsUsers);

if ($nrowsGroupsUsers > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Groups/Users Relationships</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>GroupName</th>
  <th>UserName</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultGroupsUsers)) {
    echo "<tr>";
    echo "<td>" . (isset($row['GroupName']) ? $row['GroupName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['UserName']) ? $row['UserName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsGroupsUsers . " regs.</td></tr></table>";

}


$resultSudoDefaults = mysql_query($sqlSudoDefaults);
$nrowsSudoDefaults = mysql_num_rows($resultSudoDefaults);

if ($nrowsSudoDefaults > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Sudo (Defaults)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>Rule</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultSudoDefaults)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Rule']) ? $row['Rule'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsSudoDefaults . " regs.</td></tr></table>";

}


$resultSudoAlias = mysql_query($sqlSudoAlias);
$nrowsSudoAlias = mysql_num_rows($resultSudoAlias);

if ($nrowsSudoAlias > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Sudo (Alias)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>TypeAlias</th>
  <th>NumAlias</th>
  <th>Rule</th>
  <th>Label</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultSudoAlias)) {
    echo "<tr>";
    echo "<td>" . (isset($row['TypeAlias']) ? $row['TypeAlias'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumAlias']) ? $row['NumAlias'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Rule']) ? $row['Rule'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Label']) ? $row['Label'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='7'>Total: " . $nrowsSudoAlias . " regs.</td></tr></table>";

}


$resultSudoAliasItems = mysql_query($sqlSudoAliasItems);
$nrowsSudoAliasItems = mysql_num_rows($resultSudoAliasItems);

if ($nrowsSudoAliasItems > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Sudo (Item Alias)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>TypeAlias</th>
  <th>NumAlias</th>
  <th>NumItem</th>
  <th>Item</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultSudoAliasItems)) {
    echo "<tr>";
    echo "<td>" . (isset($row['TypeAlias']) ? $row['TypeAlias'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumAlias']) ? $row['NumAlias'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumItem']) ? $row['NumItem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Item']) ? $row['Item'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='7'>Total: " . $nrowsSudoAliasItems . " regs.</td></tr></table>";

}


$resultSudoUserSpecs = mysql_query($sqlSudoUserSpecs);
$nrowsSudoUserSpecs = mysql_num_rows($resultSudoUserSpecs);

if ($nrowsSudoUserSpecs > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Sudo (User Specifications)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>Rule</th>
  <th>UserItem</th>
  <th>RunasItem</th>
  <th>HostItem</th>
  <th>CmndItem</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultSudoUserSpecs)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Rule']) ? $row['Rule'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['UserItem']) ? $row['UserItem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['RunasItem']) ? $row['RunasItem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['HostItem']) ? $row['HostItem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CmndItem']) ? $row['CmndItem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsSudoUserSpecs . " regs.</td></tr></table>";

}


$resultResolver = mysql_query($sqlResolver);
$nrowsResolver = mysql_num_rows($resultResolver);

if ($nrowsResolver > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Resolver (/etc/resolv.conf)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Domain</th>
  <th>Search</th>
  <th>NS1</th>
  <th>NS2</th>
  <th>NS3</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultResolver)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Domain']) ? $row['Domain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Search']) ? $row['Search'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NS1']) ? $row['NS1'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NS2']) ? $row['NS2'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NS3']) ? $row['NS3'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='8'>Total: " . $nrowsResolver . " regs.</td></tr></table>";

}


$resultResolverOptions = mysql_query($sqlResolverOptions);
$nrowsResolverOptions = mysql_num_rows($resultResolverOptions);

if ($nrowsResolverOptions > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Resolver Options (/etc/resolv.conf)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Option</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultResolverOptions)) {
    echo "<tr>";
    echo "<td>" . (isset($row['ROption']) ? $row['ROption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='4'>Total: " . $nrowsResolverOptions . " regs.</td></tr></table>";

}


$resultFileHosts = mysql_query($sqlFileHosts);
$nrowsFileHosts = mysql_num_rows($resultFileHosts);

if ($nrowsFileHosts > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Hosts (/etc/hosts)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>NumHost</th>
  <th>IP</th>
  <th>Rule</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultFileHosts)) {
    echo "<tr>";
    echo "<td>" . (isset($row['NumHost']) ? $row['NumHost'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IP']) ? $row['IP'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Rule']) ? $row['Rule'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsFileHosts . " regs.</td></tr></table>";

}


$resultFileHostAlias = mysql_query($sqlFileHostAlias);
$nrowsFileHostAlias = mysql_num_rows($resultFileHostAlias);

if ($nrowsFileHostAlias > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Host Alias (/etc/hosts)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>NumHost</th>
  <th>NumAlias</th>
  <th>Name</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultFileHostAlias)) {
    echo "<tr>";
    echo "<td>" . (isset($row['NumHost']) ? $row['NumHost'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumAlias']) ? $row['NumAlias'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsFileHostAlias . " regs.</td></tr></table>";

}


$resultIPTablesPolicies = mysql_query($sqlIPTablesPolicies);
$nrowsIPTablesPolicies = mysql_num_rows($resultIPTablesPolicies);

if ($nrowsIPTablesPolicies > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>IPTables (Policies)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Table</th>
  <th>Chain</th>
  <th>Policy</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultIPTablesPolicies)) {
    echo "<tr>";
    echo "<td>" . (isset($row['IPTable']) ? $row['IPTable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Chain']) ? $row['Chain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Policy']) ? $row['Policy'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsIPTablesPolicies . " regs.</td></tr></table>";

}


$resultIPTables = mysql_query($sqlIPTables);
$nrowsIPTables = mysql_num_rows($resultIPTables);

if ($nrowsIPTables > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>IPTables (Rules)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Table</th>
  <th>Chain</th>
  <th>Num</th>
  <th>Rule</th>
  <th>InterfaceIN</th>
  <th>InterfaceOUT</th>
  <th>Source</th>
  <th>Destination</th>
  <th>Protocol</th>
  <th>Src Port</th>
  <th>Dst Port</th>
  <th>State</th>
  <th>Jump</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultIPTables)) {
    echo "<tr>";
    echo "<td>" . (isset($row['IPTable']) ? $row['IPTable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Chain']) ? $row['Chain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Rule']) ? $row['Rule'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['InterfaceIN']) ? $row['InterfaceIN'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['InterfaceOUT']) ? $row['InterfaceOUT'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Source']) ? $row['Source'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Destination']) ? $row['Destination'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Protocol']) ? $row['Protocol'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SPort']) ? $row['SPort'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DPort']) ? $row['DPort'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['State']) ? $row['State'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Jump']) ? $row['Jump'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='16'>Total: " . $nrowsIPTables . " regs.</td></tr></table>";

}


$resultTCPWrappers = mysql_query($sqlTCPWrappers);
$nrowsTCPWrappers = mysql_num_rows($resultTCPWrappers);

if ($nrowsTCPWrappers > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>TCP Wrappers (Services)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Type</th>
  <th>Service</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultTCPWrappers)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Service']) ? $row['Service'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsTCPWrappers . " regs.</td></tr></table>";

}

$resultTCPWrappersHosts = mysql_query($sqlTCPWrappersHosts);
$nrowsTCPWrappersHosts = mysql_num_rows($resultTCPWrappersHosts);

if ($nrowsTCPWrappersHosts > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>TCP Wrappers (Hosts)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Type</th>
  <th>Service</th>
  <th>Host</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultTCPWrappersHosts)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Service']) ? $row['Service'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Host']) ? $row['Host'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsTCPWrappersHosts . " regs.</td></tr></table>";

}


$resultPAMAccessModules = mysql_query($sqlPAMAccessModules);
$nrowsPAMAccessModules = mysql_num_rows($resultPAMAccessModules);

if ($nrowsPAMAccessModules > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>PAM Access (Modules)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Module</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPAMAccessModules)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Module']) ? $row['Module'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='4'>Total: " . $nrowsPAMAccessModules . " regs.</td></tr></table>";

}


$resultPAMAccessRules = mysql_query($sqlPAMAccessRules);
$nrowsPAMAccessRules = mysql_num_rows($resultPAMAccessRules);

if ($nrowsPAMAccessRules > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>PAM Access Rules</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>Rule</th>
  <th>Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPAMAccessRules)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Rule']) ? $row['Rule'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Type']) ? $row['Type'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsPAMAccessRules . " regs.</td></tr></table>";

}


$resultPAMAccessRulesUsers = mysql_query($sqlPAMAccessRulesUsers);
$nrowsPAMAccessRulesUsers = mysql_num_rows($resultPAMAccessRulesUsers);

if ($nrowsPAMAccessRulesUsers > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>PAM Access Rules (Users)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>User</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPAMAccessRulesUsers)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['User']) ? $row['User'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsPAMAccessRulesUsers . " regs.</td></tr></table>";

}


$resultPAMAccessRulesOrigins = mysql_query($sqlPAMAccessRulesOrigins);
$nrowsPAMAccessRulesOrigins = mysql_num_rows($resultPAMAccessRulesOrigins);

if ($nrowsPAMAccessRulesOrigins > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>PAM Access Rules (Origins)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>Origin</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPAMAccessRulesOrigins)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Origin']) ? $row['Origin'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsPAMAccessRulesOrigins . " regs.</td></tr></table>";

}


$resultCrontabs = mysql_query($sqlCrontabs);
$nrowsCrontabs = mysql_num_rows($resultCrontabs);

if ($nrowsCrontabs > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Crontabs</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Num</th>
  <th>User</th>
  <th>Minute</th>
  <th>Hour</th>
  <th>Day</th>
  <th>Month</th>
  <th>Day of Week</th>
  <th>Command</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultCrontabs)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Num']) ? $row['Num'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['User']) ? $row['User'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Minute']) ? $row['Minute'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Hour']) ? $row['Hour'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Day']) ? $row['Day'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Month']) ? $row['Month'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DayWeek']) ? $row['DayWeek'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Command']) ? $row['Command'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsCrontabs . " regs.</td></tr></table>";

}


$resultOpenvasHosts = mysql_query($sqlOpenvasHosts);
$nrowsOpenvasHosts = mysql_num_rows($resultOpenvasHosts);

if ($nrowsOpenvasHosts > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Openvas scannings (Hosts)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Scan Id</th>
  <th>Start Scan</th>
  <th>IP</th>
  <th>CVSS</th>
  <th>Severity</th>
  <th>Total High</th>
  <th>Total Medium</th>
  <th>Total Low</th>
  <th>Total Log</th>
  <th>Total False Positive</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultOpenvasHosts)) {
    echo "<tr>";
    echo "<td>" . (isset($row['ScanId']) ? $row['ScanId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['StartScan']) ? $row['StartScan'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IP']) ? $row['IP'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CVSS']) ? $row['CVSS'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Severity']) ? $row['Severity'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalHigh']) ? $row['TotalHigh'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalMedium']) ? $row['TotalMedium'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalLow']) ? $row['TotalLow'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalLog']) ? $row['TotalLog'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalFalsePositive']) ? $row['TotalFalsePositive'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='13'>Total: " . $nrowsOpenvasHosts . " regs.</td></tr></table>";

}


$resultOpenvasResults = mysql_query($sqlOpenvasResults);
$nrowsOpenvasResults = mysql_num_rows($resultOpenvasResults);

if ($nrowsOpenvasResults > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Openvas scannings (Hosts)</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Scan Id</th>
  <th>Id</th>
  <th>Task Id</th>
  <th>Task Name</th>
  <th>Start Scan</th>
  <th>Result Id</th>
  <th>Port</th>
  <th>Protocol</th>
  <th>CVSS</th>
  <th>Severity</th>
  <th>NVT Name</th>
  <th>NVT OID</th>
  <th>Summary</th>
  <th>Specific Result</th>
  <th>Impact</th>
  <th>Solution</th>
  <th>Affected Software</th>
  <th>Vulnerability Insight</th>
  <th>Detection Method</th>
  <th>Product Detection Result</th>
  <th>BID</th>
  <th>CVE</th>
  <th>CERT</th>
  <th>Other Ref</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultOpenvasResults)) {
    echo "<tr>";
    echo "<td>" . (isset($row['ScanId']) ? $row['ScanId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Id']) ? $row['Id'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TaskId']) ? $row['TaskId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TaskName']) ? $row['TaskName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['StartScan']) ? $row['StartScan'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ResultId']) ? $row['ResultId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Port']) ? $row['Port'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Protocol']) ? $row['Protocol'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CVSS']) ? $row['CVSS'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Severity']) ? $row['Severity'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NVTName']) ? $row['NVTName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NVTOID']) ? $row['NVTOID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Summary']) ? $row['Summary'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SpecificResult']) ? $row['SpecificResult'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Impact']) ? $row['Impact'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Solution']) ? $row['Solution'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['AffectedSoftware']) ? $row['AffectedSoftware'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['VulnerabilityInsight']) ? $row['VulnerabilityInsight'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DetectionMethod']) ? $row['DetectionMethod'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ProductDetectionResult']) ? $row['ProductDetectionResult'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BID']) ? $row['BID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CVE']) ? $row['CVE'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CERT']) ? $row['CERT'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['OtherRef']) ? $row['OtherRef'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='27'>Total: " . $nrowsOpenvasResults . " regs.</td></tr></table>";

}


$resultPackages = mysql_query($sqlPackages);
$nrowsPackages = mysql_num_rows($resultPackages);

if ($nrowsPackages > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Packages</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Version</th>
  <th>Size</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultPackages)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='6'>Total: " . $nrowsPackages . " regs.</td></tr></table>";

}


$resultExes = mysql_query($sqlExes);
$nrowsExes = mysql_num_rows($resultExes);

if ($nrowsExes > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Executables</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Package</th>
  <th>File Size</th>
  <th>File User</th>
  <th>File Group</th>
  <th>File Permission</th>
  <th>Signature</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultExes)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Package']) ? $row['Package'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FileSize']) ? $row['FileSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FileUser']) ? $row['FileUser'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FileGroup']) ? $row['FileGroup'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FilePerms']) ? $row['FilePerms'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Signature']) ? $row['Signature'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='10'>Total: " . $nrowsExes . " regs.</td></tr></table>";

}


$resultWinAccounts = mysql_query($sqlWinAccounts);
$nrowsWinAccounts = mysql_num_rows($resultWinAccounts);

if ($nrowsWinAccounts > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Accounts</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Domain</th>
  <th>Name</th>
  <th>Caption</th>
  <th>Account Type</th>
  <th>Disabled</th>
  <th>FullName</th>
  <th>LocalAccount</th>
  <th>Lockout</th>
  <th>Password Changeable</th>
  <th>Password Expires</th>
  <th>Password Required</th>
  <th>SID</th>
  <th>SID Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinAccounts)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Domain']) ? $row['Domain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['AccountType']) ? $row['AccountType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Disabled']) ? $row['Disabled'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FullName']) ? $row['FullName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['LocalAccount']) ? $row['LocalAccount'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Lockout']) ? $row['Lockout'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PasswordChangeable']) ? $row['PasswordChangeable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PasswordExpires']) ? $row['PasswordExpires'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PasswordRequired']) ? $row['PasswordRequired'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SID']) ? $row['SID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SIDType']) ? $row['SIDType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='16'>Total: " . $nrowsWinAccounts . " regs.</td></tr></table>";

}


$resultWinGroups = mysql_query($sqlWinGroups);
$nrowsWinGroups = mysql_num_rows($resultWinGroups);

if ($nrowsWinGroups > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Groups</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Domain</th>
  <th>Name</th>
  <th>Caption</th>
  <th>Local Account</th>
  <th>SID</th>
  <th>SID Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinGroups)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Domain']) ? $row['Domain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['LocalAccount']) ? $row['LocalAccount'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SID']) ? $row['SID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SIDType']) ? $row['SIDType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsWinGroups . " regs.</td></tr></table>";

}


$resultWinGroupUsers = mysql_query($sqlWinGroupUsers);
$nrowsWinGroupUsers = mysql_num_rows($resultWinGroupUsers);

if ($nrowsWinGroupUsers > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Groups - Users </H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Group Domain</th>
  <th>Group Name</th>
  <th>User Domain</th>
  <th>User Name</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinGroupUsers)) {
    echo "<tr>";
    echo "<td>" . (isset($row['GroupDomain']) ? $row['GroupDomain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['GroupName']) ? $row['GroupName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['UserDomain']) ? $row['UserDomain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['UserName']) ? $row['UserName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='7'>Total: " . $nrowsWinGroupUsers . " regs.</td></tr></table>";

}


$resultWinBaseBoards = mysql_query($sqlWinBaseBoards);
$nrowsWinBaseBoards = mysql_num_rows($resultWinBaseBoards);

if ($nrowsWinBaseBoards > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows BaseBoards</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Tag</th>
  <th>Caption</th>
  <th>Manufacturer</th>
  <th>Product</th>
  <th>Model</th>
  <th>Version</th>
  <th>Serial Number</th>
  <th>Hosting Board</th>
  <th>Hot Swappable</th>
  <th>Powered On</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinBaseBoards)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Tag']) ? $row['Tag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Product']) ? $row['Product'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Model']) ? $row['Model'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SerialNumber']) ? $row['SerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['HostingBoard']) ? $row['HostingBoard'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['HotSwappable']) ? $row['HotSwappable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PoweredOn']) ? $row['PoweredOn'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='13'>Total: " . $nrowsWinBaseBoards . " regs.</td></tr></table>";

}


$resultWinOnBoardDevices = mysql_query($sqlWinOnBoardDevices);
$nrowsWinOnBoardDevices = mysql_num_rows($resultWinOnBoardDevices);

if ($nrowsWinOnBoardDevices > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows On Board Devices</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Tag</th>
  <th>Caption</th>
  <th>Description</th>
  <th>Device Type</th>
  <th>Manufacturer</th>
  <th>Model</th>
  <th>Version</th>
  <th>Serial Number</th>
  <th>Enabled</th>
  <th>Hot Swappable</th>
  <th>Powered On</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinOnBoardDevices)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Tag']) ? $row['Tag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Description']) ? $row['Description'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DeviceType']) ? $row['DeviceType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Model']) ? $row['Model'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SerialNumber']) ? $row['SerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Enabled']) ? $row['Enabled'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['HotSwappable']) ? $row['HotSwappable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PoweredOn']) ? $row['PoweredOn'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='14'>Total: " . $nrowsWinOnBoardDevices . " regs.</td></tr></table>";

}


$resultWinBios = mysql_query($sqlWinBios);
$nrowsWinBios = mysql_num_rows($resultWinBios);

if ($nrowsWinBios > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Bios</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Caption</th>
  <th>Software Element ID</th>
  <th>Software Element State</th>
  <th>Target Operating System</th>
  <th>Version</th>
  <th>Build Number</th>
  <th>CodeSet</th>
  <th>Current Language</th>
  <th>Identification Code</th>
  <th>Language Edition</th>
  <th>Manufacturer</th>
  <th>Primary BIOS</th>
  <th>Release Date</th>
  <th>Serial Number</th>
  <th>Status</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinBios)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SoftwareElementID']) ? $row['SoftwareElementID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SoftwareElementState']) ? $row['SoftwareElementState'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TargetOperatingSystem']) ? $row['TargetOperatingSystem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Version']) ? $row['Version'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BuildNumber']) ? $row['BuildNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CodeSet']) ? $row['CodeSet'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CurrentLanguage']) ? $row['CurrentLanguage'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IdentificationCode']) ? $row['IdentificationCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['LanguageEdition']) ? $row['LanguageEdition'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PrimaryBIOS']) ? $row['PrimaryBIOS'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ReleaseDate']) ? $row['ReleaseDate'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SerialNumber']) ? $row['SerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Status']) ? $row['Status'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='19'>Total: " . $nrowsWinBios . " regs.</td></tr></table>";

}


$resultWinBiosChars = mysql_query($sqlWinBiosChars);
$nrowsWinBiosChars = mysql_num_rows($resultWinBiosChars);

if ($nrowsWinBiosChars > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Bios Characteristics</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Char Code</th>
  <th>Description</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinBiosChars)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CharCode']) ? $row['CharCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Description']) ? $row['Description'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='3'>Total: " . $nrowsWinBiosChars . " regs.</td></tr></table>";

}


$resultWinBuses = mysql_query($sqlWinBuses);
$nrowsWinBuses = mysql_num_rows($resultWinBuses);

if ($nrowsWinBuses > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Buses</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>Caption</th>
  <th>Bus Type</th>
  <th>Bus Num</th>
  <th>Availability</th>
  <th>Config Manager Error</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinBuses)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BusType']) ? $row['BusType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BusNum']) ? $row['BusNum'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Availability']) ? $row['Availability'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ConfigManagerErrorCode']) ? $row['ConfigManagerErrorCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='9'>Total: " . $nrowsWinBuses . " regs.</td></tr></table>";

}


$resultWinDiskDrives = mysql_query($sqlWinDiskDrives);
$nrowsWinDiskDrives = mysql_num_rows($resultWinDiskDrives);

if ($nrowsWinDiskDrives > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Disk Drives</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>Caption</th>
  <th>Disk Index</th>
  <th>Interface Type</th>
  <th>Model</th>
  <th>Size</th>
  <th>Availability</th>
  <th>Total Heads</th>
  <th>Total Cylinders</th>
  <th>Tracks Per Cylinder</th>
  <th>Total Tracks</th>
  <th>Sectors Per Track</th>
  <th>Total Sectors</th>
  <th>Bytes Per Sector</th>
  <th>Default Block Size</th>
  <th>Media Type</th>
  <th>Partitions</th>
  <th>Config Manager Error Code</th>
  <th>Serial Number</th>
  <th>SCSI Bus</th>
  <th>SCSI Port</th>
  <th>SCSI Target ID</th>
  <th>SCSI Logical Unit</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinDiskDrives)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DiskIndex']) ? $row['DiskIndex'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['InterfaceType']) ? $row['InterfaceType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Model']) ? $row['Model'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Availability']) ? $row['Availability'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalHeads']) ? $row['TotalHeads'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalCylinders']) ? $row['TotalCylinders'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TracksPerCylinder']) ? $row['TracksPerCylinder'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalTracks']) ? $row['TotalTracks'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SectorsPerTrack']) ? $row['SectorsPerTrack'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalSectors']) ? $row['TotalSectors'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BytesPerSector']) ? $row['BytesPerSector'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DefaultBlockSize']) ? $row['DefaultBlockSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MediaType']) ? $row['MediaType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Partitions']) ? $row['Partitions'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ConfigManagerErrorCode']) ? $row['ConfigManagerErrorCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SerialNumber']) ? $row['SerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SCSIBus']) ? $row['SCSIBus'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SCSIPort']) ? $row['SCSIPort'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SCSITargetID']) ? $row['SCSITargetID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SCSILogicalUnit']) ? $row['SCSILogicalUnit'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='26'>Total: " . $nrowsWinDiskDrives . " regs.</td></tr></table>";

}


$resultWinDiskPartitions = mysql_query($sqlWinDiskPartitions);
$nrowsWinDiskPartitions = mysql_num_rows($resultWinDiskPartitions);

if ($nrowsWinDiskPartitions > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Disk Partitions</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>Caption</th>
  <th>Disk Index</th>
  <th>Partition Index</th>
  <th>Partition Type</th>
  <th>Size</th>
  <th>Block Size</th>
  <th>Number Of Blocks</th>
  <th>Access</th>
  <th>Availability</th>
  <th>Bootable</th>
  <th>Boot Partition</th>
  <th>Primary Partition</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinDiskPartitions)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DiskIndex']) ? $row['DiskIndex'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PartitionIndex']) ? $row['PartitionIndex'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PartitionType']) ? $row['PartitionType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BlockSize']) ? $row['BlockSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumberOfBlocks']) ? $row['NumberOfBlocks'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Access']) ? $row['Access'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Availability']) ? $row['Availability'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Bootable']) ? $row['Bootable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['BootPartition']) ? $row['BootPartition'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PrimaryPartition']) ? $row['PrimaryPartition'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='16'>Total: " . $nrowsWinDiskPartitions . " regs.</td></tr></table>";

}


$resultWinDiskDrivePartitions = mysql_query($sqlWinDiskDrivePartitions);
$nrowsWinDiskDrivePartitions = mysql_num_rows($resultWinDiskDrivePartitions);

if ($nrowsWinDiskDrivePartitions > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Disk Drives - Partitions</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Disk Device ID</th>
  <th>Partition Device ID</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinDiskDrivePartitions)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DiskDeviceID']) ? $row['DiskDeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PartitionDeviceID']) ? $row['PartitionDeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsWinDiskDrivePartitions . " regs.</td></tr></table>";

}


$resultWinLogicalDisks = mysql_query($sqlWinLogicalDisks);
$nrowsWinLogicalDisks = mysql_num_rows($resultWinLogicalDisks);

if ($nrowsWinLogicalDisks > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Logical Disks</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>Caption</th>
  <th>Drive Type</th>
  <th>File System</th>
  <th>Size</th>
  <th>Access</th>
  <th>Availability</th>
  <th>Compressed</th>
  <th>ConfigManagerErrorCode</th>
  <th>SupportsDiskQuotas</th>
  <th>QuotasDisabled</th>
  <th>SupportsFileBasedCompression</th>
  <th>Volume Name</th>
  <th>Volume Seriel Number</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinLogicalDisks)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DriveType']) ? $row['DriveType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FileSystem']) ? $row['FileSystem'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Size']) ? $row['Size'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Access']) ? $row['Access'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Availability']) ? $row['Availability'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Compressed']) ? $row['Compressed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ConfigManagerErrorCode']) ? $row['ConfigManagerErrorCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SupportsDiskQuotas']) ? $row['SupportsDiskQuotas'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['QuotasDisabled']) ? $row['QuotasDisabled'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['SupportsFileBasedCompression']) ? $row['SupportsFileBasedCompression'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['VolumeName']) ? $row['VolumeName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['VolumeSerialNumbre']) ? $row['VolumeSerialNumber'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='17'>Total: " . $nrowsWinLogicalDisks . " regs.</td></tr></table>";

}

$resultWinLogicalDiskPartitions = mysql_query($sqlWinLogicalDiskPartitions);
$nrowsWinLogicalDiskPartitions = mysql_num_rows($resultWinLogicalDiskPartitions);

if ($nrowsWinLogicalDiskPartitions > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Logical Disks - Partitions</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Logical Disk Device ID</th>
  <th>Partition Device ID</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinLogicalDiskPartitions)) {
    echo "<tr>";
    echo "<td>" . (isset($row['LogicalDiskDeviceID']) ? $row['LogicalDiskDeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PartitionDeviceID']) ? $row['PartitionDeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsWinLogicalDiskPartitions . " regs.</td></tr></table>";

}


$resultWinDrivers = mysql_query($sqlWinDrivers);
$nrowsWinDrivers = mysql_num_rows($resultWinDrivers);

if ($nrowsWinDrivers > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Drivers</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Caption</th>
  <th>Error Control</th>
  <th>Path Name</th>
  <th>Service Type</th>
  <th>Start Mode</th>
  <th>State</th>
  <th>Tag Id</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinDrivers)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ErrorControl']) ? $row['ErrorControl'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PathName']) ? $row['PathName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ServiceType']) ? $row['ServiceType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['StartMode']) ? $row['StartMode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['State']) ? $row['State'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TagId']) ? $row['TagId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsWinDrivers . " regs.</td></tr></table>";

}


$resultWinMemoryArrays = mysql_query($sqlWinMemoryArrays);
$nrowsWinMemoryArrays = mysql_num_rows($resultWinMemoryArrays);

if ($nrowsWinMemoryArrays > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Memory Arrays</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Tag</th>
  <th>Caption</th>
  <th>Hot Swappable</th>
  <th>Location</th>
  <th>Max Capacity</th>
  <th>Memory Devices</th>
  <th>Memory Error Correction</th>
  <th>Memory Use</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinMemoryArrays)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Tag']) ? $row['Tag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['HotSwappable']) ? $row['HotSwappable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Location']) ? $row['Location'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MaxCapacity']) ? $row['MaxCapacity'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MemoryDevices']) ? $row['MemoryDevices'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MemoryErrorCorrection']) ? $row['MemoryErrorCorrection'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MemoryUse']) ? $row['MemoryUse'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsWinMemoryArrays . " regs.</td></tr></table>";

}


$resultWinMemories = mysql_query($sqlWinMemories);
$nrowsWinMemories = mysql_num_rows($resultWinMemories);

if ($nrowsWinMemories > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Memories</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Tag</th>
  <th>Caption</th>
  <th>Capacity</th>
  <th>Data Width</th>
  <th>Total Width</th>
  <th>Device Locator</th>
  <th>Form Factor</th>
  <th>Hot Swappable</th>
  <th>Manufacturer</th>
  <th>Memory Type</th>
  <th>Position In Row</th>
  <th>Speed</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinMemories)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Tag']) ? $row['Tag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Capacity']) ? $row['Capacity'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DataWidth']) ? $row['DataWidth'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TotalWidth']) ? $row['TotalWidth'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DeviceLocator']) ? $row['DeviceLocator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['FormFactor']) ? $row['FormFactor'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['HotSwappable']) ? $row['HotSwappable'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MemoryType']) ? $row['MemoryType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PositionInRow']) ? $row['PositionInRow'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Speed']) ? $row['Speed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='15'>Total: " . $nrowsWinMemories . " regs.</td></tr></table>";

}


$resultWinMemoryLocations = mysql_query($sqlWinMemoryLocations);
$nrowsWinMemoryLocations = mysql_num_rows($resultWinMemoryLocations);

if ($nrowsWinMemoryLocations > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Memory Locations</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Group Tag</th>
  <th>Part Tag</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinMemoryLocations)) {
    echo "<tr>";
    echo "<td>" . (isset($row['GroupTag']) ? $row['GroupTag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PartTag']) ? $row['PartTag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsWinMemoryLocations . " regs.</td></tr></table>";

}


$resultWinNetworkAdapters = mysql_query($sqlWinNetworkAdapters);
$nrowsWinNetworkAdapters = mysql_num_rows($resultWinNetworkAdapters);

if ($nrowsWinNetworkAdapters > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Network Adapters</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>Name</th>
  <th>Adapter Type</th>
  <th>Manufacturer</th>
  <th>MAC Address</th>
  <th>Availability</th>
  <th>Config Manager Error Code</th>
  <th>Adapter Index</th>
  <th>Net Connection ID</th>
  <th>Net Connection Status</th>
  <th>Service Name</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinNetworkAdapters)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['AdapterType']) ? $row['AdapterType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MACAddress']) ? $row['MACAddress'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Availability']) ? $row['Availability'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ConfigManagerErrorCode']) ? $row['ConfigManagerErrorCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['AdapterIndex']) ? $row['AdapterIndex'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NetConnectionID']) ? $row['NetConnectionID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NetConnectionStatus']) ? $row['NetConnectionStatus'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ServiceName']) ? $row['ServiceName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='14'>Total: " . $nrowsWinNetworkAdapters . " regs.</td></tr></table>";

}


$resultWinNetworkAdapterConfigs = mysql_query($sqlWinNetworkAdapterConfigs);
$nrowsWinNetworkAdapterConfigs = mysql_num_rows($resultWinNetworkAdapterConfigs);

if ($nrowsWinNetworkAdapterConfigs > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Network Adapter Configs</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Net Index</th>
  <th>Description</th>
  <th>IP Address</th>
  <th>IP Subnet</th>
  <th>Default IP Gateway</th>
  <th>Default TOS</th>
  <th>Default TTL</th>
  <th>DHCP Enabled</th>
  <th>DHCP Server</th>
  <th>DNS Domain</th>
  <th>DNS Domain Suffix Search Order</th>
  <th>DNS Enabled For WINS Resolution</th>
  <th>DNS Domain Search Order</th>
  <th>IGMP Level</th>
  <th>MAC Address</th>
  <th>WINS Enabled LMHosts Lookup</th>
  <th>WINS Primary Server</th>
  <th>WINS Secondary Server</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinNetworkAdapterConfigs)) {
    echo "<tr>";
    echo "<td>" . (isset($row['NetIndex']) ? $row['NetIndex'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Description']) ? $row['Description'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IPAddress']) ? $row['IPAddress'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IPSubnet']) ? $row['IPSubnet'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DefaultIPGateway']) ? $row['DefaultIPGateway'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DefaultTOS']) ? $row['DefaultTOS'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DefaultTTL']) ? $row['DefaultTTL'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DHCPEnabled']) ? $row['DHCPEnabled'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DHCPServer']) ? $row['DHCPServer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DNSDomain']) ? $row['DNSDomain'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DNSDomainSuffixSearchOrder']) ? $row['DNSDomainSuffixSearchOrder'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DNSEnabledForWINSResolution']) ? $row['DNSEnabledForWINSResolution'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DNSDomainSearchOrder']) ? $row['DNSDomainSearchOrder'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['IGMPLevel']) ? $row['IGMPLevel'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MACAddress']) ? $row['MACAddress'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['WINSEnabledLMHostsLookup']) ? $row['WINSEnabledLMHostsLookup'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['WINSPrimaryServer']) ? $row['WINSPrimaryServer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['WINSSecondaryServer']) ? $row['WINSSecondaryServer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='21'>Total: " . $nrowsWinNetworkAdapterConfigs . " regs.</td></tr></table>";

}


$resultWinNetworkAdapterSettings = mysql_query($sqlWinNetworkAdapterSettings);
$nrowsWinNetworkAdapterSettings = mysql_num_rows($resultWinNetworkAdapterSettings);

if ($nrowsWinNetworkAdapterSettings > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Network Adapter Settings</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>NetIndex</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinNetworkAdapterSettings)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NetIndex']) ? $row['NetIndex'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='5'>Total: " . $nrowsWinNetworkAdapterSettings . " regs.</td></tr></table>";

}


$resultWinPortConnectors = mysql_query($sqlWinPortConnectors);
$nrowsWinPortConnectors = mysql_num_rows($resultWinPortConnectors);

if ($nrowsWinPortConnectors > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Port Connectors</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Tag</th>
  <th>Connector Type</th>
  <th>External Reference Designator</th>
  <th>Internal Reference Designator</th>
  <th>Port Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinPortConnectors)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Tag']) ? $row['Tag'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ConnectorType']) ? $row['ConnectorType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ExternalReferenceDesignator']) ? $row['ExternalReferenceDesignator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['InternalReferenceDesignator']) ? $row['InternalReferenceDesignator'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PortType']) ? $row['PortType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='8'>Total: " . $nrowsWinPortConnectors . " regs.</td></tr></table>";

}


$resultWinProcessors = mysql_query($sqlWinProcessors);
$nrowsWinProcessors = mysql_num_rows($resultWinProcessors);

if ($nrowsWinProcessors > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Processors</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Device ID</th>
  <th>Name</th>
  <th>Caption</th>
  <th>Config Manager Error Code</th>
  <th>CPU Status</th>
  <th>Current Clock Speed</th>
  <th>Data Width</th>
  <th>Family</th>
  <th>L2 Cache Size</th>
  <th>L2 Cache Speed</th>
  <th>L3 Cache Size</th>
  <th>L3 Cache Speed</th>
  <th>Manufacturer</th>
  <th>Max Clock Speed</th>
  <th>Number Of Cores</th>
  <th>Number Of Logical Processors</th>
  <th>Processor ID</th>
  <th>Processor Type</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinProcessors)) {
    echo "<tr>";
    echo "<td>" . (isset($row['DeviceID']) ? $row['DeviceID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ConfigManagerErrorCode']) ? $row['ConfigManagerErrorCode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CPUStatus']) ? $row['CPUStatus'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['CurrentClockSpeed']) ? $row['CurrentClockSpeed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['DataWidth']) ? $row['DataWidth'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Family']) ? $row['Family'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L2CacheSize']) ? $row['L2CacheSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L2CacheSpeed']) ? $row['L2CacheSpeed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L3CacheSize']) ? $row['L3CacheSize'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['L3CacheSpeed']) ? $row['L3CacheSpeed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Manufacturer']) ? $row['Manufacturer'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['MaxClockSpeed']) ? $row['MaxClockSpeed'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumberOfCores']) ? $row['NumberOfCores'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['NumberOfLogicalProcessors']) ? $row['NumberOfLogicalProcessors'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ProcessorID']) ? $row['ProcessorID'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ProcessorType']) ? $row['ProcessorType'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='21'>Total: " . $nrowsWinProcessors . " regs.</td></tr></table>";

}


$resultWinServices = mysql_query($sqlWinServices);
$nrowsWinServices = mysql_num_rows($resultWinServices);

if ($nrowsWinServices > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Services</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Caption</th>
  <th>Error Control</th>
  <th>Path Name</th>
  <th>Process Id</th>
  <th>Start Mode</th>
  <th>State</th>
  <th>Tag Id</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinServices)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ErrorControl']) ? $row['ErrorControl'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PathName']) ? $row['PathName'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['ProcessId']) ? $row['ProcessId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['StartMode']) ? $row['StartMode'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['State']) ? $row['State'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TagId']) ? $row['TagId'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='11'>Total: " . $nrowsWinServices . " regs.</td></tr></table>";

}


$resultWinShares = mysql_query($sqlWinShares);
$nrowsWinShares = mysql_num_rows($resultWinShares);

if ($nrowsWinShares > 0) {

  echo "<table border='1' cellpadding='5' style='background:#75B9E4'>
  <caption><H2>Windows Shares</H2></caption>
  <tr style='background:#2D7297; color:white'>
  <th>Name</th>
  <th>Caption</th>
  <th>Path Share</th>
  <th>Type Share</th>
  <th>Init</th>
  <th>End</th>
  <th>Checked</th>
  </tr>";

  while($row = mysql_fetch_array($resultWinShares)) {
    echo "<tr>";
    echo "<td>" . (isset($row['Name']) ? $row['Name'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Caption']) ? $row['Caption'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['PathShare']) ? $row['PathShare'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['TypeShare']) ? $row['TypeShare'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Init']) ? $row['Init'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['End']) ? $row['End'] : "&nbsp;") . "</td>";
    echo "<td>" . (isset($row['Checked']) ? $row['Checked'] : "&nbsp;") . "</td>";
    echo "</tr>";
  }
  echo "<tr style='background:#2D7297; color:white'><td colspan='8'>Total: " . $nrowsWinShares . " regs.</td></tr></table>";

}





mysql_close($con);
?>
