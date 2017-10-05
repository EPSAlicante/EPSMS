<?php
/**
 * Options for the authhttp plugin
 *
 * @author Pieter Hollants <pieter@hollants.com>
 */

$meta['usernameregex'] = array('string',  '_cautionList' => array('plugin____authhttp____userregex' => 'danger'));
$meta['emaildomain']   = array('string');
$meta['specialusers']  = array('string', '_cautionList' => array('plugin____authhttp____specialusers' => 'danger'));
$meta['specialgroup']  = array('string', '_cautionList' => array('plugin____authhttp____specialgroup' => 'danger'));
