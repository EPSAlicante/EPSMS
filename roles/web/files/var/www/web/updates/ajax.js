var xmlHttp;

function showComboServer(strType)
{
xmlHttp=GetXmlHttpObject();
if (xmlHttp==null)
 {
 alert ("Browser does not support HTTP Request");
 return;
 }
var url="getComboServer.php";
url=url+"?q="+strType;
url=url+"&sid="+Math.random();
xmlHttp.onreadystatechange=comboChanged;
xmlHttp.open("GET",url,true);
xmlHttp.send(null);
}

function comboChanged()
{
if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete")
 {
 document.getElementById("comboServer").innerHTML=xmlHttp.responseText;
 }
}

function showTableServer(strType,strServer)
{ 
xmlHttp=GetXmlHttpObject();
if (xmlHttp==null)
 {
 alert ("Browser does not support HTTP Request");
 return;
 }
var url="getTableServer.php";
url=url+"?q="+strType;
url=url+"&s="+strServer;
url=url+"&sid="+Math.random();
xmlHttp.onreadystatechange=listadoChanged;
xmlHttp.open("GET",url,true);
xmlHttp.send(null);
}

function listadoChanged() 
{ 
if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete")
 { 
 document.getElementById("listado").innerHTML=xmlHttp.responseText;
 } 
}

function GetXmlHttpObject()
{
var xmlHttp=null;
try
 {
 // Firefox, Opera 8.0+, Safari
 xmlHttp=new XMLHttpRequest();
 }
catch (e)
 {
 //Internet Explorer
 try
  {
  xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
  }
 catch (e)
  {
  xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
 }
return xmlHttp;
}
