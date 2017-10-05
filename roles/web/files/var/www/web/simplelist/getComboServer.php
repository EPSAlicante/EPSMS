<?php
require_once("conn.php");

$q=$_GET["q"];

if ($q=="Historical") {
  $sql="SELECT Name FROM Server GROUP BY Name ORDER BY Name";
} else {
  $sql="SELECT Name FROM Server WHERE End IS NULL ORDER BY Name";
}

$result = mysql_query($sql);

$nrows = mysql_num_rows($result);

if ($nrows > 0) {

  echo "Select Host: ";
  echo "<select name='servers' onchange='showTableServer(\"" . $q . "\",this.value)'>";
  echo "<option value='X'>Select Host</option>";

  while($row = mysql_fetch_array($result)) {
    echo "<option value='" . $row['Name'] . "'>" . $row['Name'] . "</option>";
  }

  echo "</select>";

} else {
  echo "No hosts";
}

mysql_close($con);
?>
