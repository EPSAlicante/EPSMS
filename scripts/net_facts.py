#!/usr/bin/python

import subprocess
import socket
import paramiko
import os
import sys
import re
import time


# Configuration Files
#pathAnsible = os.path.abspath(os.path.dirname(sys.argv[0]))
pathAnsible = "/etc/ansible"
configAll = "%s/group_vars/all" % (pathAnsible) 
nodesInventory = "%s/inventory/nodes" % (pathAnsible)
winNodesInventory = "%s/inventory/winNodes" % (pathAnsible)

bash = "/bin/sh"

# Error Log file ('/dev/null' by default)
errorLog = "/dev/null"


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


def getValueFromFile(file, label, separator):
    value = ""
    if os.access(file, os.R_OK):
      f = open(file, "r")
      for line in f:
        if line.startswith(label+':'):
          value = line.split(separator,1)[1].strip() 

    return value


def sshUser():

    user = ""
    # Get global value
    user = getValueFromFile(configAll, "sshUserNodes", ":")
    
    return  user 


def winCheck():

    check = ""
    # Get global value
    check = getValueFromFile(configAll, "winNodes", ":") 

    return check


def winUser():

    user = ""
    # Get global value
    user = getValueFromFile(configAll, "winUserNodes", ":")

    return  user


def winPasswd():
    passwd = ""
    # Get global value
    passwd = getValueFromFile(configAll, "winPasswdNodes", ":")

    return passwd


def sshAccess(IP, user):
    try:
      s = paramiko.SSHClient()
      s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      paramiko.util.log_to_file("/dev/null")
      s.connect(IP, username=user)

    except KeyboardInterrupt:
      return False
    except:
      return False

    s.close()
    return True


