<?php
require_once("../db.php");

$con = mysql_connect("$hostDB", "$userDB", "$passwdDB");
if (!$con)
 {
 die('Could not connect: ' . mysql_error());
 }

mysql_select_db("$nameDB", $con);
?>
