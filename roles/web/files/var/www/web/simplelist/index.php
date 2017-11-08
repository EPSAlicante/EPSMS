<html>
<head>
<script src="ajax.js"></script>
</head>
<body style="background:#A4BBC7">

<div align="center">
<H1>SIMPLE LIST (list of tables' data)</H1>
<form>
<div id="combos">
<table border='0' cellpadding='10'>
<tr>
<td><div id="comboType">
Select Query Type: 
<select name='type' onchange='showComboServer(this.value)'>
<option value='X'>Select Query</option>
<option value='Current'>Current Data</option>
<option value='Historical'>Historical Data</option>
</select>
</div></td>
<td><div id="comboServer">
</div></td>
</tr>
</table>
</div>
</form>

<p>
<div id="listado"></div>
</p>

</div>

</body>
</html>
