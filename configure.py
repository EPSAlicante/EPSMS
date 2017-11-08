#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
import socket
import struct
import sys
import glob
import shutil
import readline
import os
import datetime


# Configuration Files
pathAnsible = "/etc/ansible"
configFile = "%s/config_files/main.conf" % (pathAnsible)
configExtra = "%s/config_files/extra.conf" % (pathAnsible)

# Production File
productionFile = "%s/group_vars/all" % (pathAnsible)
productionFileTmp = "%s.tmp" % (productionFile)

# Inventory Files
inventoryAnsible = "%s/inventory/ansible" % (pathAnsible)
inventoryMysql = "%s/inventory/mysql" % (pathAnsible)
inventoryWeb = "%s/inventory/web" % (pathAnsible)
inventoryMunin = "%s/inventory/munin" % (pathAnsible)
inventoryNagios = "%s/inventory/nagios" % (pathAnsible)
inventoryOpenvas = "%s/inventory/openvas" % (pathAnsible)
inventoryGrafana = "%s/inventory/grafana" % (pathAnsible)
inventoryServers = "%s/inventory/servers" % (pathAnsible)
inventoryNodes = "%s/inventory/nodes" % (pathAnsible)
inventoryWinNodes = "%s/inventory/winNodes" % (pathAnsible)

# Frequency Range
frequencyRangeMinutes = "5 6 10 12 15 20 30 60 120 180 240 360 480 720 1440"
frequencyRangeHours = "1 2 3 4 6 8 12 24"
frequencyRangeMonths = "1 2 3 4 6 12"

# Max Errors
maxErrors = 3



def checkIP(IP,localhost=""):
    print "Checking IP (%s) syntax..." % (IP)
    if localhost != "localhost" and IP == "127.0.0.1":
      print >> sys.stderr, "Loopback address not valid. Please check '/etc/hosts' and '/etc/sysconfig/network' files and reboot"
      return False
    try:
      socket.inet_aton(IP)
      return True
    except:
      return False


def checkNet(subnet):
    print "Checking subnet (%s) syntax..." % subnet
    cad = subnet.split('/')
    if len(cad) == 2:
      if checkIP(cad[0]) == True:
	try:
          if int(cad[1]) >0 and int(cad[1]) <= 32:
            return True
        except:
	    return False
      else:
	return False
    else:
      return False 


def IPInNetworks(IP,subnets):
    print "Checking IP in subnets (%s)..." % subnets
    ipaddr = struct.unpack('!L',socket.inet_aton(IP))[0]
    arr = subnets.split(' ')
    for net in arr:
      netaddr,bits = net.split('/')
      netmask = struct.unpack('!L',socket.inet_aton(netaddr))[0] & ((2L<<int(bits)-1) - 1)

      if ipaddr & netmask == netmask:
        return True 

    return False 


def IPInList(IP,list):
    print "Checking IP in list (%s)..." % list 
    arr = list.split(' ')
    if IP in arr:  
        return True
    else:
	return False

    return False


def accessIP(IP, remoteUser):
    print "Checking access by Ansible..."

    try:
      retCode = subprocess.call("timeout 30s ansible all -i \"%s\", -u %s -s -T 10 -m ping" % (IP,remoteUser), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)
    except KeyboardInterrupt:
      retCode = 1

    if retCode == 0:
      return True
    else:
      return False


def enforcingSELinux(IP, remoteUser):
    print "Checking SELinux (enforcing) on %s..." % (IP)
    print

    try:
      retCode = subprocess.call("timeout 30s ansible all -i \"%s\", -u %s -s -T 10 -m shell -a '((/usr/sbin/sestatus|grep -i \"^SELinux status:\"|grep -i enabled) && (/usr/sbin/sestatus|grep -i \"^Current mode:\"|grep -i \"enforcing\")) >/dev/null 2>/dev/null'" % (IP,remoteUser), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)
    except KeyboardInterrupt:
      retCode = 1 

    if retCode == 0:
      return True
    else:
      return False


def IPtoName(IP):
    try:
      nameDNS = socket.getfqdn(IP)
    except:
      return IP 

    return nameDNS.lower()


def checkFQDN(IP):
    print "Checking FQDN of (%s) ..." % (IP)
    try:
      nameFQDN = socket.getfqdn(IP)
      if nameFQDN != IP and "." in nameFQDN:
	return True 
    except:
      return False

    return False


def checkTime(cadTime):
    try:
	if len(cadTime) == 5:
          datetime.datetime.strptime(cadTime, '%H:%M')
	  return True
	else:
	  return False
    except ValueError:
        return False 


def checkFrequency(value,range):
    # Checking frequency
    rangeList = range.split(' ')
    if value in rangeList:
	return True
    else:
	return False
 

def question(cad, default, countErrors):
    correct = False
    count = 0
    if default.lower().strip() == "y" or default.lower().strip() == "n":
      defValue = default.lower().strip()
    else:
      defValue = "y"
    if countErrors > 0:
      maxErrors = countErrors
    else:
      maxErrors = 3

    while not correct:
      inputValue = raw_input_def("%s (y/n) " % (cad), "%s" % (defValue))
      if inputValue.lower().strip() == 'y' or inputValue.lower().strip() == 'n':
        correct = True
        answer = inputValue.lower().strip()
	print
        continue
      else:
        print >> sys.stderr, "ERROR: value %s is not valid. Values (y/n)" % (inputValue.strip())

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        return "n" 

    return answer


def getValueFromFile(file, label, separator):
    value = ""
    if os.access(file, os.R_OK):
      f = open(file, "r")
      for line in f:
	if line.startswith(label):
          value = line.split(separator,1)[1].strip() 

    return value


def writeVariableToFile(file, comment, variable ):
    if os.access(file, os.W_OK):
      f = open(file, "a")
      f.write("\n")
      f.write("%s\n" % (comment))
      f.write("%s\n" % (variable))

      return True
    else:
      return False


def raw_input_def(prompt, default):
    def pre_input_hook():
        readline.insert_text(default)
        readline.redisplay()

    readline.set_pre_input_hook(pre_input_hook)
    try:
      return raw_input(prompt)
    finally:
      readline.set_pre_input_hook(None)




