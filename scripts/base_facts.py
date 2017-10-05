#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
import sys



bash = "/bin/sh"

# Configuration Files
pathAnsible = "/etc/ansible"
configAll = "%s/group_vars/all" % (pathAnsible)
nodesInventory = "%s/inventory/nodes" % (pathAnsible)

# Error Log file ('/dev/null' by default)
errorLog = "/dev/null"


# Base Packages List by Package Manager 
basePackages = {}
basePackages['apt'] = ['bash', 'coreutils', 'grep', 'sed', 'gawk', 'net-tools', 'iproute', 'findutils', 'dmidecode', 'util-linux']
basePackages['conary'] = ['bash', 'coreutils', 'grep', 'sed', 'gawk', 'net-tools', 'iproute', 'findutils', 'dmidecode', 'util-linux']
basePackages['emerge'] = ['bash', 'coreutils', 'grep', 'sed', 'gawk', 'net-tools', 'iproute', 'findutils', 'dmidecode', 'util-linux'] 
basePackages['freebsd_pkg'] = ['bash', 'gsed', 'gawk', 'findutils', 'dmidecode']
basePackages['macports'] = ['bash', 'coreutils', 'grep', 'gsed', 'gawk', 'iproute', 'findutils', 'util-linux']
basePackages['openbsd_pkg'] = ['bash', 'gsed', 'gawk', 'findutils', 'dmidecode']
basePackages['pacman'] = ['bash', 'grep', 'sed', 'gawk', 'net-tools', 'iproute2', 'findutils', 'dmidecode', 'util-linux', 'xinetd']
basePackages['pkgutil'] = ['bash', 'coreutils', 'ggrep', 'gsed', 'gawk', 'findutils'] 
basePackages['slackpkg'] = ['bash', 'coreutils', 'grep', 'sed', 'gawk', 'net-tools', 'iproute2', 'findutils', 'dmidecode', 'util-linux']
basePackages['yum'] = ['bash', 'coreutils', 'grep', 'sed', 'gawk', 'net-tools', 'iproute', 'findutils', 'dmidecode', 'util-linux-ng']
basePackages['zypper'] = ['bash', 'coreutils', 'grep', 'sed', 'gawk', 'net-tools', 'iproute2', 'findutils', 'dmidecode', 'util-linux', 'python-xml']

# Munin Packages by Package Manager 
muninNodePackages = {}
muninNodePackages['apt'] = ['munin-node']
muninNodePackages['freebsd_pkg'] = ['munin-node']
muninNodePackages['openbsd_pkg'] = ['munin-node']
muninNodePackages['pacman'] = ['munin-node']
muninNodePackages['pkgutil'] = ['CSWmunin-common', 'CSWmunin-node']
muninNodePackages['yum'] = ['munin-node']
muninNodePackages['zypper'] = ['munin-node']

# Nagios NRPE by Package Manager
nagiosNrpePackages = {}
nagiosNrpePackages['apt'] = ['nagios-nrpe-server']
nagiosNrpePackages['emerge'] = ['nrpe']
nagiosNrpePackages['freebsd_pkg'] = ['nrpe-ssl', 'nagios-plugins']
nagiosNrpePackages['macports'] = ['nrpe', 'nagios-plugins']
nagiosNrpePackages['pacman'] = ['nrpe', 'nagios-plugins']
nagiosNrpePackages['pkgutil'] = ['CSWnrpe', 'CSWnagios-plugins']
nagiosNrpePackages['yum'] = ['nagios-nrpe', 'nagios-plugins-dhcp', 'nagios-plugins-disk', 'nagios-plugins-dns', 'nagios-plugins-http', 'nagios-plugins-file_age', 'nagios-plugins-ldap', 'nagios-plugins-load', 'nagios-plugins-log', 'nagios-plugins-mysql', 'nagios-plugins-ntp', 'nagios-plugins-oracle', 'nagios-plugins-perl', 'nagios-plugins-pgsql', 'nagios-plugins-ping', 'nagios-plugins-procs', 'nagios-plugins-rpc', 'nagios-plugins-smtp', 'nagios-plugins-snmp', 'nagios-plugins-ssh', 'nagios-plugins-swap', 'nagios-plugins-users']
#nagiosNrpePackages['zypper'] = ['nrpe', 'nagios-plugins-nrpe']




### Functions ###

