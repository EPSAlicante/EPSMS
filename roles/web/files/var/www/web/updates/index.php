<html>
<head>
<script src="ajax.js"></script>
</head>
<body style="background:#A4BBC7">

<div align="center">
<H1>UPDATES LIST (last events)</H1>
<form>
<div id="combos">
<table border='0' cellpadding='10'>
<tr>
<td><div id="comboType">
Select Time: 
<select name='type' onchange='showComboServer(this.value)' onkeyup='showComboServer(this.value)'>
<option value='X'>Select Time</option>
<option value='1Day'>Last day</option>
<option value='2Days'>Last 2 days</option>
<option value='3Days'>Last 3 days</option>
<option value='4Days'>Last 4 days</option>
<option value='1Week'>Last week</option>
<option value='2Weeks'>Last 2 weeks</option>
<option value='1Month'>Last month</option>
<option value='2Months'>Last 2 months</option>
<option value='3Months'>Last 3 months</option>
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
