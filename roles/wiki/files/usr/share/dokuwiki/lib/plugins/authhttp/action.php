<?php
/**
 * DokuWiki HTTP authentication plugin
 * https://www.dokuwiki.org/plugin:authhttp
 *
 * This is authhttp's action plugin which
 * a.) skips the 'login' action as it does not make sense with HTTP
 *     authentication.
 * b.) modifies DokuWiki's register form so that
 *     i.) the username is hard-coded to match the username from the
 *         HTTP authentication.
 *     ii.) the password text fields are replaced by hidden fields with
 *          a random password that won't do any harm.
 *
 * All of this code ONLY applies when DokuWiki's configured auth plugin is authsplit
 * (https://www.dokuwiki.org/plugin:authsplit) and authhttp is its primary auth plugin.
 * If authhttp is used on its own (ie. as DokuWiki's auth plugin), users will never
 * see a login or a register screen anyway.
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

class action_plugin_authhttp extends DokuWiki_Action_Plugin {
    public function __construct() {
        global $conf, $active;

        if ($active) {
            /* We register an event handler to skip the login action below, but
               we also don't want the template to show a 'login' link in the
               first place.

               DokuWiki has no capability setting for 'login', so we need a
               little hack that pretends the admin disabled the login action
               himself. */
            $disableactions = explode(',', $conf['disableactions']);
            $disableactions = array_map('trim', $disableactions);
            if (!in_array('login', $disableactions)) {
                $disableactions[] = 'login';
            }
            $conf['disableactions'] = implode(',', $disableactions);

            /* We also don't want DokuWiki to generate passwords on its own and
               mail them to the users upon registration. We need to use the same
               hack as above, pretending the admin disabled password generation
               himself. */
            $conf['autopasswd'] = 0;
        }
    }

    /**
     * Register the event handlers
     */
    function register(Doku_Event_Handler $controller){
        global $active;

        if ($active) {
            $controller->register_hook('ACTION_ACT_PREPROCESS',
                                       'AFTER',
                                       $this,
                                       'skip_login_action',
                                       NULL);

            $controller->register_hook('HTML_REGISTERFORM_OUTPUT',
                                       'BEFORE',
                                       $this,
                                       'modify_register_form',
                                       NULL);
        }
    }

    /**
     * Event handler to skip the 'login' action
     */
    function skip_login_action(&$event, $param) {
        /* Some actions handled in inc/actions.php:act_dispatch() result in $ACT
           being modified to 'login', eg. 'register'. */
        if ($event->data == 'login') {
            /* With HTTP authentication, there is no sense in showing a login form,
               so we directly redirect to a 'show' action instead. By using
               act_redirect() instead of modifying $event->data, we make sure
               DokuWiki's entire auth logic can work, which is eg. required so that
               after a user's registration he gets logged in automatically. */
            act_redirect($ID, 'show');
        }
    }

    /**
     * Event handler to modify the registration form
     */
    function modify_register_form(&$event, $param) {
        /* Hard-code the HTTP authentication user name as login name to be registered as
           registering as anyone else than the already externally authenticated user does
           not make much sense. */
        $pos = $event->data->findElementByAttribute('name','login');
        if (!$pos)
            return;
        $elem = $event->data->getElementAt($pos);
        $elem['value'] = $_SERVER['PHP_AUTH_USER'];
        $elem['readonly'] = 'readonly';
        $event->data->replaceElement($pos, $elem);

        /* We do not want DokuWiki to auto-generate a password and mail it to the user.
           Then, however, inc/auth.php's register() will insist on a non-null password,
           so we supply a random one in hidden form fields. As this code only runs when
           both authhttp AND authsplit are active, the password won't end up anywhere
           since authhttp is the primary auth plugin in that case and does not offer the
           modPass capability. */
        $pwd = auth_pwgen();
        foreach (array('pass', 'passchk') as $name) {
            $pos = $event->data->findElementByAttribute('name', $name);
            $event->data->replaceElement($pos, NULL);
            $event->data->addHidden($name, $pwd);
        }
    }
}