def winAccess(IP, user):
    passwd = winPasswd()

    try:
      nameHost = subprocess.Popen("%s -U %s%%%s //%s 'Select Name from Win32_ComputerSystem' >/dev/null 2>%s && echo 'OK'" % (path('wmic'),user,passwd,IP,errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
      if nameHost == "OK":
	return True
      else:
	return False

    except:
      return False

    return True


def isNode(IP):
    value = False
    try:
      if os.access(nodesInventory, os.R_OK):
        f = open(nodesInventory, "r")
        for line in f:
          if line.startswith(IP) or line.startswith(socket.getfqdn(IP).lower()):
            value = True

    except:
      value = False

    return value


def isWinNode(IP):
    value = False
    try:
      if os.access(winNodesInventory, os.R_OK):
        f = open(winNodesInventory, "r")
        for line in f:
          if line.startswith(IP) or line.startswith(socket.getfqdn(IP).lower()):
            value = True

    except:
      value = False

    return value


def sshHostkey(IP):
    # Get ssh Hostkey
    command = "(%s --host-timeout=30 %s --script ssh-hostkey|grep 'ssh-hostkey:') 2>/dev/null" % (path('nmap'),IP)
    hostkey = subprocess.Popen("%s" % (command), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()

    if hostkey != "":
      hostkey = hostkey.split(':',1)[1].strip()

    return hostkey 


def getAccess(IP, sshPort, minPort):
    access = "ping"

    # Trying ping access to IP 
    pingCheck = subprocess.Popen("%s -c 1 %s > /dev/null; echo $?" % (path('ping'),IP), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    if int(pingCheck.stdout.read()) == 0:
      # Ping Access to IP 
      access = "ping"
    elif sshPort == 1:
      # SSH access to IP
      access = "22"
    else:
      # Access to IP by minPort 
      access = minPort

    return access 


def getType(IP, sshPort, winPort):
    # Host type (outsider, node or winNode)
    type = "outsider"

    # Type (node-winNode-outsider)
    if sshPort == 1:
      # Get sshUser value
      user = sshUser()
      if sshAccess(IP, user) == True:
        try:
          pingCheck = subprocess.Popen("(%s 30s ansible all -i \"%s\", -u %s -s -T 10 -m ping|grep pong|wc -l) 2>/dev/null" % (path('timeout'),IP,user), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
          if int(pingCheck.stdout.read()) > 0:
            type = "node"

        except:
	  type = "outsider"

    # Check Windows nodes
    if winCheck() == "y":
      # Type (winNode-outsider)
      if type == "outsider" and winPort == 1:
        # Get winUser value
        user = winUser()
        if winAccess(IP, user) == True:
          type = "winNode"


    return type


def showTCP(IP):
    sshPort = 0
    winPort = 0

    contTCP = 1
    command = "(%s -min-parallelism 100 -sS \"%s\" --host-timeout=30 --min-hostgroup=10 -v0|grep tcp|grep open|cut -d'/' -f1) 2>/dev/null" % (path('nmap'),IP)
    listTCP = subprocess.Popen("%s" % (command), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	
    lines = listTCP.stdout.readlines()
    maxTCP = len(lines)
    minPort = "" 
     
    if maxTCP > 0:
      print "        \"tcp\": ["

      for line in lines:
        portTCP = line.strip() 
	if contTCP == 1:
	  minPort = portTCP

        if portTCP.isdigit():
          if contTCP < maxTCP:
            print "          \"%s\"," % (portTCP)
          else:
            print "          \"%s\"" % (portTCP)

          # sshPort is active
          if portTCP == "22":
            sshPort = 1

	  # winPort is active
	  if portTCP == "135":
	    winPort = 1

          contTCP += 1

      print "        ],"

    # Type (outsider-node)
    type = getType(IP, sshPort, winPort)

    # If IP is an outsider and it was a node, try again (ssh problems probably)
    if type == "outsider" and (isNode(IP) or (winCheck() and isWinNode(IP))):
      cont = 1
      while type == "outsider" and cont<=5: 
        time.sleep(10*cont)
  	cont += 1
        type = getType(IP, sshPort, winPort)

    print "        \"type\": \"%s\"," % (type)

    # Nagios access (ping or TCP port)
    print "        \"access\": \"%s\"" % (getAccess(IP,sshPort,minPort)) 


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

    subnetsFile = "/tmp/net_facts_subnets.tmp"
    if os.access(subnetsFile, os.R_OK):
      f = open(subnetsFile, "r")
      subnetsNmap = f.read().replace('\n',' ')
       
    else:
      if len(sys.argv) > 1:
        subnetsNmap = " ".join(sys.argv[1:])
      else:
        print >> sys.stderr, "Subnets needed by arguments or the subnets file %s" % (subnetsFile)
        sys.exit(1)
 
    excludeFile = "/tmp/net_facts_exclude.tmp"
    excludeNmap = ""
    if os.access(excludeFile, os.R_OK):
      f = open(excludeFile, "r")
      excludeNmap = f.read().strip()
      if excludeNmap != "":
        excludeNmap = "--exclude " + excludeNmap.replace('\n',',') 

    command = "(%s -min-parallelism 100 -n -sP %s %s | grep \"scan report\" | cut -d' ' -f5) 2> /dev/null" % (path('nmap'),subnetsNmap,excludeNmap)
    listHosts = subprocess.Popen("%s" % (command), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    linesHosts = listHosts.stdout.readlines()

    show_cabecera()
    print "    \"network\": ["
    # Save hosts and hostnames removing repeated
    usedHosts = {}
    for line in linesHosts:
      host = line.strip()
      hostname = socket.getfqdn(host).lower()
      usedHosts[hostname] = host

    maxHosts = len(usedHosts)
    contHosts = 1
    for name, IP in sorted(usedHosts.iteritems()):
      print "      {"
      print "        \"IP\": \"%s\"," % (IP)
      print "        \"name\": \"%s\"," % (name)
      print "        \"contHosts\": \"%s\"," % (contHosts)
      print "        \"maxHosts\": \"%s\"," % (maxHosts)
      print "        \"sshUser\": \"%s\"," % (sshUser())
      print "        \"sshHostkey\": \"%s\"," % (sshHostkey(IP))
      print "        \"winCheck\": \"%s\"," % (winCheck())
      # TCP ports
      showTCP(IP)
      if contHosts < maxHosts:
        print "      }," 
      else: 
        print "      }"
      
      contHosts += 1
      
    print "    ],"
    show_pie()



if __name__ == '__main__':
    main()