def getShell():
    ret = subprocess.Popen("(bash --version > /dev/null && ((which bash >/dev/null && which bash) || (whereis -b bash|cut -d' ' -f1,2|cut -d' ' -f2) || (find /bin /sbin /usr/bin /usr/sbin /usr /opt -executable -name 'bash')) || (echo '/bin/sh')) 2>%s" % (errorLog), shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
    return ret.stdout.read().strip()


def path(command1, command2=''):
    if command1 != "" and command2 != "":
      ret = subprocess.Popen("(%s --version > /dev/null && ((which %s >/dev/null && which %s) || echo '%s') || ((which %s >/dev/null && which %s) || echo '%s')) 2>%s" % (command1, command1, command1, command1, command2, command2, command2, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    elif command1 != "":
      ret = subprocess.Popen("((which %s >/dev/null && which %s) || echo '%s') 2>%s" % (command1, command1, command1, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    else:
      ret=""

    return ret


def getPackageManager():
    # Getting Package Manager
    packageManager = subprocess.Popen("((%s --version >/dev/null && echo 'yum') || (%s --version >/dev/null && echo 'apt') || (%s --version >/dev/null && echo 'conary') || (%s --version >/dev/null && echo 'zypper') || (%s --version >/dev/null && echo 'pacman') || (%s --version >/dev/null && echo 'emerge') || ([ `%s -s` == 'FreeBSD' ] && echo 'freebsd_pkg') || ([ `%s -s` == 'OpenBSD' ] && echo 'openbsd_pkg') || (%s help >/dev/null && echo 'macports') || (%s >/dev/null && [ `%s -s` == 'SunOS' ] && echo 'pkgutil') || (%s >/dev/null && echo 'slackpkg') || (%s >/dev/null && echo 'installpkg') || echo 'unknown') 2>%s" % (path('yum'), path('apt-get'), path('conary'), path('zypper'), path('pacman'), path('emerge'), path('uname'), path('uname'), path('port'), path('pkgutil'), path('uname'), path('slackpkg'), path('installpkg'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    return packageManager


def show_packageManager():
    # Printing Package Manager 
    print "    \"packageManager\": \"%s\"," % (getPackageManager())


def show_basePackages():
    # Getting Base Packages by Package Manager 
    packManager = getPackageManager()

    print "    \"basePackages\": ["
    if packManager in basePackages:
      countPackages = 1
      for package in basePackages[packManager]:
        print "      \"%s\"%s" % (package, ("",",") [ countPackages < len(basePackages[packManager]) ]) 
        countPackages += 1

    print "    ],"


def show_repsYum():
    # Get reps label for EPEL & Rpmforge (YUM Package Manager)
    packManager = getPackageManager()
    if packManager == "yum":
      labelEpel = subprocess.Popen("(%s -il 'epel' /etc/yum.repos.d/*|xargs %s '^\[.*\]'|%s 's/\[//g'|%s 's/\]//g'|head -1) 2>%s" % (grep, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip() 
      labelRpmforge = subprocess.Popen("(%s -il 'rpmforge' /etc/yum.repos.d/*|xargs %s '^\[.*\]'|%s 's/\[//g'|%s 's/\]//g'|head -1) 2>%s" % (grep, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
      print "    \"labelEpel\": \"%s\"," % (labelEpel)
      print "    \"labelRpmforge\": \"%s\"," % (labelRpmforge)



def show_muninNode():
    # Munin Node

    # Getting Munin Node Packages by Package Manager
    packManager = getPackageManager()
    print "    \"packageMuninNode\": ["
    if packManager in muninNodePackages:
      countPackages = 1
      for package in muninNodePackages[packManager]:
        print "        \"%s\"%s" % (package, ("",",") [ countPackages < len(muninNodePackages[packManager]) ])
        countPackages += 1

    print "    ],"

    # Getting munin-node.conf file
    confFile = subprocess.Popen("(%s /etc/munin /etc /usr -name 'munin-node.conf'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "    \"confFileMuninNode\": \"%s\"," % (confFile)

    if confFile != "":
      # Getting Munin Node daemon

      # Looking for in /etc/init.d /etc/rc.d and /usr/local/etc/rc.d
      daemon = subprocess.Popen("(%s -L /etc/init.d /etc/rc.d /usr/local/etc/rc.d -name 'munin-node'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      if daemon == "":
	# Looking for in /etc/init.d /etc/rc.d and /usr/local/etc/rc.d
        daemon = subprocess.Popen("(%s -L /etc/init.d /etc/rc.d /usr/local/etc/rc.d -name '*munin*node*'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      if daemon == "":
	# Looking for in /etc/xinetd.d
	xinetd = subprocess.Popen("(%s -L /etc/xinetd.d -name '*munin*node*'|head -1|%s 's/.*\///') 2>%s" % (find, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	if xinetd != "":
	  daemon = "xinetd"

      if daemon == "":
	# Looking for Munin Node service
        daemon = subprocess.Popen("(%s /usr/lib /usr/lib64 -name 'munin-node.service'|head -1|%s 's/.*\///'|cut -d'.' -f1) 2>%s" % (find, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      if daemon == "":
	# Looking for Munin Node service
	daemon = subprocess.Popen("(%s /usr/lib /usr/lib64 -name '*munin*node*.service'|head -1|%s 's/.*\///'|cut -d'.' -f1) 2>%s" % (find, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      # Looking for in /etc/inetd.conf      
      if daemon == "":
	inetd = subprocess.Popen("(%s -i '^munin*node*' /etc/inetd.conf | head -1) 2>%s" % (grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	if inetd != "":
	  #daemon = subprocess.Popen("(%s -L /etc/init.d -name 'inetd'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  daemon = "inetd"

      if daemon == "":
        # Looking for with SMF commands (Solaris)
        daemon = subprocess.Popen("(%s -? >/dev/null && (%s|%s -i 'munin*node'|%s -i '^online'|tr '\t' ' '|tr -s ' '|cut -d' ' -f3)) 2>%s" % (path('svcs'), path('svcs'), grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    else:
      daemon = ""

    print "    \"daemonMuninNode\": \"%s\"," % (daemon)


def show_nagiosNrpe():
    # Nagios NRPE

    # Getting Nagios NRPE Packages by Package Manager
    packManager = getPackageManager()
    print "    \"packageNagiosNrpe\": ["
    if packManager in nagiosNrpePackages: 
      countPackages = 1
      for package in nagiosNrpePackages[packManager]:
        print "      \"%s\"%s" % (package, ("",",") [ countPackages < len(nagiosNrpePackages[packManager]) ])
        countPackages += 1

    print "    ],"

    # Getting nrpe.cfg file
    confFile = subprocess.Popen("(%s /etc/nagios /etc /usr -name 'nrpe.cfg'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "    \"confFileNagiosNrpe\": \"%s\"," % (confFile)

    if confFile != "":
      # Getting Nagios NRPE daemon

      # Looking for in /etc/init.d /etc/rc.d and /usr/local/etc/rc.d 
      daemon = subprocess.Popen("(%s -L /etc/init.d /etc/rc.d /usr/local/etc/rc.d -name 'nrpe'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      if daemon == "":
	# Looking for in /etc/init.d /etc/rc.d and /usr/local/etc/rc.d
	daemon = subprocess.Popen("(%s -L /etc/init.d /etc/rc.d /usr/local/etc/rc.d -name '*nrpe*'|head -1) 2>%s" % (find, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      if daemon == "":
	# Looking for in /etc/xinetd
	xinetd = subprocess.Popen("(%s -L /etc/xinetd.d -name '*nrpe*'|head -1|%s 's/.*\///') 2>%s" % (find, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	if xinetd != "":
	  daemon = "xinetd"

      if daemon == "":
	# Looking for Nagios NRPE service
	daemon = subprocess.Popen("(%s /usr/lib /usr/lib64 -name 'nrpe.service'|head -1|%s 's/.*\///'|cut -d'.' -f1) 2>%s" % (find, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	
      if daemon == "":
        # Looking for Nagios NRPE service
        daemon = subprocess.Popen("(%s /usr/lib /usr/lib64 -name '*nrpe*.service'|head -1|%s 's/.*\///'|cut -d'.' -f1) 2>%s" % (find, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

      if daemon == "":
	# Looking for in /etc/inetd.conf
        inetd = subprocess.Popen("(%s -i '^nrpe*' /etc/inetd.conf | head -1) 2>%s" % (grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        if inetd != "":
	  daemon = "inetd"

      if daemon == "":
	# Looking for with SMF commands (Solaris)
	daemon = subprocess.Popen("(%s -? >/dev/null && (%s|%s -i 'nrpe'|%s -i '^online'|tr '\t' ' '|tr -s ' '|cut -d' ' -f3)) 2>%s" % (path('svcs'), path('svcs'), grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    else:
      daemon = ""

    print "    \"daemonNagiosNrpe\": \"%s\"," % (daemon)

    if confFile != "":
      # Getting Nagios NRPE plugins directory
      # Looking for in config File
      pluginsPath = subprocess.Popen("(%s -i '^command' %s |cut -d'=' -f2|cut -d' ' -f1|%s -i check|head -1|%s 's/\\(.*\\)\\/.*/\\1/') 2>%s" % (grep, confFile, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
      if pluginsPath == "":
        # Looking for a directory with 'nagios' and 'plugins' words
        pluginsPath = subprocess.Popen("(%s /usr /lib -type d -name '*plugins*'|%s -i '/*nagios*/'|head -1) 2>%s" % (find, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    else:
      pluginsPath = ""

    print "    \"pluginsPathNagiosNrpe\": \"%s\"," % (pluginsPath)


def show_pythonVersion():
    # Getting Python Version 
    pythonVersion = sys.version[0:3]

    print "    \"pythonVersion\": %s," % (pythonVersion)


def show_cabecera():
    print "{"
    print "  \"ansible_facts\": {"


def show_pie():
    print "    \"base_facts\": \"true\","
    print "    \"changed\": false"
    print "  }"
    print "}" 


def main():

    show_cabecera()

    # Looking for commands path
    global awk, bash, find, grep, sed
    awk = path('gawk','awk')
    bash = getShell()
    find = path('gfind','find')
    grep = path('ggrep','grep')
    sed = path('gsed','sed')

    show_packageManager()
    show_basePackages()
    show_repsYum()
    show_muninNode()
    show_nagiosNrpe()
    #show_pythonVersion()

    show_pie()



if __name__ == '__main__':
    main()

