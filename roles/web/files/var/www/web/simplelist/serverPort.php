<?php

  $q = intval($_GET['q']);

  include("../db.php");

  // Connecy to DataBase
  $link = mysql_connect("$hostDB", "$userDB", "$passwdDB")
    or die('Connection failed: ' . mysql_error());
  mysql_select_db('inventory') or die('Failed using database');

  // Mysql query 
  $sql = "SELECT * FROM ServerPort WHERE Server='" . $q . "' order by Protocol, Port, Process" 
  $query = mysql_query($sql, $link) or die ("Query failed");

  // Rows count 
  $nfilas = mysql_num_rows($query);

  if ($nfilas > 0) {

    print ("<TABLE WIDTH='650' border='1'>\n");
    print ("<TR>\n");
    print ("<TH WIDTH='100'>Server</TH>\n");
    print ("<TH WIDTH='10'>Protocol</TH>\n");
    print ("<TH WIDTH='10'>Port</TH>\n");
    print ("<TH WIDTH='50'>Process</TH>\n");
    print ("<TH WIDTH='20'>Init</TH>\n");
    print ("<TH WIDTH='20'>End</TH>\n");
    print ("<TH WIDTH='20'>Checked</TH>\n");
    print ("</TR>\n");

    for ($i=0; $i<$nfilas; $i++) {

      $result = mysql_fetch_array($query);
      print ("<TR>\n");
      print ("<TD>" . $result['Server'] . "</TD>\n");
      print ("<TD>" . $result['Protocol'] . "</TD>\n");
      print ("<TD>" . $result['Port'] . "</TD>\n");
      print ("<TD>" . $result['Process'] . "</TD>\n");
      print ("<TD>" . $result['Init'] . "</TD>\n");
      print ("<TD>" . $result['End'] . "</TD>\n");
      print ("<TD>" . $result['Checked'] . "</TD>\n");
      print ("</TR>\n");

    }

    print ("</TABLE>\n");

  } else {

    print ("No data");

  }

  // Closing connection
  mysql_close($link);
  ?>

</BODY>

</HTML>
