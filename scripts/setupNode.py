#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
import socket
import sys
import os

# Configuration Files
pathAnsible = "/etc/ansible"
pathAnsibleLibrary= "/usr/share/ansible"
configAll = "%s/group_vars/all" % (pathAnsible)
nodesInventory = "%s/inventory/nodes" % (pathAnsible)

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
      nameDNS = socket.getfqdn(IP)
    except:
      return IP 

    return nameDNS.lower()


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

    if len(sys.argv) == 3 or len(sys.argv) == 4:
      node = sys.argv[1]
      user = sys.argv[2]
      if len(sys.argv) == 4:
	uid = sys.argv[3]
      else:
	uid = "default"
    else:
        print >> sys.stderr, "%s host remoteUser [uid] ('host' can be name or IP)" % (sys.argv[0])
        sys.exit(1)
 
    # Check if argument 'host' is IP or name
    if checkIP(node):
      node = IPtoName(node)
 
    # Create inventory file for 'host' in /tmp
    inventoryTmp = "/tmp/inventory" 
    fileInv = open(inventoryTmp, 'w')
    fileInv.write("[newNode]\n") 
    fileInv.write("%s createUser=%s\n" % (node,user))
    fileInv.write("%s uidUserValue=%s\n" % (node,uid))
    fileInv.write("%s hostAnsibleValue=%s\n" % (node,getValueFromFile(configAll,'hostAnsible',':')))
    fileInv.write("%s pathAnsibleValue=%s\n" % (node,pathAnsible))
    fileInv.write("%s pathAnsibleLibraryValue=%s\n" % (node,pathAnsibleLibrary))
    fileInv.close()
     
    try:
      subprocess.call("ansible-playbook -i %s %s/scripts/setupLocal.yml --connection=local" % (inventoryTmp,pathAnsible), shell=True, executable='%s' % (bash))
      print
      print "Now you're connecting to '%s' with user 'root' by SSH..." % (node)
      subprocess.call("ansible-playbook -i %s %s/scripts/setupNode.yml -u root -k" % (inventoryTmp,pathAnsible), shell=True, executable='%s' % (bash))
    except KeyboardInterrupt:
      print "Interrupted"

    # Checking Access without password
    print "Checking ansible access to %s with user %s..." % (node,user)
    try:
      retCode = subprocess.call("timeout 30s ansible all -i %s -u %s -s -T 30 -m shell -a 'ls /root >/dev/null'" % (inventoryTmp,user), shell=True, executable='%s' % (bash))
    except KeyboardInterrupt:
      retCode = 1

    # Remove Temp Inventory
    os.remove(inventoryTmp)
    if retCode == 0:
      print "Host '%s' is accesible by ansible with user '%s'." % (node,user) 
      sys.exit(0)
    else:
      print >> sys.stderr, "Error: host '%s' is not accesible by ansible with user '%s'." % (node,user) 
      sys.exit(2)

    


if __name__ == '__main__':
    main()

