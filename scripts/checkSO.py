#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
import sys
import os

# Configuration Files
pathAnsible = "/etc/ansible"
OSFile = "%s/group_vars/CentOS-6" % (pathAnsible)


bash = "/bin/sh"

# Error Log file ('/dev/null' by default)
errorLog = "/dev/null"


def getShell():
    ret = subprocess.Popen("(bash --version > /dev/null && ((which bash >/dev/null && which bash) || (whereis -b bash|cut -d' ' -f1,2|cut -d' ' -f2) || (find /bin /sbin /usr/bin /usr/sbin /usr /opt -executable -name 'bash')) || (echo '/bin/sh')) 2>%s" % (errorLog), shell=True, executable='/bin/sh', stdout=subprocess.PIPE)
    return ret.stdout.read().strip()


def checkIP(IP):
    try:
      socket.inet_aton(IP)
      return True
    except:
      return False


def IPtoName(IP):
    try:
      nameDNS = socket.gethostbyaddr(IP)
    except:
      return IP

    return nameDNS[0].lower()


def getValueFromFile(file, label, separator):
    value = ""
    if os.access(file, os.R_OK):
      f = open(file, "r")
      for line in f:
        if line.startswith(label):
          value = line.split(separator,1)[1].strip()

    return value


def main():

    global bash

    bash = getShell()

    if len(sys.argv) == 4:
      node = sys.argv[1]
      user = sys.argv[2]
      role = sys.argv[3]
    else:
      print >> sys.stderr, "Error!!! Usage: %s host user role" % (sys.argv[0])
      print >> sys.stderr, "Parameter 'host' coud be name or IP"
      print >> sys.stderr, "Parameter 'user' is the user to connect to host"
      print >> sys.stderr, "Parameter 'role' is an Ansible task (a file with yml extension)"
      sys.exit(1)

    # Check if argument 'host' is IP or name
    if checkIP(node):
      node = IPtoName(node)

    # Check role
    fileRole = "%s/%s.yml" % (pathAnsible,role)
    if not os.access(fileRole, os.R_OK):
      print >> sys.stderr, "Error!!! Bad role, %s not found!!!" % (fileRole)
      sys.exit(2)
    
    # Getting Operating System and version
    cadSO = subprocess.Popen("ansible all -i \"%s\", -u %s -s -T 10 -m setup 2>/dev/null|grep \\\"ansible_distribution\\\":|cut -d ':' -f2|cut -d',' -f1" % (node, user), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    cadVersion = subprocess.Popen("ansible all -i \"%s\", -u %s -s -T 10 -m setup 2>/dev/null|grep \\\"ansible_distribution_version\\\":|cut -d ':' -f2|cut -d',' -f1" % (node, user), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    SO = cadSO.stdout.read().strip().strip('"')
    version = cadVersion.stdout.read().strip().strip('"').split(".")[0]
    retCode = subprocess.call("grep \"%s-%s\" %s >/dev/null 2>/dev/null" % (SO,version,fileRole), shell=True, executable='%s' % (bash))
    if retCode == 0:
      print "OK. SO %s-%s found in %s" % (SO,version,fileRole)
    else:
      print >> sys.stderr, "Error!!! SO %s-%s not found in %s" % (SO,version,fileRole)
      sys.exit(3)

    # Getting LANG
    cadLANG = subprocess.Popen("ansible all -i \"%s\", -u %s -s -T 10 -m setup 2>/dev/null|grep \\\"LANG\\\":|tail -1|cut -d ':' -f2|cut -d ',' -f1" % (node, user), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    lang = cadLANG.stdout.read().strip().strip('"')
    if "UTF-8" in lang.upper():
      print "OK. LANG: UTF-8 found"
    else:
      print >> sys.stderr, "Error!!! LANG: UTF-8 not found in '%s'" % (lang)
      sys.exit(4)

    # Checking EPEL repository
    labelEpel = getValueFromFile(OSFile, 'labelEpel:', ':')
    cadEPEL = subprocess.Popen("((ansible all -i \"%s\", -u %s -s -T 30 -m shell -a 'yum repolist \"%s\"|grep \"^repolist\"|cut -d \":\" -f2|tr -d \" \"|grep -v \"^0\$\"') >/dev/null 2>/dev/null && echo 'OK') || echo 'no'" % (node, user, labelEpel), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    epel = cadEPEL.stdout.read().strip()
    if epel == "OK":
      print "OK. EPEL: repository '%s' found and enabled" % (labelEpel)
    else:
      print >> sys.stderr, "Error!!! EPEL: repository '%s' not found or not enabled" % (labelEpel)
      sys.exit(5)

    # Checking SELinux 
    cadSelinux = subprocess.Popen("((ansible all -i \"%s\", -u %s -s -T 30 -m shell -a 'sestatus|grep \"^SELinux status:\"') 2>/dev/null|grep '^SELinux status:'|cut -d ':' -f2|tr -d ' ') || echo ''" % (node, user), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    selinux = cadSelinux.stdout.read().strip()
    if selinux == "disabled":
      print "SELinux: %s" % (selinux)
    else:
      print "SELinux: %s (be carefull, could be problems with output connections)" % (selinux) 
    sys.exit(0)




if __name__ == '__main__':
    main()


