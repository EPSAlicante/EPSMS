<?php
require_once("conn.php");

$q=$_GET["q"];

if ($q=="1Day") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 1 DAY ) or End >= ( CURDATE() - INTERVAL 1 DAY ) )";
} elseif ($q=="2Days") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 2 DAY ) or End >= ( CURDATE() - INTERVAL 2 DAY ) )";
} elseif ($q=="3Days") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 3 DAY ) or End >= ( CURDATE() - INTERVAL 3 DAY ) )";
} elseif ($q=="4Days") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 4 DAY ) or End >= ( CURDATE() - INTERVAL 4 DAY ) )";
} elseif ($q=="1Week") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 1 WEEK ) or End >= ( CURDATE() - INTERVAL 1 WEEK ) )";
} elseif ($q=="2Weeks") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 2 WEEK ) or End >= ( CURDATE() - INTERVAL 2 WEEK ) )";
} elseif ($q=="1Month") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 1 MONTH ) or End >= ( CURDATE() - INTERVAL 1 MONTH ) )";
} elseif ($q=="2Months") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 2 MONTH ) or End >= ( CURDATE() - INTERVAL 2 MONTH ) )";
} elseif ($q=="3Months") {
  $sqlFilter = "( Init >= ( CURDATE() - INTERVAL 3 MONTH ) or End >= ( CURDATE() - INTERVAL 3 MONTH ) )";
} else {
  $sqlFilter = "False";
}

$sqlFilter = " Auto and " . $sqlFilter;


$sql = "Select Server from Baseboard where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from BaseboardDevice where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Bios where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Cache where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Connector where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Crontab where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Device where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Exe where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from FileHost where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from FileSystem where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Hardware where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Interface where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from IPTables where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from IPTablesPolicy where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from LocalGroup where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from LocalGroupUser where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from LocalUser where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Memory where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from MemoryArray where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Module where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from OpenvasHost where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Package where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from PAMAccessModule where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from PAMAccessRule where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from PAMAccessRuleOrigin where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from PAMAccessRuleUser where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Partition where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Processor where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from ProcessorFlag where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Resolver where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Route where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from ServerPort where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Slot where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from Software where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from SudoAlias where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from SudoDefault where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from SudoUserSpec where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from TCPWrappersHost where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinAccount where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinBaseBoard where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinBios where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinBiosChar where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinBus where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinDiskDrive where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinDiskDrivePartition where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinDriver where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinGroup where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinGroupUser where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinLogicalDisk where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinLogicalDiskPartition where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinMemory where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinMemoryArray where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinMemoryLocation where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinNetworkAdapter where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinNetworkAdapterConfig where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinNetworkAdapterSetting where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinOnBoardDevice where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinPortConnector where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinProcessor where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinService where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinShare where " . $sqlFilter . " group by Server";
$sql = $sql . " UNION Select Server from WinPackage where " . $sqlFilter . " group by Server";
$sql = $sql . " ORDER BY 1";


$result = mysql_query($sql);

$nrows = mysql_num_rows($result);

if ($nrows > 0) {

  echo "Select Host: ";
  echo "<select name='servers' onchange='showTableServer(\"" . $q . "\",this.value)' onkeyup='showTableServer(\"" . $q . "\",this.value)'>";
  echo "<option value='X'>Select Host</option>";
  echo "<option value='All Hosts'>All Hosts</option>";

  while($row = mysql_fetch_array($result)) {
    echo "<option value='" . $row['Server'] . "'>" . $row['Server'] . "</option>";
  }

  echo "</select>";

} else {
  echo "No updates";
}

mysql_close($con);
?>
