<?php
/**
 * English language file for authhttp plugin
 *
 * @author Pieter Hollants <pieter@hollants.com>
 */

$lang['plugin_settings_name'] = 'HTTP authentication plugin';

$lang['usernameregex'] = 'Regular expression to match the username part in HTTP authentication login names. Defaults to <tt>.+</tt>, use <tt>^[^@]+</tt> in Kerberos environments with usernames such as <em>user@domain</em> and <tt>&#92;&#92;[^&#92;&#92;]+$</tt> in Windows domain scenarios with usernames such as <em>DOMAIN\User</em>.';
$lang['emaildomain']   = 'Domain to append for creating email addresses';
$lang['specialusers']  = 'Usernames belonging to the special group';
$lang['specialgroup']  = 'Name of the special group';

//Setup VIM: ex: et ts=4 :
