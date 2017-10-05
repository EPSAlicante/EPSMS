#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess


bash = "/bin/sh"

# Error Log file ('/dev/null' by default)
errorLog = "/dev/null"



### Functions ###

def getShell():
    ret = subprocess.Popen("(bash --version > /dev/null && ((which bash >/dev/null && which bash) || (whereis -b bash|cut -d' ' -f1,2|cut -d' ' -f2|grep -v '^bash:') || ((find /bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin /usr/gnu/bin /usr/gnu/sbin /opt/csw/bin /opt/csw/sbin -name 'bash') || (echo '/bin/sh'))|head -1)) 2>%s" % (errorLog), shell=True, executable='/bin/sh', stdout=subprocess.PIPE).stdout.read().strip()

    if ret == "":
      ret = "/bin/sh"

    return ret


def path(command1, command2=''):
    if command1 != "" and command2 != "":
      ret = subprocess.Popen("(%s --version > /dev/null && ((which %s >/dev/null && which %s) || (whereis -b %s|cut -d' ' -f1,2|cut -d' ' -f2|grep -v '^%s:') || ((find /bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin /usr/gnu/bin /usr/gnu/sbin /opt/csw/bin /opt/csw/sbin -name '%s') || (echo '%s'))|head -1) || ((which %s >/dev/null && which %s) || (whereis -b %s|cut -d' ' -f1,2|cut -d' ' -f2|grep -v '^%s:') || ((find /bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin /usr/gnu/bin /usr/gnu/sbin /opt/csw/bin /opt/csw/sbin -name '%s'))|head -1 || (echo '%s'))) 2>%s" % (command1, command1, command1, command1, command1, command1, command1, command2, command2, command2, command2, command2, command2, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    elif command1 != "":
      ret = subprocess.Popen("((which %s >/dev/null && which %s) || (whereis -b %s|cut -d' ' -f1,2|cut -d' ' -f2|grep -v '^%s:') || ((find /bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin /usr/gnu/bin /usr/gnu/sbin /opt/csw/bin /opt/csw/sbin -name '%s') || (echo '%s'))|head -1) 2>%s" % (command1, command1, command1, command1, command1, command1, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    else:
      ret=""

    return ret


def show_paths():
    # Getting paths
    print "    \"path\": {" 
    print "      \"apt-get\": \"%s\"," % (path('apt-get'))
    print "      \"awk\": \"%s\"," % (path('gawk','awk'))
    print "      \"bash\": \"%s\"," % (bash)
    print "      \"conary\": \"%s\"," % (path('conary'))
    print "      \"emerge\": \"%s\"," % (path('emerge'))
    print "      \"equery\": \"%s\"," % (path('equery'))
    print "      \"find\": \"%s\"," % (path('gfind','find'))
    print "      \"grep\": \"%s\"," % (path('ggrep','grep'))
    print "      \"installpkg\": \"%s\"," % (path('installpkg'))
    print "      \"netstat\": \"%s\"," % (path('netstat'))
    print "      \"pacman\": \"%s\"," % (path('pacman'))
    print "      \"passwd\": \"%s\"," % (path('passwd'))
    print "      \"pkg\": \"%s\"," % (path('pkg'))
    print "      \"pkg_add\": \"%s\"," % (path('pkg_add'))
    print "      \"pkg_info\": \"%s\"," % (path('pkg_info'))
    print "      \"pkgutil\": \"%s\"," % (path('pkgutil'))
    print "      \"port\": \"%s\"," % (path('port'))
    print "      \"sed\": \"%s\"," % (path('gsed','sed'))
    print "      \"service\": \"%s\"," % (path('service'))
    print "      \"slackpkg\": \"%s\"," % (path('slackpkg'))
    print "      \"ssh-keygen\": \"%s\"," % (path('ssh-keygen'))
    print "      \"svcadm\": \"%s\"," % (path('svcadm'))
    print "      \"svcs\": \"%s\"," % (path('svcs'))
    print "      \"systemctl\": \"%s\"," % (path('systemctl'))
    print "      \"uname\": \"%s\"," % (path('uname'))
    print "      \"yum\": \"%s\"," % (path('yum'))
    print "      \"zypper\": \"%s\"" % (path('zypper'))
    print "    },"


def show_cabecera():
    print "{"
    print "  \"ansible_facts\": {"


def show_pie():
    print "    \"changed\": false"
    print "  }"
    print "}" 


def main():


    global bash 
 
    bash = getShell()

    show_cabecera()

    show_paths()

    show_pie()



if __name__ == '__main__':
    main()