def main():

  try:

    # Clear screen
    os.system("clear")
    # System configuration
    print "#######################################"
    print "  System Configuration and Deployment "
    print "#######################################"
    print

    # Errors Message
    msgErrors = ""

    # Getting local Hostname
    try:
      var_localHostname = socket.gethostname()
    except:
      var_localHostname = ""

    # Getting local IP
    try:
      var_localIP = socket.gethostbyname(var_localHostname) 
    except: 
      var_localIP = ""
    

    ###### ssh User ######
    var_sshUserNodes = getValueFromFile(configFile, 'sshUserNodes:', ':')
    def_sshUserNodes = var_sshUserNodes
    if not var_sshUserNodes:
      var_sshUserNodes = "ansible"

    correct = False
    count = 0
    print "-----------------------------------------------------------"
    print "System needs a SSH user to connect to hosts (using Ansible)"
    print "-----------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Remote user to connect: ', var_sshUserNodes)
      if inputValue:
        correct = True
        var_sshUserNodes = inputValue
        print
        continue
      else:
        print >> sys.stderr, "ERROR: No value"

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(1)

    # Sudo User 
    if var_sshUserNodes == "root":
      var_sudoUserNodes = "no"
    else:
      var_sudoUserNodes = "yes"


    ###### Ansible Server ######
    var_hostAnsible = getValueFromFile(configFile, 'hostAnsible:', ':') 
    def_hostAnsible = var_hostAnsible
    if not var_hostAnsible:
      # First Configuration
      var_hostAnsible = var_localIP
      print
      print "---------------------------------------------"
      print "Ansible Server Configuration (Control Server)"
      print "---------------------------------------------"
      print
      print "Hostname detected: %s" % (var_localHostname if var_localHostname != "" else "Not detected")
      print "Hostname (IP address) detected: %s" % (var_localIP if var_localIP != "" else "Not detected")
      if var_localHostname == "localhost" or var_localIP == "127.0.0.1":
	print "Hostname (IP address) should be different from localhost (127.0.0.1)"
	print "To change hostname, check '/etc/hosts' and '/etc/sysconfig/network' files and reboot"
      if var_localHostname == "":
	print "Hostname not detected. To change hostname, check '/etc/hosts' and '/etc/sysconfig/network' files and reboot"
      elif var_localIP == "":
	print "Hostname (IP address )not detected. To change hostname, check '/etc/hosts' and '/etc/sysconfig/network' files and reboot"
      print
      cadIP = subprocess.Popen("ip addr show|grep inet|grep -v 'inet6'|grep -v '127.0.0.1'|tr -s ' '|cut -d '/' -f1|sed 's/inet//g'|tr -d ' '", shell=True, stdout=subprocess.PIPE)
      IPList = cadIP.stdout.read().strip()
      if IPList != "":
	print "IPs detected"
	print IPList
	print
      confFirst = "y"
    else:
      confFirst = "n"

    if confFirst == "y":
      # Let user to select IP
      inputValue = raw_input_def('Ansible Server (Local IP address): ', var_hostAnsible)
    else:
      # Re-configuration
      print "Ansible Server (Local IP address): %s" % (var_hostAnsible)
      print
      inputValue = var_hostAnsible

    if inputValue.strip():
      # Checking syntax IP
      if checkIP(inputValue):
	# Check local IP 
	retCode = subprocess.call("ip addr show|grep '%s/' >/dev/null 2>/dev/null" % (inputValue), shell=True)
	if retCode == 0:
	  # Checking FQDN
          if checkFQDN(inputValue):
            # Checking IP Ansible access
            if not accessIP(inputValue, var_sshUserNodes):
              print "Ansible access to %s required." % (inputValue)
              if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                # Calling setupNode.py
                print "Configuring node..."
                retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
                if retCode != 0:
                  print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
                  print >> sys.stderr
		  sys.exit(2)
              else:
                print >> sys.stderr, "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
                print >> sys.stderr
	        sys.exit(2)

            # Check Operating System 
            print "Checking Operating System..."
            retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s ansible" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
            if retSOCode == 0:
              correct = True
              var_hostAnsible = inputValue.strip()
              print "Everything is OK"
              print

            else:
              print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
              print >> sys.stderr
              sys.exit(2)

	  else:
            print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
            print >> sys.stderr
            sys.exit(2)

        else:
          print >> sys.stderr, "ERROR: Not local IP address!!!"
          print >> sys.stderr
          sys.exit(2)

      else:
        print >> sys.stderr, "ERROR: IP address Syntax error!!!"
        print >> sys.stderr
	sys.exit(2)

    else:
      print >> sys.stderr, "ERROR: No value"
      print >> sys.stderr
      sys.exit(2)


    ###### Working Subnets ######
    var_subnets = getValueFromFile(configFile, 'subnets:', ':')
    def_subnets = var_subnets
    if not var_subnets:
      var_subnets = "%s/32" % (var_hostAnsible)

    correct = False
    count = 0
    print
    print "----------------------------------------------------------------------"
    print "System realizes monitoring over hosts belonging to 'working subnets'  "
    print "Working subnets should be written in CIDR notation (Ex 192.168.1.0/24)"
    print "----------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Working subnets (separated by white spaces): ', var_subnets)
      if inputValue.strip():
        # Splitting in subnets
        arr = inputValue.split(' ')
	correct = True
	for net in arr:
          # Checking syntax Network
	  if not checkNet(net):
            correct = False
	    print >> sys.stderr, "ERROR: Net %s Syntax error!!!" % (net)
	    print
        if correct:
          if IPInNetworks(var_hostAnsible,inputValue.strip()):
	    var_subnets = inputValue.strip()
	    print "Everything is OK"
            print
          else:
	    correct = False
            print >> sys.stderr, "ERROR: Ansible Host (%s) doesn't belong to any subnet (%s)" % (var_hostAnsible,inputValue.strip())
            print
      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(3)


    ###### Exclude (IPs) ######
    var_exclude = getValueFromFile(configFile, 'exclude:', ':')
    def_exclude = var_exclude

    correct = False
    count = 0
    print
    print "-----------------------------------------------------------------------------"
    print "System can exclude some IP addresses of 'working subnets' to avoid monitoring"
    print "-----------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('IP address to be excluded (separated by white spaces): ', var_exclude)
      if inputValue.strip():
        # Splitting in IPs
        arr = inputValue.split(' ')
        correct = True
        for IP in arr:
          # Checking syntax IP
          if not checkIP(IP,"localhost"):
            correct = False
            print >> sys.stderr, "ERROR: IP address %s Syntax error!!!" % (IP)
            print >> sys.stderr
        if correct:
          if var_hostAnsible not in arr:
            var_exclude = inputValue.strip()
            print "Everything is OK"
            print
          else:
            correct = False
            print >> sys.stderr, "ERROR: Ansible Server (%s) musn't be excluded (%s)" % (var_hostAnsible,inputValue.strip())
            print

      else:
	var_exclude = inputValue.strip()
	correct = True
        print "No IP address excluded"
        print

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(4)

    # Always exclude localhost
    if not "127.0.0.1" in var_exclude:
      var_exclude = ("127.0.0.1 " + var_exclude).strip()
 

    print
    print "--------------------------------------------------------------------------------"
    print "Servers Configuration (IP Addresses): Mysql, Nagios, Munin, Web, Grafana and "
    print "Openvas"
    print "--------------------------------------------------------------------------------"
    print


    ###### Mysql Server ######
    var_hostMysql = getValueFromFile(configFile, 'hostMysql:', ':')
    def_hostMysql = var_hostMysql
    if not var_hostMysql:
      var_hostMysql = var_hostAnsible

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Mysql Server (IP address): ', var_hostMysql)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible:
	  # Checking syntax IP
	  if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
	      # Checking if IP is excluded
	      if not IPInList(inputValue,var_exclude):
                # Checking FQDN
                if checkFQDN(inputValue):
	          # Checking IP Ansible access
		  access = 0
	          if not accessIP(inputValue, var_sshUserNodes):
		    print "Ansible access to %s required." % (inputValue)
                    if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                      # Calling setupNode.py
                      print "Configuring node..."
                      retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
	              if retCode != 0:
		        print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
		        print >> sys.stderr
		      else:
		        access = 1

                    else:
                      print "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
	              print

		  else:
		    access = 1

	          if access == 1:
	            # Check Operating System 
                    print "Checking Operating System..."
	            retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s mysql" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))	
	            if retSOCode == 0:
	              correct = True
	              var_hostMysql = inputValue.strip()
	              print "Everything is OK"
	              print

	            else:
	              print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
	              print >> sys.stderr

	        else:
          	  print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
          	  print >> sys.stderr

	      else:
                print >> sys.stderr, "ERROR: IP address (%s) belongs to excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

            else:
              print >> sys.stderr, "ERROR: IP address (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

	  else:
	    print >> sys.stderr, "ERROR: IP address Syntax error!!!"
	    print >> sys.stderr

	else:
          correct = True
          var_hostMysql = inputValue.strip()
          print "Everything is OK"
          print

      else:
	print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      count += 1
      if count > maxErrors:
	print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(5)

    if correct and def_hostMysql and def_hostMysql != var_hostMysql:
      print "*** You are moving Mysql server from %s to %s. Stop and disable Mysql service in %s to avoid confusion ***" % (def_hostMysql,var_hostMysql,def_hostMysql)
      print


    ###### Nagios Server ######
    var_hostNagios = getValueFromFile(configFile, 'hostNagios:', ':')
    def_hostNagios = var_hostNagios
    if not var_hostNagios:
      var_hostNagios = var_hostMysql

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Nagios Server (IP address): ', var_hostNagios)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking FQDN
                if checkFQDN(inputValue):
                  # Checking IP Ansible access
		  access = 0
                  if not accessIP(inputValue, var_sshUserNodes):
		    print "Ansible access to %s required." % (inputValue)
                    if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                      # Calling setupNode.py
                      print "Configuring node..."
                      retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
                      if retCode != 0:
                        print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
		        print >> sys.stderr
		      else:
		        access = 1

                    else:
                      print "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
	              print

                  else:
                    access = 1 

                  if access == 1:
                    # Check Operating System 
                    print "Checking Operating System..."
                    retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s nagios" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                    if retSOCode == 0:
                      correct = True
                      var_hostNagios = inputValue.strip()
	              print "Everything is OK"
                      print

                    else:
                      print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
	              print >> sys.stderr

                else:
                  print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
                  print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP address (%s) belongs to excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

	    else:
              print >> sys.stderr, "ERROR: IP address (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

	  else:
	    print >> sys.stderr, "ERROR: IP address Syntax error!!!"
	    print >> sys.stderr

	else:
          correct = True
          var_hostNagios = inputValue.strip()
          print "Everything is OK"
          print

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(6)

    if correct and def_hostNagios and def_hostNagios != var_hostNagios:
      print "*** You are moving Nagios server from %s to %s. Stop and disable Nagios and Graphios (connection to Influx database) services in %s to avoid confusion ***" % (def_hostNagios,var_hostNagios,def_hostNagios)
      print


    ###### Munin Server ######
    var_hostMunin = getValueFromFile(configFile, 'hostMunin:', ':')
    def_hostMunin = var_hostMunin
    if not var_hostMunin:
      var_hostMunin = var_hostNagios

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Munin Server (IP address): ', var_hostMunin)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking FQDN
                if checkFQDN(inputValue):
                  # Checking IP Ansible access
		  access = 0
                  if not accessIP(inputValue, var_sshUserNodes):
		    print "Ansible access to %s required." % (inputValue)
                    if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                      # Calling setupNode.py
                      print "Configuring node..."
                      retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
                      if retCode != 0:
                        print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
		        print >> sys.stderr
		      else:
		        access = 1 

                    else:
                      print "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
	              print

                  else:
                    access = 1 

                  if access == 1:
                    # Check Operating System 
                    print "Checking Operating System..."
                    retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s munin" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                    if retSOCode == 0:
                      correct = True
                      var_hostMunin = inputValue.strip()
	              print "Everything is OK"
                      print

                    else:
                      print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
	              print >> sys.stderr

                else:
                  print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
                  print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP address (%s) belongs excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

	    else:
              print >> sys.stderr, "ERROR: IP address (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP address Syntax error!!!"
	    print >> sys.stderr

	else:
          correct = True
          var_hostMunin = inputValue.strip()
          print "Everything is OK"
          print

      else:
	print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(7)

    if correct and def_hostMunin and def_hostMunin != var_hostMunin:
      print "*** You are moving Munin server from %s to %s. Stop and disable Munin service and delete munintoinfluxdb (connection to Influx database) entry on crontab in %s to avoid confusion ***" % (def_hostMunin,var_hostMunin,def_hostMunin)
      print


    ###### Web Server ######
    var_hostWeb = getValueFromFile(configFile, 'hostWeb:', ':')
    def_hostWeb = var_hostWeb
    if not var_hostWeb:
      var_hostWeb = var_hostMunin

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Web Server (IP address): ', var_hostWeb)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios and inputValue.strip() != var_hostMunin:
          # Checking syntax IP
	  if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking FQDN
                if checkFQDN(inputValue):
	          # Checking IP Ansible access
		  access = 0
                  if not accessIP(inputValue, var_sshUserNodes):
		    print "Ansible access to %s required." % (inputValue)
                    if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                      # Calling setupNode.py
                      print "Configuring node..."
                      retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
                      if retCode != 0:
                        print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
		        print >> sys.stderr
		      else:
		        access = 1

                    else:
                      print "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
	              print

                  else:
                    access = 1 

                  if access == 1:
                    # Check Operating System 
                    print "Checking Operating System..."
                    retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s web" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                    if retSOCode == 0:
                      correct = True
                      var_hostWeb = inputValue.strip()
	              print "Everything is OK"
                      print

                    else:
                      print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
	              print >> sys.stderr

                else:
                  print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
                  print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP address (%s) belongs to excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

	    else:
              print >> sys.stderr, "ERROR: IP address (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP address Syntax error!!!"
	    print >> sys.stderr

	else:
          correct = True
          var_hostWeb = inputValue.strip()
          print "Everything is OK"
          print

        if correct == True and var_hostWeb != var_hostMysql:
          # Checking SELinux
          if enforcingSELinux(var_hostWeb, var_sshUserNodes):
            print "SELinux is enabled (enforcing). If SELinux is not configured appropiately, PHPMyAdmin Server won't be able to manage Mysql (SELinux will block output connections)"
            print
            print "To disable SELinux: check status with 'sestatus' command, modify '/etc/sysconfig/selinux' file with 'SELINUX=disabled' and reboot"
            print
            if question("Do you want to continue configuration with SELinux 'enforcing' and change it later?", "y", 3) != "y":
              print
              print "Change SELinux and start again"
              print
              sys.exit(0)

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      count += 1
      if count > maxErrors:
        print sys.stderr, "Too many Errors. Exiting..."
        sys.exit(8)

    if correct and def_hostWeb and def_hostWeb != var_hostWeb:
      print "*** You are moving Web server from %s to %s. Stop and disable Web service (apache) in %s to avoid confusion (if no other software like Nagios or Munin required apache in server)***" % (def_hostWeb,var_hostWeb,def_hostWeb)
      print


    ###### Grafana Server ######
    var_hostGrafana = getValueFromFile(configFile, 'hostGrafana:', ':')
    def_hostGrafana = var_hostGrafana
    if not var_hostGrafana:
      var_hostGrafana = var_hostWeb

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Grafana Server (IP address): ', var_hostGrafana)
      if inputValue.strip():
        if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios and inputValue.strip() != var_hostMunin and inputValue.strip() != var_hostWeb:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking FQDN
                if checkFQDN(inputValue):
                  # Checking IP Ansible access
                  access = 0
                  if not accessIP(inputValue, var_sshUserNodes):
		    print "Ansible access to %s required." % (inputValue)
                    if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                      # Calling setupNode.py
                      print "Configuring node..."
                      retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
                      if retCode != 0:
                        print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
                        print >> sys.stderr
                      else:
                        access = 1

                    else:
                      print "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
                      print

                  else:
                    access = 1 

                  if access == 1:
                    # Check Operating System 
                    print "Checking Operating System..."
                    retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s web" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                    if retSOCode == 0:
                      correct = True
                      var_hostGrafana = inputValue.strip()
                      print "Everything is OK"
                      print

                    else:
                      print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
                      print >> sys.stderr

                else:
                  print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
                  print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP address (%s) belongs to excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

            else:
              print >> sys.stderr, "ERROR: IP address (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP address Syntax error!!!"
            print >> sys.stderr

        else:
          correct = True
          var_hostGrafana = inputValue.strip()
          print "Everything is OK"
          print

      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      count += 1
      if count > maxErrors:
        print sys.stderr, "Too many Errors. Exiting..."
        sys.exit(9)

    if correct and def_hostGrafana and def_hostGrafana != var_hostGrafana:
      print "*** You are moving Grafana server from %s to %s. Stop and disable Grafana and InfluxDB services in %s to avoid confusion ***" % (def_hostGrafana,var_hostGrafana,def_hostGrafana)
      print


    ###### Openvas Server ######
    var_hostOpenvas = getValueFromFile(configFile, 'hostOpenvas:', ':')
    def_hostOpenvas = var_hostOpenvas
    if not var_hostOpenvas:
      var_hostOpenvas = var_hostGrafana

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Openvas Server (IP address): ', var_hostOpenvas)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios and inputValue.strip() != var_hostMunin and inputValue.strip() != var_hostWeb and inputValue.strip() != var_hostGrafana:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking FQDN
                if checkFQDN(inputValue):

                  # Checking IP Ansible access
		  access = 0
                  if not accessIP(inputValue, var_sshUserNodes):
		    print "Ansible access to %s required." % (inputValue)
                    if question("Do you want to access by SSH with 'root' user and configure it automatically?", "y", 3) == "y":
                      # Calling setupNode.py
                      print "Configuring node..."
                      retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
                      if retCode != 0:
                        print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually. See EXAMPLE and FAQ (help)"
                        print >> sys.stderr
		      else:
		        access = 1

                    else:
                      print "You will have to access and configure it manually. See EXAMPLE and FAQ (help)"
                      print

                  else:
                    access = 1

                  if access == 1:
                    # Check Operating System 
                    print "Checking Operating System..."
                    retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s openvas" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                    if retSOCode == 0:
                      correct = True
                      var_hostOpenvas = inputValue.strip()
                      print "Everything is OK"
                      print

                    else:
                      print >> sys.stderr, "ERROR: Operating System not permitted. See EXAMPLE and FAQ (help)"
                      print >> sys.stderr

                else:
                  print >> sys.stderr, "ERROR: Not FQDN for %s!!! Change DNS or '/etc/hosts' file" % (inputValue)
                  print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP address (%s) belongs to excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

            else:
              print >> sys.stderr, "ERROR: IP address (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP address Syntax error!!!"
            print >> sys.stderr

	else:
          correct = True
          var_hostOpenvas = inputValue.strip()
          print "Everything is OK"
          print
	  
	if correct == True:
	  # Checking SELinux
	  if enforcingSELinux(var_hostOpenvas, var_sshUserNodes):
	    print "SELinux is enabled (enforcing). If SELinux is not configured appropiately, Openvas Server won't be able to scan vulnerabilities (SELinux will block output connections)"
	    print
	    print "To disable SELinux: check status with 'sestatus' command, modify '/etc/sysconfig/selinux' file with 'SELINUX=disabled' and reboot"
	    print
	    if question("Do you want to continue configuration with SELinux 'enforcing' and change it later?", "y", 3) != "y": 
	      print
	      print "Change SELinux and start again"
	      print 
	      sys.exit(0)

      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      count += 1
      if count > maxErrors:
        print sys.stderr, "Too many Errors. Exiting..."
        sys.exit(10)

    if correct and def_hostOpenvas and def_hostOpenvas != var_hostOpenvas:
      print "*** You are moving Openvas server from %s to %s. Stop and disable Openvas services (gsad, openvas-manager and openvas-scanner) in %s to avoid confusion ***" % (def_hostOpenvas,var_hostOpenvas,def_hostOpenvas)
      print


    print
    print
    print "-----------------------------------------------"
    print "Security Servers Configuration (Admin password)"
    print "-----------------------------------------------"
    print


    ###### Password Admin user ######
    var_passwdAdmin = getValueFromFile(configFile, 'passwdAdmin:', ':')
    def_passwdAdmin = var_passwdAdmin
    if not var_passwdAdmin:
      var_passwdAdmin = "admin"

    correct = False
    count = 0
    print
    print "-----------------------------------------"
    print "Servers require an 'admin' user to access"
    print "-----------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Password (admin user): ', var_passwdAdmin)
      if inputValue:
        correct = True
        var_passwdAdmin = inputValue
        print
        continue
      else:
        print >> sys.stderr, "ERROR: No value"
        pritn >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(11)


    ###### Password Mysql root user ######
    var_passwdMysqlRoot = getValueFromFile(configFile, 'passwdMysqlRoot:', ':')
    def_passwdMysqlRoot = var_passwdMysqlRoot
    if not var_passwdMysqlRoot:
      var_passwdMysqlRoot = var_passwdAdmin 

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Mysql Server requires a 'root' user to manage"
    print "Access allowed from localhost, Mysql Server, Web Server and Administrators Hosts"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Password Mysql (root user): ', var_passwdMysqlRoot)
      if inputValue:
        correct = True
        var_passwdMysqlRoot = inputValue
	print
	continue
      else:
        print >> sys.stderr, "ERROR: No value"
	pritn >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(12)


    ###### Hosts Admins ######
    var_hostsAdmins = getValueFromFile(configFile, 'hostsAdmins:', ':')
    if var_hostsAdmins == "''":
      var_hostsAdmins = ""
    def_hostsAdmins = var_hostsAdmins

    correct = False
    count = 0
    print
    print "-----------------------------------------------------"
    print "Administrators Hosts (allowed to acccess all Servers)"
    print "Leave empty to permit access from everywhere"
    print "-----------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Hosts administrators (IP addresses separated by white spaces): ', var_hostsAdmins)
      if inputValue.strip():
        # Splitting in IPs
        arr = inputValue.split(' ')
        correct = True
	for IP in arr:
	  # Checking syntax IP 
          if not checkIP(IP):
	    correct = False
	    print >> sys.stderr, "ERROR: IP address %s Syntax error!!!" % (IP)
	    print >> sys.stderr
      else:
        correct = True
        print "Access from everywhere"

      if correct:
        var_hostsAdmins = inputValue.strip()
        print "Everything is OK"
        print


      if not correct:
	count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(13)


    ###### Frequency Installation ######
    var_cronInstall = getValueFromFile(configFile, 'cronInstall:', ':').replace('|',':')
    def_cronInstall = var_cronInstall
    if not var_cronInstall:
      var_cronInstall = "3" 

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Ansible Server checks installed software and configurations on servers and nodes"
    print " to be sure everything is OK"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Frequency to check Installed Software (%s hours) or fixed time (00:00 to 23:59): ' % (frequencyRangeHours), var_cronInstall)
      if inputValue.strip():
 	if checkFrequency(inputValue.strip(),frequencyRangeHours) or checkTime(inputValue.strip()):
          correct = True
	  var_cronInstall = inputValue.strip()
          print
	else:
          print >> sys.stderr, "ERROR: Incorrect value"
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(14)


    ###### Frequency Outsiders ######
    var_cronOutsiders = getValueFromFile(configFile, 'cronOutsiders:', ':').replace('|',':')
    def_cronOutsiders = var_cronOutsiders
    if not var_cronOutsiders:
      var_cronOutsiders = "4"

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Ansible Server performs scannings tasks with 'nmap' to discover hosts belonging "
    print "to 'working subnets' and clasifies them as 'nodes' (they can be accessed by "
    print "Ansible Server using ansible with 'remote user') or 'outsiders' (they can't be "
    print "accessed)" 
    print "--------------------------------------------------------------------------------"
    print 
    while not correct:
      inputValue = raw_input_def('Frequency to check new hosts in subnets (%s hours) or fixed time (00:00 to 23:59): ' % (frequencyRangeHours), var_cronOutsiders)
      if inputValue.strip():
	if checkFrequency(inputValue.strip(),frequencyRangeHours) or checkTime(inputValue.strip()):
          correct = True
          var_cronOutsiders = inputValue.strip()
	  print
        else:
          print >> sys.stderr, "ERROR: Incorrect value"
          print >> sys.stderr

      else:
	print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
	count += 1
	if count > maxErrors:
	  print >> sys.stderr, "Too many Errors. Exiting..."
	  sys.exit(15)


    ###### Frequency Openvas ######
    var_cronOpenvas = getValueFromFile(configFile, 'cronOpenvas:', ':')
    def_cronOpenvas = var_cronOpenvas
    if not var_cronOpenvas:
      var_cronOpenvas = "2"

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Openvas Server checks vulnerabilities for every host belonging to 'working "
    print "subnets'"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Frequency to check vulnerabilities in hosts (%s months): ' % (frequencyRangeMonths), var_cronOpenvas)
      if inputValue.strip():
        # Checking frequency
        if checkFrequency(inputValue.strip(),frequencyRangeMonths):
          correct = True
          var_cronOpenvas = inputValue.strip()
          print
        else:
          print >> sys.stderr, "ERROR: Incorrect value"
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(16)


    ###### Frequency Nodes ######
    var_cronNodes = getValueFromFile(configFile, 'cronNodes:', ':').replace('|',':')
    def_cronNodes = var_cronNodes
    if not var_cronNodes:
      var_cronNodes = "2"

    correct = False
    count = 0
    print 
    print "--------------------------------------------------------------------------------"
    print "Ansible Server gets information (everything but packages and executables) from "
    print "nodes"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Frequency to get Info from Nodes (%s hours) or fixed time (00:00 to 23:59): ' % (frequencyRangeHours), var_cronNodes)
      if inputValue.strip():
	if checkFrequency(inputValue.strip(),frequencyRangeHours) or checkTime(inputValue.strip()):
	  correct = True
	  var_cronNodes = inputValue.strip()
	  print
        else:
          print >> sys.stderr, "ERROR: Incorrect value"
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(17)


    ###### Frequency Nodes (Packages) ######
    var_cronNodesPackages = getValueFromFile(configFile, 'cronNodesPackages:', ':').replace('|',':')
    def_cronNodesPackages = var_cronNodesPackages
    if not var_cronNodesPackages:
      var_cronNodesPackages = "6"

    correct = False
    count = 0
    print
    print "---------------------------------------------------"
    print "Ansible Server gets packages information from nodes"
    print "---------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Frequency to get Info Packages from Nodes (%s hours) or fixed time (00:00 to 23:59): ' % (frequencyRangeHours), var_cronNodesPackages)
      if inputValue.strip():
	if checkFrequency(inputValue.strip(),frequencyRangeHours) or checkTime(inputValue.strip()):
	  correct = True
	  var_cronNodesPackages = inputValue.strip()
	  print
        else:
          print >> sys.stderr, "ERROR: Incorrect value"
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
	count += 1
	if count > maxErrors:
	  print >> sys.stderr, "Too many Errors. Exiting..."
	  sys.exit(18)


    ###### Frequency Nodes (Executables) ######
    var_cronNodesExes = getValueFromFile(configFile, 'cronNodesExes:', ':').replace('|',':')
    def_cronNodesExes = var_cronNodesExes
    if not var_cronNodesExes:
      var_cronNodesExes = "24"

    correct = False
    count = 0
    print
    print "------------------------------------------------------"
    print "Ansible Server gets executables information from nodes"
    print "------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Frequency to get Info Executables from Nodes (%s hours) or fixed time (00:00 to 23:59): ' % (frequencyRangeHours), var_cronNodesExes)
      if inputValue.strip():
	if checkFrequency(inputValue.strip(),frequencyRangeHours) or checkTime(inputValue.strip()):
	  correct = True
	  var_cronNodesExes = inputValue.strip()
          print
        else:
          print >> sys.stderr, "ERROR: Incorrect value"
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(19)


    ###### Adding Nodes ######
    # Repeat loop until user decide to finish ('again' variable)
    print
    print "--------------------------------------------------------------------------------"
    print "After configuration, infrastructure deployment will be started. Then Ansible "
    print "Server will start a scanning of hosts to discover 'outsiders' and 'nodes'. We "
    print "can prepare some hosts to be detected as nodes"
    print "--------------------------------------------------------------------------------"
    print
    again = question("Do you want to configure hosts as nodes (ssh connection with 'root' required)?", "n", 3)
    while again == "y":
      # Ask host name or IP
      print
      try:
        host = raw_input('Hostname or IP address: ')
      except KeyboardInterrupt:
        host = ""

      if host:
        print
        try:
          retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,host,var_sshUserNodes), shell=True)
        except KeyboardInterrupt:
          retCode = 1

      else:
        print >> sys.stderr, "You have to introduce a hostname or IP address"
        print >> sys.stderr

      # Configure another host?
      print
      again = question("Do you want to configure another host?", "n", 3)


    ##### Checking Windows Hosts? #####
    var_winNodes = getValueFromFile(configFile, 'winNodes:', ':')
    def_winNodes = var_winNodes
    if var_winNodes != "y" and var_winNodes != "n":
      var_winNodes = "n"

    print
    print "--------------------------------------------------------------------------------"
    print "Ansible Server can check Windows hosts to get information about them if they are"
    print " 'Windows Nodes'. To prepare a Windows host to be a 'Windows Node' WMI (Windows "
    print "Management Instrumentation) has to be configured, and a user with specific "
    print "permissions (read FAQ help for details)"
    print "--------------------------------------------------------------------------------"
    print
    inputValue = question("Do you want to check windows hosts as nodes?", var_winNodes, 3) 
    if inputValue:
      var_winNodes = inputValue


    ##### User (Windows nodes) #####
    if var_winNodes == "y":
      var_winUserNodes = getValueFromFile(configFile, 'winUserNodes:', ':')
      def_winUserNodes = var_winUserNodes
      if not var_winUserNodes:
        var_winUserNodes = "ansible"

      correct = False
      count = 0
      while not correct:
        inputValue = raw_input_def('Remote user to connect to Windows nodes ( [domain/]user ): ', var_winUserNodes)
        if inputValue:
          correct = True
          var_winUserNodes = inputValue
          print
          continue
        else:
          print >> sys.stderr, "ERROR: No value"

        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(20)


    ###### Password Windows User Nodes ######
    if var_winNodes == "y":
      var_winPasswdNodes = getValueFromFile(configFile, 'winPasswdNodes:', ':')
      def_winPasswdNodes = var_winPasswdNodes
      if not var_winPasswdNodes:
        var_winPasswdNodes = "admin"

      correct = False
      count = 0
      while not correct:
        inputValue = raw_input_def('Password Windows User Nodes: ', var_winPasswdNodes)
        if inputValue:
          correct = True
          var_winPasswdNodes = inputValue
          print
          continue
        else:
          print >> sys.stderr, "ERROR: No value"
          print >> sys.stderr

        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(21)


    ###### Frequency WinNodes ######
    if var_winNodes == "y":
      var_winCronNodes = getValueFromFile(configFile, 'winCronNodes:', ':').replace('|',':')
      def_winCronNodes = var_winCronNodes
      if not var_winCronNodes:
        var_winCronNodes = "4"

      correct = False
      count = 0
      print
      print "--------------------------------------------------"
      print "Ansible Server gets information from Windows Nodes"
      print "--------------------------------------------------"
      print
      while not correct:
        inputValue = raw_input_def('Frequency to get Info from Windows Nodes (%s hours) or fixed time (00:00 to 23:59): ' % (frequencyRangeHours), var_winCronNodes)
        if inputValue.strip():
	  if checkFrequency(inputValue.strip(),frequencyRangeHours) or checkTime(inputValue.strip()):
            correct = True
            var_winCronNodes = inputValue.strip()
            print
          else:
            print >> sys.stderr, "ERROR: Incorrect value"
            print >> sys.stderr

        else:
          print >> sys.stderr, "ERROR: No value"
          print >> sys.stderr

        if not correct:
          count += 1
          if count > maxErrors:
            print >> sys.stderr, "Too many Errors. Exiting..."
            sys.exit(22)


    ###### SUMMARY ######
    print
    print "----------------------------------------"
    if confFirst == "y":
      print "          Main Configuration            "
    else: 
      print "         Main Re-Configuration          "
    print "----------------------------------------"
    print "Ansible Server: %s (%s)" % (var_hostAnsible,IPtoName(var_hostAnsible))
    print "Working Subnets: %s" % (var_subnets)
    print "Exclude: %s" % (var_exclude)
    print "Mysql Server: %s (%s)" % (var_hostMysql,IPtoName(var_hostMysql))
    print "Nagios Server: %s (%s)" % (var_hostNagios,IPtoName(var_hostNagios))
    print "Munin Server: %s (%s)" % (var_hostMunin,IPtoName(var_hostMunin))
    print "Web Server: %s (%s)" % (var_hostWeb,IPtoName(var_hostWeb))
    print "Grafana Server: %s (%s)" % (var_hostGrafana,IPtoName(var_hostGrafana))
    print "Openvas Server: %s (%s)" % (var_hostOpenvas,IPtoName(var_hostOpenvas))
    print "Remote User (nodes): %s with sudo='%s'" % (var_sshUserNodes,var_sudoUserNodes)
    print "Password Admin user: %s" % (var_passwdAdmin)
    print "Password Mysql root user: %s" % (var_passwdMysqlRoot)
    print "Hosts administrators: %s" % (var_hostsAdmins if var_hostsAdmins != "" else "ALL")
    print "Time check Installation: %s" % (var_cronInstall) if checkTime(var_cronInstall) else "Frequency check Installation: %s hours" % (var_cronInstall)
    print "Time check Outsiders: %s" % (var_cronOutsiders) if checkTime(var_cronOutsiders) else "Frequency check Outsiders: %s hours" % (var_cronOutsiders)
    print "Frequency check Openvas: %s months" % (var_cronOpenvas)
    print "Time check Nodes: %s" % (var_cronNodes) if checkTime(var_cronNodes) else "Frequency check Nodes: %s hours" % (var_cronNodes)
    print "Time check Nodes (Packages): %s" % (var_cronNodesPackages) if checkTime(var_cronNodesPackages) else "Frequency check Nodes (Packages): %s hours" % (var_cronNodesPackages)
    print "Time check Nodes (Executables): %s" % (var_cronNodesExes) if checkTime(var_cronNodesExes) else "Frequency check Nodes (Executables): %s hours" % (var_cronNodesExes)
    print "Check Windows Nodes? %s" % (var_winNodes)
    if var_winNodes == "y":
      print "Remote User (Windows nodes): %s" % (var_winUserNodes)
      print "Password Remote User (Windows Nodes): %s" % (var_winPasswdNodes)
      print "Time check Windows Nodes: %s" % (var_winCronNodes) if checkTime(var_winCronNodes) else "Frequency check Windows Nodes: %s hours" % (var_winCronNodes)
    print "----------------------------------------"
    print



    if question("Config and Start?", "y", 3) == "y":
      print "Generating Temporal Production File %s ..." % (productionFileTmp)
      try:
        f = open(productionFileTmp, 'w')
        extra = open(configExtra, 'r')

        f.write("### FILE GENERATED BY ANSIBLE. DON'T TOUCH ###\n")
        f.write("\n") 
	f.write("### Main variables ###\n")
	f.write("\n")
        f.write("# Path Ansible\n")
        f.write("pathAnsible: %s\n" % (pathAnsible))

	f.write("\n")
        f.write("# Host Ansible\n")
        f.write("hostAnsible: %s\n" % (var_hostAnsible))
	f.write("\n")
	f.write("# Hostname Ansible\n")
	f.write("hostnameAnsible: %s\n" % (IPtoName(var_hostAnsible)))
	f.write("\n")
	f.write("# Subnets\n")
	f.write("subnets:\n")
	arr = var_subnets.split(' ')
	for x in arr:
	  f.write("- %s\n" % (x))
        f.write("\n")
        f.write("# Exclude\n")
        f.write("exclude:\n")
        arr = var_exclude.split(' ')
        for x in arr:
          f.write("- %s\n" % (x))
        f.write("\n")
	f.write("# Host Mysql\n")
	f.write("hostMysql: %s\n" % (var_hostMysql))
	f.write("\n")
        f.write("# Hostname Mysql\n")
        f.write("hostnameMysql: %s\n" % (IPtoName(var_hostMysql)))
        f.write("\n")
	f.write("# Host Nagios\n")
	f.write("hostNagios: %s\n" % (var_hostNagios))
	f.write("\n")
        f.write("# Hostname Nagios\n")
        f.write("hostnameNagios: %s\n" % (IPtoName(var_hostNagios)))
        f.write("\n")
	f.write("# Host Munin\n")
	f.write("hostMunin: %s\n" % (var_hostMunin))
	f.write("\n")
        f.write("# Hostname Munin\n")
        f.write("hostnameMunin: %s\n" % (IPtoName(var_hostMunin)))
        f.write("\n")
        f.write("# Host Web\n")
        f.write("hostWeb: %s\n" % (var_hostWeb))
        f.write("\n")
        f.write("# Hostname Web\n")
        f.write("hostnameWeb: %s\n" % (IPtoName(var_hostWeb)))
        f.write("\n")
        f.write("# Host Grafana\n")
        f.write("hostGrafana: %s\n" % (var_hostGrafana))
        f.write("\n")
        f.write("# Hostname Grafana\n")
        f.write("hostnameGrafana: %s\n" % (IPtoName(var_hostGrafana)))
        f.write("\n")
        f.write("# Host Openvas\n")
        f.write("hostOpenvas: %s\n" % (var_hostOpenvas))
        f.write("\n")
        f.write("# Hostname Openvas\n")
        f.write("hostnameOpenvas: %s\n" % (IPtoName(var_hostOpenvas)))
        f.write("\n")
        f.write("# Remote user (nodes)\n")
        f.write("sshUserNodes: %s\n" % (var_sshUserNodes))
        f.write("\n")
	f.write("# Default remote user (nodes)\n")
        f.write("ansible_ssh_user: %s\n" % (var_sshUserNodes))
        f.write("\n")
        f.write("# Password Admin user\n")
        f.write("passwdAdmin: %s\n" % (var_passwdAdmin))
        f.write("\n")
        f.write("# Password Mysql root user\n")
	f.write("passwdMysqlRoot: %s\n" % (var_passwdMysqlRoot))
	f.write("\n")
        f.write("# Hosts Administrators\n")
        if var_hostsAdmins != "":
          f.write("hostsAdmins:\n")
          arr = var_hostsAdmins.split(' ')
          for x in arr:
            f.write("- %s\n" % (x))
        else:
          f.write("hostsAdmins: ''\n")
        f.write("\n")
	f.write("# Frequency Installation (hours) or Fixed Time (00|00 to 23|59)\n")
	f.write("cronInstall: %s\n" % (var_cronInstall.replace(':','|')))
	f.write("\n")
        f.write("# Frequency Outsiders (hours) or Fixed Time (00|00 to 23|59)\n")
	f.write("cronOutsiders: %s\n" % (var_cronOutsiders.replace(':','|')))
	f.write("\n")
        f.write("# Frequency Openvas (months)\n")
        f.write("cronOpenvas: %s\n" % (var_cronOpenvas))
        f.write("\n")
        f.write("# Frequency Nodes (hours) or Fixed Time (00|00 to 23|59)\n")
	f.write("cronNodes: %s\n" % (var_cronNodes.replace(':','|')))
	f.write("\n")
        f.write("# Frequency Nodes - Packages (hours) or Fixed Time (00|00 to 23|59)\n")
	f.write("cronNodesPackages: %s\n" % (var_cronNodesPackages.replace(':','|')))
	f.write("\n")
        f.write("# Frequency Nodes - Executables (hours) or Fixed Time (00|00 to 23|59)\n")
	f.write("cronNodesExes: %s\n" % (var_cronNodesExes.replace(':','|')))
        f.write("\n")
        f.write("# Checking Windows Nodes?\n")
        f.write("winNodes: %s\n" % (var_winNodes))
        f.write("\n")
	if var_winNodes == "y":
          f.write("# Remote User (Windows nodes)\n")
          f.write("winUserNodes: %s\n" % (var_winUserNodes))
          f.write("\n")
          f.write("# Password Remote User (Windows nodes)\n")
          f.write("winPasswdNodes: %s\n" % (var_winPasswdNodes))
	  f.write("\n")
          f.write("# Frequency Windows Nodes (hours) or Fixed Time (00|00 to 23|59)\n")
          f.write("winCronNodes: %s\n" % (var_winCronNodes.replace(':','|')))
          f.write("\n")
	f.write("\n")
        for line in extra.readlines():
          if line.startswith("hostsReadUser:") and not line.startswith("hostsReadUser: ''"):
            arrLine = line.split(':', 1)
            f.write("%s:\n" % (arrLine[0]))
            arrData = arrLine[1].strip().split(' ')
            for data in arrData:
              f.write("- %s\n" % (data))
          else:
            f.write("%s" % (line))

	extra.close()
	f.close()
        print "Generated."
        print

      except:
        print >> sys.stderr, "Error opening file: %s" % (productionFileTmp)
        sys.exit(23)

      print "Updating Real Production File %s ..." % (productionFile)
      try:
        # Backup Production file
        print "Saved Old Production file as '.back'" 
        shutil.copy(productionFile, "%s.back" % (productionFile))
	os.chmod("%s.back" % (productionFile), 0600)
        # Move Temp file to Production file
        print "Moving Temporal to Real..."
        shutil.move(productionFileTmp, productionFile)
	os.chmod(productionFile, 0600)
        print "Done."
        print
      except:
        print >> sys.stderr, "Error updating Real Production file %s" % (productionFile) 
        sys.exit(24)      
  
      print "Updating Config file %s ..." % (configFile)
      try:

        # Backup Config file
        shutil.copy(configFile, "%s.back" % (configFile))
	print "Saved Old Config file as '.back'"
	os.chmod("%s.back" % (configFile), 0600)
	os.chmod(configFile, 0600)

        f = open(configFile, 'w')

        f.write("### Main variables ###\n")
        f.write("\n")
        f.write("# Path Ansible\n")
        f.write("pathAnsible: %s\n" % (pathAnsible))
        f.write("\n")
        f.write("# Remote user (nodes)\n")
        f.write("sshUserNodes: %s\n" % (var_sshUserNodes))
        f.write("\n")
        f.write("# Default remote user (nodes)\n")
        f.write("ansible_ssh_user: %s\n" % (var_sshUserNodes))
        f.write("\n")
        f.write("# Password Admin user\n")
        f.write("passwdAdmin: %s\n" % (var_passwdAdmin))
        f.write("\n")
        f.write("# Password Mysql root user\n")
        f.write("passwdMysqlRoot: %s\n" % (var_passwdMysqlRoot))
        f.write("\n")
        f.write("# Hosts Administrators\n")
        f.write("hostsAdmins: %s\n" % (var_hostsAdmins if var_hostsAdmins != "" else "''"))
        f.write("\n")
        f.write("# Frequency Installation (hours) or Fixed Time (00|00 to 23|59)\n")
        f.write("cronInstall: %s\n" % (var_cronInstall.replace(':','|')))
        f.write("\n")
        f.write("# Frequency Outsiders (hours) or Fixed Time (00|00 to 23|59)\n")
        f.write("cronOutsiders: %s\n" % (var_cronOutsiders.replace(':','|')))
        f.write("\n")
        f.write("# Frequency Openvas (months)\n")
        f.write("cronOpenvas: %s\n" % (var_cronOpenvas))
        f.write("\n")
        f.write("# Frequency Nodes (hours) or Fixed Time (00|00 to 23|59)\n")
        f.write("cronNodes: %s\n" % (var_cronNodes.replace(':','|')))
        f.write("\n")
        f.write("# Frequency Nodes - Packages (hours) or Fixed Time (00|00 to 23|59)\n")
        f.write("cronNodesPackages: %s\n" % (var_cronNodesPackages.replace(':','|')))
        f.write("\n")
        f.write("# Frequency Nodes - Executables (hours) or Fixed Time (00|00 to 23|59)\n")
        f.write("cronNodesExes: %s\n" % (var_cronNodesExes.replace(':','|')))
        f.write("\n")
        f.write("# Checking Windows Nodes?\n")
        f.write("winNodes: %s\n" % (var_winNodes))
	if var_winNodes == "y":
	  f.write("\n")
          f.write("# Remote User (Windows nodes)\n")
          f.write("winUserNodes: %s\n" % (var_winUserNodes))
          f.write("\n")
          f.write("# Password Remote User (Windows nodes)\n")
          f.write("winPasswdNodes: %s\n" % (var_winPasswdNodes))
          f.write("\n")
          f.write("# Frequency Windows Nodes (hours) or Fixed Time (00|00 to 23|59)\n")
          f.write("winCronNodes: %s\n" % (var_winCronNodes.replace(':','|')))

        f.close()
        print "Done."
        print

      except:
        print >> sys.stderr, "Error updating Config file %s" % (configFile)
        print >> sys.stderr


      # Updating sudo
      print "Updating sudo in playbooks..."
      for file in glob.glob("%s/*.yml" % (pathAnsible)):
	print "File: %s..." % (file)
     	if var_sudoUserNodes == "no":
	  subprocess.call("sed -i 's/become:\s*\([yY]es\|[tT]rue\)/become: no/g' %s" % (file), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)	
	else:
	  subprocess.call("sed -i 's/become:\s*\([nN]o\|[fF]alse\)/become: yes/g' %s" % (file), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)
      print "Done."
      print


      # Updating Inventory
      print "Updating inventory %s/inventory/ ..." % (pathAnsible)
      try:
        invAnsible = open(inventoryAnsible, 'w') 
        invMysql = open(inventoryMysql, 'w')
        invNagios = open(inventoryNagios, 'w')
        invMunin = open(inventoryMunin, 'w')
        invWeb = open(inventoryWeb, 'w')
	invGrafana = open(inventoryGrafana, 'w')
	invOpenvas = open(inventoryOpenvas, 'w')
        invServers = open(inventoryServers, 'w')

        invAnsible.write("# Ansible Server\n")
        invAnsible.write("\n")
        invAnsible.write("[ansible]\n")
        invAnsible.write("%s\n" % (IPtoName(var_hostAnsible)))
        invAnsible.write("\n")

        invMysql.write("# Mysql Server\n")
        invMysql.write("\n")
        invMysql.write("[mysql]\n")
        invMysql.write("%s\n" % (IPtoName(var_hostMysql)))
        invMysql.write("\n")

        invNagios.write("# Nagios Server\n")
	invNagios.write("\n")
        invNagios.write("[nagios]\n")
        invNagios.write("%s\n" % (IPtoName(var_hostNagios)))
        invNagios.write("\n")

        invMunin.write("# Munin Server\n")
        invMunin.write("\n")
        invMunin.write("[munin]\n")
        invMunin.write("%s\n" % (IPtoName(var_hostMunin)))
        invMunin.write("\n")

        invWeb.write("# Web Server\n")
        invWeb.write("\n")
        invWeb.write("[web]\n")
        invWeb.write("%s\n" % (IPtoName(var_hostWeb)))
        invWeb.write("\n")

        invGrafana.write("# Grafana Server\n")
        invGrafana.write("\n")
        invGrafana.write("[grafana]\n")
        invGrafana.write("%s\n" % (IPtoName(var_hostGrafana)))
        invGrafana.write("\n")

        invOpenvas.write("# Openvas Server\n")
        invOpenvas.write("\n")
        invOpenvas.write("[openvas]\n")
        invOpenvas.write("%s\n" % (IPtoName(var_hostOpenvas)))
        invOpenvas.write("\n")

        invServers.write("# Servers\n")
        invServers.write("\n")
        invServers.write("[servers]\n")
	invServers.write("%s\n" % (IPtoName(var_hostAnsible)))
        if var_hostMysql != var_hostAnsible:
	  invServers.write("%s\n" % (IPtoName(var_hostMysql)))
        if var_hostNagios != var_hostAnsible and var_hostNagios != var_hostMysql:
	  invServers.write("%s\n" % (IPtoName(var_hostNagios)))
        if var_hostMunin != var_hostAnsible and var_hostMunin != var_hostMysql and var_hostMunin != var_hostNagios:
	  invServers.write("%s\n" % (IPtoName(var_hostMunin)))
        if var_hostWeb != var_hostAnsible and var_hostWeb != var_hostMysql and var_hostWeb != var_hostNagios and var_hostWeb != var_hostMunin:
	  invServers.write("%s\n" % (IPtoName(var_hostWeb)))
        invServers.write("\n")
        if var_hostGrafana != var_hostAnsible and var_hostGrafana != var_hostMysql and var_hostGrafana != var_hostNagios and var_hostGrafana != var_hostMunin and var_hostGrafana != var_hostWeb:
          invServers.write("%s\n" % (IPtoName(var_hostGrafana)))
        invServers.write("\n")
	if var_hostOpenvas != var_hostAnsible and var_hostOpenvas != var_hostMysql and var_hostOpenvas != var_hostNagios and var_hostOpenvas != var_hostMunin and var_hostOpenvas != var_hostWeb and var_hostOpenvas != var_hostGrafana:
          invServers.write("%s\n" % (IPtoName(var_hostOpenvas)))
        invServers.write("\n")



        invAnsible.close()
	invMysql.close()
	invNagios.close()
	invMunin.close()
	invWeb.close()
	invGrafana.close()
	invOpenvas.close()
  	invServers.close()

        print "Done."
        print

      except:
        print >> sys.stderr, "Error updating inventory %s/inventory/" % (pathAnsible)
        # Restoring Production File from backup 
        print >> sys.stderr, "Restoring Production file from backup %s.back ..." % (productionFile)
        shutil.copy("%s.back" % (productionFile), productionFile)
        print >> sys.stderr, "Done."
        sys.exit(25)  


      # Calling Playbooks
      print
      print "Calling Playbooks..."
      print

      # Deleting Ansible crontab entries 
      print "Deleting Ansible crontab entries..."
      print 
      subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/ansible.yml -t cronStop -u %s -s 2>&1|tee /var/log/ansible/.configure-cronStop.$timestamp.log.tmp; [ ${PIPESTATUS[0]} -gt 0 ] && ((echo; echo \"### ERRORS System Stop (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-cronStop.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-cronStop.$timestamp.log.tmp; echo \"### System Stop (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,var_sshUserNodes), shell=True)
      print 
      print "Done."
      print 


      # Installing & Configuring Ansible
      if var_hostAnsible != def_hostAnsible or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Installing & Configuring Ansible server..."
        print 
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/ansible.yml -t install,config -u %s -s 2>&1|tee /var/log/ansible/.configure-ansible.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Ansible Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-ansible.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-ansible.$timestamp.log.tmp; echo \"### Ansible Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(26)
        print 
        print "Done."
        print 

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Ansible", "hostAnsible: %s" % (var_hostAnsible)) or not writeVariableToFile(configFile, "# Hostname Ansible", "hostnameAnsible: %s" % (IPtoName(var_hostAnsible))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Installing & Configuring Mysql Server 
      if var_hostMysql != def_hostMysql or var_passwdMysqlRoot != def_passwdMysqlRoot or var_passwdAdmin != def_passwdAdmin or var_hostsAdmins != def_hostsAdmins or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Installing & Configuring Mysql Server..."
        print 
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/mysql.yml -u %s -s 2>&1|tee /var/log/ansible/.configure-mysql.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Mysql Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-mysql.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-mysql.$timestamp.log.tmp; echo \"### Mysql Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again" 
          sys.exit(27)
        print 
        print "Done."
        print 

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Mysql", "hostMysql: %s" % (var_hostMysql)) or not writeVariableToFile(configFile, "# Hostname Mysql", "hostnameMysql: %s" % (IPtoName(var_hostMysql))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Installing & Configuring Web Server 
      if var_hostWeb != def_hostWeb or var_passwdAdmin != def_passwdAdmin or var_hostsAdmins != def_hostsAdmins or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas): 
        print "Installing & Configuring Web Server..."
        print 
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/web.yml -u %s -s 2>&1|tee /var/log/ansible/.configure-web.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Web Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-web.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-web.$timestamp.log.tmp; echo \"### Web Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(28)
        print 
        print "Done."
        print 

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Web", "hostWeb: %s" % (var_hostWeb)) or not writeVariableToFile(configFile, "# Hostname Web", "hostnameWeb: %s" % (IPtoName(var_hostWeb))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Installing & Configuring Munin Server 
      if var_hostMunin != def_hostMunin or var_hostsAdmins != def_hostsAdmins or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Installing & Configuring Munin Server..."
        print 
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/munin.yml -u %s -s 2>&1|tee /var/log/ansible/.configure-munin.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Munin Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-munin.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-munin.$timestamp.log.tmp; echo \"### Munin Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(29)
        print 
        print "Done."
        print 

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Munin", "hostMunin: %s" % (var_hostMunin)) or not writeVariableToFile(configFile, "# Hostname Munin", "hostnameMunin: %s" % (IPtoName(var_hostMunin))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Installing & Configuring Nagios Server
      if var_hostNagios != def_hostNagios or var_hostsAdmins != def_hostsAdmins or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Installing & Configuring Nagios Server..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/nagios.yml -u %s -s 2>&1|tee /var/log/ansible/.configure-nagios.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Nagios Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-nagios.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-nagios.$timestamp.log.tmp; echo \"### Nagios Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(30)
        print 
        print "Done."
        print

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Nagios", "hostNagios: %s" % (var_hostNagios)) or not writeVariableToFile(configFile, "# Hostname Nagios", "hostnameNagios: %s" % (IPtoName(var_hostNagios))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Installing & Configuring Grafana Server
      if var_hostGrafana != def_hostGrafana or var_passwdAdmin != def_passwdAdmin or var_hostsAdmins != def_hostsAdmins or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Installing & Configuring Grafana Server..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/grafana.yml -u %s -s --skip-tags dashboards 2>&1|tee /var/log/ansible/.configure-grafana.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Grafana Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-grafana.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-grafana.$timestamp.log.tmp; echo \"### Grafana Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(31)
        print
        print "Done."
        print

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Grafana", "hostGrafana: %s" % (var_hostGrafana)) or not writeVariableToFile(configFile, "# Hostname Grafana", "hostnameGrafana: %s" % (IPtoName(var_hostGrafana))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Scanning Networks to discover hosts (nodes and outsiders)
      if var_subnets != def_subnets or var_exclude != def_exclude or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Scanning Networks to discover hosts (nodes and outsiders)..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/outsiders.yml -u %s -s 2>&1|tee /var/log/ansible/.configure-outsiders.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Scanning Networks (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-outsiders.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-outsiders.$timestamp.log.tmp; echo \"### Scanning Networks (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(32)
        print
        print "Done."
        print


      # Installing software nodes
      if var_subnets != def_subnets or var_exclude != def_exclude or var_hostNagios != def_hostNagios or var_hostMunin != def_hostMunin or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Configuring Nodes..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/nodes.yml -t install -u %s -s 2>&1|tee /var/log/ansible/.configure-nodesInstall.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Nodes Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-nodesInstall.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-nodesInstall.$timestamp.log.tmp; echo \"### Nodes Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error configuring nodes!!!"
	  print >> sys.stderr, "Select option '6. Install Node(s)' in Control menu after"
	  print >> sys.stderr, "configuration to view errors and reinstall nodes again."
	  msgErrors = "Error configuring nodes!!!\n"
	  msgErrors = "Select option '6. Install Node(s)' in Control menu after\n"
	  msgErrors = "configuration to view errors and reinstall nodes again.\n\n"
        print
        print "Done."
        print


      # Getting basic data from nodes
      if var_subnets != def_subnets or var_exclude != def_exclude or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Getting basic data from nodes..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/nodes.yml -t dataDB -u %s -s 2>&1|tee /var/log/ansible/.configure-nodesData.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Getting Data from Nodes (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-nodesData.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-nodesData.$timestamp.log.tmp; echo \"### Getting Data from Nodes (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error getting data from nodes!!!"
          print >> sys.stderr, "Select option '7. Get Data from Node(s)' in Control menu after"
          print >> sys.stderr, "configuration to view errors and get data from nodes again."
          msgErrors = "Error getting data from nodes!!!\n"
          msgErrors = "Select option '7. Get Data from Node(s)' in Control menu after\n"
          msgErrors = "configuration to view errors and get data from nodes again.\n\n"
        print
        print "Done."
        print


      if var_winNodes == "y":
        # Getting data from windows node
        if var_subnets != def_subnets or var_exclude != def_exclude or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
          print "Getting data from windows nodes..."
          print
	  retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/winNodes.yml 2>&1|tee /var/log/ansible/.configure-winNodes.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Getting data from Windows Nodes (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-winNodes.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-winNodes.$timestamp.log.tmp; echo \"### Getting Data from Nodes (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible), shell=True)
          if retCode != 0:
            print >> sys.stderr, "Error getting data from Windows nodes!!!"
            print >> sys.stderr, "Select option '8. Get Data from Windows Node(s)' in Control menu after"
            print >> sys.stderr, "configuration to view errors and get data from Windows nodes again."
            msgErrors = "Error getting data from Windows nodes!!!\n"
            msgErrors = "Select option '8. Get Data from Windows Node(s)' in Control menu after\n"
            msgErrors = "configuration to view errors and get data from Windows nodes again.\n\n"
          print
          print "Done."
          print

      # Installing & Configuring Openvas Server
      if var_hostOpenvas != def_hostOpenvas or var_passwdAdmin != def_passwdAdmin or var_hostsAdmins != def_hostsAdmins or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Installing Openvas Server..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/openvas.yml -t install,openssl,config --skip-tags dataDB -u %s -s 2>&1|tee /var/log/ansible/.configure-openvas.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Openvas Install & Config (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-openvas.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-openvas.$timestamp.log.tmp; echo \"### Openvas Install & Config (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(33)
        print
        print "Done."
        print

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Host Openvas", "hostOpenvas: %s" % (var_hostOpenvas)) or not writeVariableToFile(configFile, "# Hostname Openvas", "hostnameOpenvas: %s" % (IPtoName(var_hostOpenvas))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr

      # Configuring Grafana dashboards 
      if var_hostGrafana != def_hostGrafana or var_subnets != def_subnets or var_exclude != def_exclude or (var_hostAnsible != def_hostAnsible or var_hostMysql != def_hostMysql or var_hostWeb != def_hostWeb or var_hostMunin != def_hostMunin or var_hostNagios != def_hostNagios or var_hostGrafana != def_hostGrafana or var_hostOpenvas != def_hostOpenvas):
        print "Configuring Grafana dashboards..."
        print
	retCode = subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/grafana.yml -t dashboards -u %s -s 2>&1|tee /var/log/ansible/.configure-grafanaDashboards.$timestamp.log.tmp; ret=${PIPESTATUS[0]}; [ $ret -gt 0 ] && ((echo; echo \"### ERRORS Grafana Dashboards (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-grafanaDashboards.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-grafanaDashboards.$timestamp.log.tmp; echo \"### Grafana Dashboards (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log; exit $ret" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(34)
        print
        print "Done."
        print

      # Writing Variables to Config File
      if not writeVariableToFile(configFile, "# Subnets", "subnets: %s" % (var_subnets)) or not writeVariableToFile(configFile, "# Exclude", "exclude: %s" % (var_exclude)):
        print >> sys.stderr
        print >> sys.stderr, "Error writing variables to config file"
        print >> sys.stderr


      # Adding Ansible crontab entries
      print "Adding Ansible crontab entries..."
      print
      subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/ansible.yml -t cronStart -u %s -s 2>&1|tee /var/log/ansible/.configure-cronStart.$timestamp.log.tmp; [ ${PIPESTATUS[0]} -gt 0 ] && ((echo; echo \"### ERRORS System Start (configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configure-cronStart.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configure-cronStart.$timestamp.log.tmp; echo \"### System Start (configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,var_sshUserNodes), shell=True)
      print
      print "Done."
      print

      # There's been errors, let's show them
      if msgErrors != "":
	print
	print "There's been errors:"
	print
	print msgErrors

      print
      print "Start analyzing results (Nagios, Munin, Wiki, Mysql (PhpMyAdmin), Web Apps (PHP & AngularJS), InfluxDB, Grafana and Openvas) from URL https://%s" % (IPtoName(var_hostWeb))
      print

    else:
      print "Cancelled."
      print


  except KeyboardInterrupt:
    print
    print "Configuration interrumped"
    print

    # Writing default values to config file

    if not getValueFromFile(configFile, 'hostAnsible:', ':'):
      # Writing default values to Config File
      if not writeVariableToFile(configFile, "# Host Ansible", "hostAnsible: %s" % (def_hostAnsible)) or not writeVariableToFile(configFile, "# Hostname Ansible", "hostnameAnsible: %s" % (IPtoName(def_hostAnsible))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'hostMysql:', ':'):
      # Writing default values to Config File
      if not writeVariableToFile(configFile, "# Host Mysql", "hostMysql: %s" % (def_hostMysql)) or not writeVariableToFile(configFile, "# Hostname Mysql", "hostnameMysql: %s" % (IPtoName(def_hostMysql))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'hostWeb:', ':'):
      if not writeVariableToFile(configFile, "# Host Web", "hostWeb: %s" % (def_hostWeb)) or not writeVariableToFile(configFile, "# Hostname Web", "hostnameWeb: %s" % (IPtoName(def_hostWeb))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'hostMunin:', ':'):
      if not writeVariableToFile(configFile, "# Host Munin", "hostMunin: %s" % (def_hostMunin)) or not writeVariableToFile(configFile, "# Hostname Munin", "hostnameMunin: %s" % (IPtoName(def_hostMunin))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'hostNagios:', ':'):
      if not writeVariableToFile(configFile, "# Host Nagios", "hostNagios: %s" % (def_hostNagios)) or not writeVariableToFile(configFile, "# Hostname Nagios", "hostnameNagios: %s" % (IPtoName(def_hostNagios))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'hostGrafana:', ':'):
      if not writeVariableToFile(configFile, "# Host Grafana", "hostGrafana: %s" % (def_hostGrafana)) or not writeVariableToFile(configFile, "# Hostname Grafana", "hostnameGrafana: %s" % (IPtoName(def_hostGrafana))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'hostOpenvas:', ':'):
      if not writeVariableToFile(configFile, "# Host Openvas", "hostOpenvas: %s" % (def_hostOpenvas)) or not writeVariableToFile(configFile, "# Hostname Openvas", "hostnameOpenvas: %s" % (IPtoName(def_hostOpenvas))):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr

    if not getValueFromFile(configFile, 'subnets:', ':'):
      if not writeVariableToFile(configFile, "# Subnets", "subnets: %s" % (def_subnets)) or not writeVariableToFile(configFile, "# Exclude", "exclude: %s" % (def_exclude)):
        print >> sys.stderr
        print >> sys.stderr, "Error writing default values to config file"
        print >> sys.stderr





if __name__ == '__main__':
	    main()

