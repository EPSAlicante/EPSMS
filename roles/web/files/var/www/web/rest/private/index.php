<?php
include_once '../epiphany/src/Epi.php';
include_once './paths/hardware/hardware.php';
include_once './paths/software/software.php';
include_once './paths/security/security.php';

// DB variables
require_once("../../db.php");

// Allow from any origin
header("Access-Control-Allow-Origin: *");

chdir('.');
Epi::setPath('base', '../epiphany/src');
Epi::setPath('config', dirname(__FILE__));
Epi::setSetting('exceptions', true);
Epi::init('route','database','api');
EpiDatabase::employ('mysql',$nameDB,$hostDB,$userDB,$passwdDB);

getDatabase()->execute("SET NAMES 'utf8'");

/*
 * ******************************************************************************************
 * Load the routes from routes.ini then call run()
 * ******************************************************************************************
 */
getRoute()->load('routes.ini');
getRoute()->load('paths/hardware/routes.ini');
getRoute()->load('paths/software/routes.ini');
getRoute()->load('paths/security/routes.ini');
#getRoute()->load('paths/aulas/routes.ini',EpiApi::internal);

getRoute()->get('.*', 'error404');
getRoute()->post('.*', 'error404');
getRoute()->put('.*', 'error404');
getRoute()->delete('.*', 'error404');
getRoute()->run(); 

/*
 * ******************************************************************************************
 * Define functions and classes which are executed by EpiCode based on the $_['routes'] array
 * ******************************************************************************************
 */
function error404() {
	header('HTTP/1.1 404 Not Found');
}

class MyClass
{
	static public function MyMethod()
	{
		header('Content-Type: text/html; charset=utf-8');
		readfile("private.html");
	}

}



?>
