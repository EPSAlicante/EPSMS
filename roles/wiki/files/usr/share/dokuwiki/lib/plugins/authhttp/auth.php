<?php
/**
 * DokuWiki HTTP authentication plugin
 * https://www.dokuwiki.org/plugin:authhttp
 *
 * This plugin basically replaces DokuWiki's own authentication features
 * with the HTTP authentication configured in the Webserver. As only login name and
 * password are known:
 * - the user's real name is set to his login name
 * - a possibly non-working email address is constructed with the "emaildomain"
 *   config setting
 * - all users are part of the DokuWiki group configured with DokuWiki's
 *   "defaultgroup" config setting
 * - users that are specified in the list configured with "specialusers" will
 *   also be member of the group configured with "specialgroup" (default: "admin")
 *
 * These restrictions may not suit your setup, in which case you should check out
 * the "authsplit" plugin at https://www.dokuwiki.org/plugin:authhttp.
 *
 * This plugin in based on the ideas in the "ggauth" auth backend by Grant Gardner
 * <grant@lastweekend.com.au>, https://www.dokuwiki.org/auth:ggauth.
 *
 * @license GPL 3 http://www.gnu.org/licenses/gpl-3.0.html
 * @author  Pieter Hollants <pieter@hollants.com>
 */

// must be run within Dokuwiki
if(!defined('DOKU_INC')) die();

/* We have to distinguish between the plugin being loaded and the plugin
   actually being used for authentication. */
$active = (
    $conf['authtype'] == 'authhttp' ||
    (
        $conf['authtype'] == 'authsplit' &&
        $conf['plugin']['authsplit']['primary_authplugin'] == 'authhttp'
    )
);

class auth_plugin_authhttp extends DokuWiki_Auth_Plugin {
    protected $usernameregex;
    protected $emaildomain;
    protected $specialusers;
    protected $specialgroup;

    /**
     * Constructor.
     */
    public function __construct() {
        global $conf;

        parent::__construct();

        /* Make sure that HTTP authentication has been enabled in the Web
           server. Note that does not seem to work with PHP >= 4.3.0 and safe
           mode enabled! */
        if ($_SERVER['PHP_AUTH_USER'] == "") {
            msg($this->getLang('nocreds'), -1);
            $this->success = false;
            return;
        }

        /* Load the config */
        $this->loadConfig();

        /* Set the config values */
        foreach (array("usernameregex", "emaildomain", "specialusers", "specialgroup") as $cfgvar) {
            $this->$cfgvar = $this->getConf("$cfgvar");
            if (!$this->$cfgvar) {
                 msg("Config error: \"$cfgvar\" not set!", -1);
                 $this->success = false;
                 return;
            }
        }
        if (preg_match('/^\/.*\/$/m', $this->usernameregex) == 0) {
            $this->usernameregex = '/'.$this->usernameregex.'/';
        }
        $this->specialusers = explode(" ", $this->specialusers);

        if ($active) {
            /* No support for logout in this auth plugin. */
            $this->cando['logout'] = false;
        }
    }

    /**
     * Check user+password
     *
     * @param   string $user the user name
     * @param   string $pass the clear text password
     * @return  bool
     */
    public function checkPass($user, $pass) {
        return ($user == $this->cleanUser($_SERVER['PHP_AUTH_USER']) && $pass == $_SERVER['PHP_AUTH_PW']);
    }

    /**
     * Return user info
     *
     * Returned info about the given user needs to contain
     * at least these fields:
     *
     * name string  full name of the user
     * mail string  email address of the user
     * grps array   list of groups the user is in
     *
     * @param   string $user the user name
     * @param   bool $requireGroups ignored, this plugin always returns groups
     * @return  array containing user data or false
     */
    public function getUserData($user, $requireGroups = true) {
        global $conf;

        $info['name'] = $user;
        $info['mail'] = $user."@".$this->emaildomain;
        $info['grps'] = array($conf['defaultgroup']);
        if (in_array($user, $this->specialusers)) {
            $info['grps'][] = $this->specialgroup;
        }

        return $info;
    }

    /**
     * Sanitize a given user name
     *
     * This function is applied to any user name that is given to
     * the backend.
     *
     * @param  string $user user name
     * @return string the cleaned user name
     */
    public function cleanUser($user) {
        if (preg_match($this->usernameregex, $user, $results)) {
            error_log("---");
            error_log("returning ".$results[0]);
            error_log("---");
            return $results[0];
        } else {
            return $user;
        }
    }
}

// vim:ts=4:sw=4:et:
