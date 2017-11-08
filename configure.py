#!/usr/bin/python

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
inventoryServers = "%s/inventory/servers" % (pathAnsible)
inventoryNodes = "%s/inventory/nodes" % (pathAnsible)
inventoryWinNodes = "%s/inventory/winNodes" % (pathAnsible)

# Frequency Range
frequencyRangeMinutes = "5 6 10 12 15 20 30 60 120 180 240 360 480 720 1440"
frequencyRangeHours = "1 2 3 4 6 8 12 24"
frequencyRangeMonths = "1 2 3 4 6 12"

# Max Errors
maxErrors = 3


def checkIP(IP):
    print "Checking IP (%s) syntax..." % (IP)
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


def IPtoName(IP):
    try:
      nameDNS = socket.gethostbyaddr(IP)
    except:
      return IP 

    return nameDNS[0].lower()


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
        print "ERROR: value %s is not valid. Values (y/n)" % (inputValue.strip())

      count += 1
      if count > maxErrors:
        print "Too many Errors. Exiting..."
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

    # Clear screen
    os.system("clear")
    # System configuration
    print "#####################################"
    print " System Configuration and Deployment "
    print "#####################################"
    print

    # Getting local IP
    var_localIP = socket.gethostbyname(socket.gethostname()) 
    

    ###### ssh User ######
    var_sshUserNodes = getValueFromFile(configFile, 'sshUserNodes:', ':')
    def_sshUserNodes = var_sshUserNodes
    if not var_sshUserNodes:
      var_sshUserNodes = "ansible"

    correct = False
    count = 0
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


    ###### Ansible Host ######
    var_hostAnsible = getValueFromFile(configFile, 'hostAnsible:', ':') 
    def_hostAnsible = var_hostAnsible
    if not var_hostAnsible:
      var_hostAnsible = var_localIP

    print 
    print "Getting Ansible local IP (%s)..." % var_hostAnsible

    if not var_hostAnsible: 
      print >> sys.stderr, "Host Ansible IP Error: No value"
      sys.exit(2)

    # Checking syntax IP
    print
    print "Ansible Host (IP): %s" % var_hostAnsible 
    if not checkIP(var_hostAnsible):
      print >> stderr, "Host Ansible IP Error: %s not valid" % (var_hostAnsible)
      sys.exit(3)

    # Checking IP Ansible access
    if not accessIP(var_hostAnsible, var_sshUserNodes):
      print "Host Ansible IP Error: no Ansible access to %s" % (var_hostAnsible)
      if question("Do you want to access with user 'root' and configure it automatically?", "y", 3) == "y":
	# Calling setupNode.py
	print "Configuring node..."
	retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,var_hostAnsible,var_sshUserNodes), shell=True)
	if retCode != 0:
	  print >> sys.stderr, "Configuration error."
	  sys.exit(4) 
	else:
	  print
      else:
	print "You will have to access and configure it manually."
        sys.exit(5)

    # Check SO
    print "Checking SO..."
    retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s ansible" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
    if retSOCode != 0:
      print >> sys.stderr, "ERROR: Operating System not permitted"
      sys.exit(6)

    print "Everything is OK"
    print


    ###### Subnets ######
    var_subnets = getValueFromFile(configFile, 'subnets:', ':')
    def_subnets = var_subnets
    if not var_subnets:
      var_subnets = "%s/32" % (var_hostAnsible)

    correct = False
    count = 0
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
          sys.exit(7)


    ###### Exclude (IPs) ######
    var_exclude = getValueFromFile(configFile, 'exclude:', ':')
    def_exclude = var_exclude

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('IPs to be excluded (separated by white spaces): ', var_exclude)
      if inputValue.strip():
        # Splitting in IPs
        arr = inputValue.split(' ')
        correct = True
        for IP in arr:
          # Checking syntax IP
          if not checkIP(IP):
            correct = False
            print >> sys.stderr, "ERROR: IP %s Syntax error!!!" % (IP)
            print >> sys.stderr
        if correct:
          if var_hostAnsible not in arr:
            var_exclude = inputValue.strip()
            print "Everything is OK"
            print
          else:
            correct = False
            print >> sys.stderr, "ERROR: Ansible Host (%s) musn't be excluded (%s)" % (var_hostAnsible,inputValue.strip())
            print

      else:
	var_exclude = inputValue.strip()
	correct = True
        print "No IPs excluded"
        print

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(8)

    # Always exclude localhost
    if not "127.0.0.1" in var_exclude:
      var_exclude = ("127.0.0.1 " + var_exclude).strip()
 

    ###### Mysql Host ######
    var_hostMysql = getValueFromFile(configFile, 'hostMysql:', ':')
    def_hostMysql = var_hostMysql
    if not var_hostMysql:
      var_hostMysql = var_hostAnsible

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Mysql Host (IP): ', var_hostMysql)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible:
	  # Checking syntax IP
	  if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
	      # Checking if IP is excluded
	      if not IPInList(inputValue,var_exclude):
	        # Checking IP Ansible access
		retry = 0
	        if not accessIP(inputValue, var_sshUserNodes):
                  print >> sys.stderr, "ERROR: No ansible access to IP!!!"
                  if question("Do you want to access with user 'root' and configure it automatically?", "y", 3) == "y":
                    # Calling setupNode.py
                    print "Configuring node..."
                    retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,inputValue,var_sshUserNodes), shell=True)
	            if retCode != 0:
		      print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually."
		      print >> sys.stderr
		    else:
		      retry = 1

                  else:
                    print "You will have to access and configure it manually."
	            print

		else:
                  correct = True
                  var_hostMysql = inputValue.strip()
                  print "Everything is OK"
                  print

	        if retry and accessIP(inputValue, var_sshUserNodes):
	          # Check SO
                  print "Checking SO..."
	          retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s mysql" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))	
	          if retSOCode == 0:
	            correct = True
	            var_hostMysql = inputValue.strip()
	            print "Everything is OK"
	            print
	          else:
	            print >> sys.stderr, "ERROR: Operating System not permitted"
	            print >> sys.stderr

	      else:
                print >> sys.stderr, "ERROR: IP (%s) is in excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

            else:
              print >> sys.stderr, "ERROR: IP (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

	  else:
	    print >> sys.stderr, "ERROR: IP Syntax error!!!"
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
        sys.exit(9)


    ###### Nagios Host ######
    var_hostNagios = getValueFromFile(configFile, 'hostNagios:', ':')
    def_hostNagios = var_hostNagios
    if not var_hostNagios:
      var_hostNagios = var_hostMysql

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Nagios Host (IP): ', var_hostNagios)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking IP Ansible access
		retry = 0
                if not accessIP(inputValue, var_sshUserNodes):
	          print >> sys.stderr, "ERROR: No ansible access to IP!!!"
                  if question("Do you want to access with user 'root' and configure it automatically?", "y", 3) == "y":
                    # Calling setupNode.py
                    print "Configuring node..."
                    retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,var_hostNagios,var_sshUserNodes), shell=True)
                    if retCode != 0:
                      print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually."
		      print >> sys.stderr
		    else:
		      retry = 1

                  else:
                    print "You will have to access and configure it manually."
	            print

                else:
                  correct = True
                  var_hostMysql = inputValue.strip()
                  print "Everything is OK"
                  print

                if retry and accessIP(inputValue, var_sshUserNodes):
                  # Check SO
                  print "Checking SO..."
                  retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s nagios" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                  if retSOCode == 0:
                    correct = True
                    var_hostNagios = inputValue.strip()
	            print "Everything is OK"
                    print
                  else:
                    print >> sys.stderr, "ERROR: Operating System not permitted"
	            print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP (%s) is in excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

	    else:
              print >> sys.stderr, "ERROR: IP (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

	  else:
	    print >> sys.stderr, "ERROR: IP Syntax error!!!"
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
        sys.exit(10)


    ###### Munin Host ######
    var_hostMunin = getValueFromFile(configFile, 'hostMunin:', ':')
    def_hostMunin = var_hostMunin
    if not var_hostMunin:
      var_hostMunin = var_hostNagios

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Munin Host (IP): ', var_hostMunin)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking IP Ansible access
		retry = 0
                if not accessIP(inputValue, var_sshUserNodes):
                  print >> sys.stderr, "ERROR: No ansible access to IP!!!"
                  if question("Do you want to access with user 'root' and configure it automatically?", "y", 3) == "y":
                    # Calling setupNode.py
                    print "Configuring node..."
                    retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,var_hostMunin,var_sshUserNodes), shell=True)
                    if retCode != 0:
                      print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually."
		      print >> sys.stderr
		    else:
		      retry = 1 

                  else:
                    print "You will have to access and configure it manually."
	            print

                else:
                  correct = True
                  var_hostMysql = inputValue.strip()
                  print "Everything is OK"
                  print

                if retry and accessIP(inputValue, var_sshUserNodes):
                  # Check SO
                  print "Checking SO..."
                  retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s munin" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                  if retSOCode == 0:
                    correct = True
                    var_hostMunin = inputValue.strip()
	            print "Everything is OK"
                    print
                  else:
                    print >> sys.stderr, "ERROR: Operating System not permitted"
	            print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP (%s) is in excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

	    else:
              print >> sys.stderr, "ERROR: IP (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP Syntax error!!!"
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
        sys.exit(11)


    ###### Web Host ######
    var_hostWeb = getValueFromFile(configFile, 'hostWeb:', ':')
    def_hostWeb = var_hostWeb
    if not var_hostWeb:
      var_hostWeb = var_hostMunin

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Web Host (IP): ', var_hostWeb)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios and inputValue.strip() != var_hostMunin:
          # Checking syntax IP
	  if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
	        # Checking IP Ansible access
		retry = 0
                if not accessIP(inputValue, var_sshUserNodes):
                  print >> sys.stderr, "ERROR: No ansible access to IP!!!"
                  if question("Do you want to access with user 'root' and configure it automatically?", "y", 3) == "y":
                    # Calling setupNode.py
                    print "Configuring node..."
                    retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,var_hostWeb,var_sshUserNodes), shell=True)
                    if retCode != 0:
                      print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually."
		      print >> sys.stderr
		    else:
		      retry = 1

                  else:
                    print "You will have to access and configure it manually."
	            print

                else:
                  correct = True
                  var_hostWeb = inputValue.strip()
                  print "Everything is OK"
                  print

                if retry and accessIP(inputValue, var_sshUserNodes):
                  # Check SO
                  print "Checking SO..."
                  retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s web" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                  if retSOCode == 0:
                    correct = True
                    var_hostWeb = inputValue.strip()
	            print "Everything is OK"
                    print
                  else:
                    print >> sys.stderr, "ERROR: Operating System not permitted"
	            print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP (%s) is in excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

	    else:
              print >> sys.stderr, "ERROR: IP (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP Syntax error!!!"
	    print >> sys.stderr

	else:
          correct = True
          var_hostWeb = inputValue.strip()
          print "Everything is OK"
          print

      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      count += 1
      if count > maxErrors:
        print sys.stderr, "Too many Errors. Exiting..."
        sys.exit(12)


    ###### Openvas Host ######
    var_hostOpenvas = getValueFromFile(configFile, 'hostOpenvas:', ':')
    def_hostOpenvas = var_hostOpenvas
    if not var_hostOpenvas:
      var_hostOpenvas = var_hostWeb

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Openvas Host (IP): ', var_hostOpenvas)
      if inputValue.strip():
	if inputValue.strip() != var_hostAnsible and inputValue.strip() != var_hostMysql and inputValue.strip() != var_hostNagios and inputValue.strip() != var_hostMunin and inputValue.strip() != var_hostWeb:
          # Checking syntax IP
          if checkIP(inputValue):
            # Checking if IP belongs to subnets
            if IPInNetworks(inputValue,var_subnets):
              # Checking if IP is excluded
              if not IPInList(inputValue,var_exclude):
                # Checking IP Ansible access
		retry = 0
                if not accessIP(inputValue, var_sshUserNodes):
                  print >> sys.stderr, "ERROR: No ansible access to IP!!!"
                  if question("Do you want to access with user 'root' and configure it automatically?", "y", 3) == "y":
                    # Calling setupNode.py
                    print "Configuring node..."
                    retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,var_hostOpenvas,var_sshUserNodes), shell=True)
                    if retCode != 0:
                      print >> sys.stderr, "Configuration error. Try again (if authentication error) or configure it manually."
                      print >> sys.stderr
		    else:
		      retry = 1

                  else:
                    print "You will have to access and configure it manually."
                    print

                else:
                  correct = True
                  var_hostOpenvas = inputValue.strip()
                  print "Everything is OK"
                  print

                if retry and accessIP(inputValue, var_sshUserNodes):
                  # Check SO
                  print "Checking SO..."
                  retSOCode = subprocess.call("%s/scripts/checkSO.py %s %s openvas" % (pathAnsible,inputValue,var_sshUserNodes), shell=True, stdout=open('/dev/null','w'))
                  if retSOCode == 0:
                    correct = True
                    var_hostOpenvas = inputValue.strip()
                    print "Everything is OK"
                    print
                  else:
                    print >> sys.stderr, "ERROR: Operating System not permitted"
                    print >> sys.stderr

              else:
                print >> sys.stderr, "ERROR: IP (%s) is in excluded list (%s)" % (inputValue,var_exclude)
                print >> sys.stderr

            else:
              print >> sys.stderr, "ERROR: IP (%s) doesn't belong to any subnet (%s)" % (inputValue,var_subnets)
              print >> sys.stderr

          else:
            print >> sys.stderr, "ERROR: IP Syntax error!!!"
            print >> sys.stderr

	else:
          correct = True
          var_hostOpenvas = inputValue.strip()
          print "Everything is OK"
          print

      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      count += 1
      if count > maxErrors:
        print sys.stderr, "Too many Errors. Exiting..."
        sys.exit(13)


    ###### Password Openvas user ######
    var_passwdOpenvas = getValueFromFile(configFile, 'passwdOpenvas:', ':')
    def_passwdOpenvas = var_passwdOpenvas
    if not var_passwdOpenvas:
      var_passwdOpenvas = "jjzubi"

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Password Openvas user: ', var_passwdOpenvas)
      if inputValue:
        correct = True
        var_passwdOpenvas = inputValue
        print
        continue
      else:
        print >> sys.stderr, "ERROR: No value"
        pritn >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(14)


    ###### Password Mysql user root ######
    var_passwdMysqlRoot = getValueFromFile(configFile, 'passwdMysqlRoot:', ':')
    def_passwdMysqlRoot = var_passwdMysqlRoot
    if not var_passwdMysqlRoot:
      var_passwdMysqlRoot = var_passwdOpenvas 

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Password Mysql user root: ', var_passwdMysqlRoot)
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
        sys.exit(15)


    ###### Password Mysql user inventory ######
    var_passwdMysqlInventory = getValueFromFile(configFile, 'passwdMysqlInventory:', ':')
    def_passwdMysqlInventory = var_passwdMysqlInventory
    if not var_passwdMysqlInventory:
      var_passwdMysqlInventory = var_passwdMysqlRoot

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Password Mysql user inventory: ', var_passwdMysqlInventory)
      if inputValue:
        correct = True
	var_passwdMysqlInventory = inputValue
	print
	continue
      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(16)


    ###### Password Web user admin ######
    var_passwdWebAdmin = getValueFromFile(configFile, 'passwdWebAdmin:', ':')
    def_passwdWebAdmin = var_passwdWebAdmin
    if not var_passwdWebAdmin:
      var_passwdWebAdmin = var_passwdMysqlInventory 

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Password Web user admin: ', var_passwdWebAdmin)
      if inputValue:
        correct = True
        var_passwdWebAdmin = inputValue
        print
        continue
      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(17)


    ###### Hosts Admins ######
    var_hostsAdmins = getValueFromFile(configFile, 'hostsAdmins:', ':')
    def_hostsAdmins = var_hostsAdmins
    if not var_hostsAdmins:
      var_hostsAdmins = var_hostAnsible

    correct = False
    count = 0
    while not correct:
      inputValue = raw_input_def('Hosts administrators (IPs separated by white spaces): ', var_hostsAdmins)
      if inputValue.strip():
        # Splitting in IPs
        arr = inputValue.split(' ')
        correct = True
	for IP in arr:
	  # Checking syntax IP 
          if not checkIP(IP):
	    correct = False
	    print >> sys.stderr, "ERROR: IP %s Syntax error!!!" % (IP)
	    print >> sys.stderr
	if correct:
          var_hostsAdmins = inputValue.strip()
	  print "Everything is OK"
          print
      else:
        print >> sys.stderr, "ERROR: No value"
	print >> sys.stderr

      if not correct:
	count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(18)


    ###### Frequency Installation ######
    var_cronInstall = getValueFromFile(configFile, 'cronInstall:', ':').replace('|',':')
    def_cronInstall = var_cronInstall
    if not var_cronInstall:
      var_cronInstall = "3" 

    correct = False
    count = 0
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
          sys.exit(19)


    ###### Frequency Outsiders ######
    var_cronOutsiders = getValueFromFile(configFile, 'cronOutsiders:', ':').replace('|',':')
    def_cronOutsiders = var_cronOutsiders
    if not var_cronOutsiders:
      var_cronOutsiders = "4"

    correct = False
    count = 0
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
	  sys.exit(20)


    ###### Frequency Openvas ######
    var_cronOpenvas = getValueFromFile(configFile, 'cronOpenvas:', ':')
    def_cronOpenvas = var_cronOpenvas
    if not var_cronOpenvas:
      var_cronOpenvas = "2"

    correct = False
    count = 0
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
          sys.exit(21)


    ###### Frequency Nodes ######
    var_cronNodes = getValueFromFile(configFile, 'cronNodes:', ':').replace('|',':')
    def_cronNodes = var_cronNodes
    if not var_cronNodes:
      var_cronNodes = "2"

    correct = False
    count = 0
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
          sys.exit(22)


    ###### Frequency Nodes (Packages) ######
    var_cronNodesPackages = getValueFromFile(configFile, 'cronNodesPackages:', ':').replace('|',':')
    def_cronNodesPackages = var_cronNodesPackages
    if not var_cronNodesPackages:
      var_cronNodesPackages = "6"

    correct = False
    count = 0
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
	  sys.exit(23)


    ###### Frequency Nodes (Executables) ######
    var_cronNodesExes = getValueFromFile(configFile, 'cronNodesExes:', ':').replace('|',':')
    def_cronNodesExes = var_cronNodesExes
    if not var_cronNodesExes:
      var_cronNodesExes = "24"

    correct = False
    count = 0
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
          sys.exit(24)


    ###### Adding Nodes ######
    # Repeat loop until user decide to finish ('again' variable)
    again = question("Do you want to configure hosts as nodes (ssh connection with 'root' required)?", "n", 3)
    while again == "y":
      # Ask host name or IP
      print
      try:
        host = raw_input('Hostname or IP: ')
      except KeyboardInterrupt:
        host = ""

      if host:
        print
        try:
          retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,host,var_sshUserNodes), shell=True)
        except KeyboardInterrupt:
          retCode = 1

      else:
        print >> sys.stderr, "You have to introduce a name or IP"
        print >> sys.stderr

      # Configure another host?
      print
      again = question("Do you want to configure another host?", "n", 3)


    ##### Checking Windows Hosts? #####
    var_winNodes = getValueFromFile(configFile, 'winNodes:', ':')
    def_winNodes = var_winNodes
    if var_winNodes != "y" and var_winNodes != "n":
      var_winNodes = "n"

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
          sys.exit(25)


    ###### Password Windows User Nodes ######
    if var_winNodes == "y":
      var_winPasswdNodes = getValueFromFile(configFile, 'winPasswdNodes:', ':')
      def_winPasswdNodes = var_winPasswdNodes
      if not var_winPasswdNodes:
        var_winPasswdNodes = "jjzubi"

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
          sys.exit(26)


    ###### Frequency WinNodes ######
    if var_winNodes == "y":
      var_winCronNodes = getValueFromFile(configFile, 'winCronNodes:', ':').replace('|',':')
      def_winCronNodes = var_winCronNodes
      if not var_winCronNodes:
        var_winCronNodes = "4"

      correct = False
      count = 0
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
            sys.exit(27)


    ###### SUMMARY ######
    print
    print "---------------------------------------"
    print "          Main Configuration           "
    print "---------------------------------------"
    print "Host local (host Ansible): %s (%s)" % (var_hostAnsible,IPtoName(var_hostAnsible))
    print "Subnets: %s" % (var_subnets)
    print "Exclude: %s" % (var_exclude)
    print "Host Mysql: %s (%s)" % (var_hostMysql,IPtoName(var_hostMysql))
    print "Host Nagios: %s (%s)" % (var_hostNagios,IPtoName(var_hostNagios))
    print "Host Munin: %s (%s)" % (var_hostMunin,IPtoName(var_hostMunin))
    print "Host Web: %s (%s)" % (var_hostWeb,IPtoName(var_hostWeb))
    print "Host Openvas: %s (%s)" % (var_hostOpenvas,IPtoName(var_hostOpenvas))
    print "Remote User (nodes): %s with sudo='%s'" % (var_sshUserNodes,var_sudoUserNodes)
    print "Password Openvas user: %s" % (var_passwdOpenvas)
    print "Password Mysql user root: %s" % (var_passwdMysqlRoot)
    print "Password Mysql user inventory: %s" % (var_passwdMysqlInventory)
    print "Password Web user admin: %s" % (var_passwdWebAdmin)
    print "Hosts administrators: %s" % (var_hostsAdmins)
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
    print "---------------------------------------"
    print



    if question("Config and Start?", "y", 3) == "y":
      print "Generating Production File..."
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
        f.write("# Password Openvas user\n")
        f.write("passwdOpenvas: %s\n" % (var_passwdOpenvas))
        f.write("\n")
        f.write("# Password Mysql user root\n")
	f.write("passwdMysqlRoot: %s\n" % (var_passwdMysqlRoot))
	f.write("\n")
	f.write("# Password Mysql user inventory\n")
	f.write("passwdMysqlInventory: %s\n" % (var_passwdMysqlInventory))
	f.write("\n")
        f.write("# Password Web user admin\n")
        f.write("passwdWebAdmin: %s\n" % (var_passwdWebAdmin))
        f.write("\n")
        f.write("# Hosts Administrators\n")
        f.write("hostsAdmins:\n")
        arr = var_hostsAdmins.split(' ')
        for x in arr:
          f.write("- %s\n" % (x))
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
	  f.write("%s" % (line))

	extra.close()
	f.close()
        print "Generated."
        print

      except:
        print >> sys.stderr, "Error opening file: %s" % (productionFileTmp)
        sys.exit(28)

      print "Updating Production File..."
      try:
        # Backup Production file
        print "Backup of Production file as '.back'" 
        shutil.copy(productionFile, "%s.back" % (productionFile))
        # Move Temp file to Production file
        print "Moving from Temp to Production..."
        shutil.move(productionFileTmp, productionFile)
        print "Done."
        print
      except:
        print >> sys.stderr, "Error updating Production file."
        sys.exit(29)      
  
      print "Updating Config file..."
      try:
        f = open(configFile, 'w')

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
        f.write("subnets: %s\n" % (var_subnets))
        f.write("\n")
        f.write("# Exclude\n")
        f.write("exclude: %s\n" % (var_exclude))
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
        f.write("# Password Openvas user\n")
        f.write("passwdOpenvas: %s\n" % (var_passwdOpenvas))
        f.write("\n")
        f.write("# Password Mysql user root\n")
        f.write("passwdMysqlRoot: %s\n" % (var_passwdMysqlRoot))
        f.write("\n")
        f.write("# Password Mysql user inventory\n")
        f.write("passwdMysqlInventory: %s\n" % (var_passwdMysqlInventory))
        f.write("\n")
        f.write("# Password Web user admin\n")
        f.write("passwdWebAdmin: %s\n" % (var_passwdWebAdmin))
        f.write("\n")
        f.write("# Hosts Administrators\n")
        f.write("hostsAdmins: %s\n" % (var_hostsAdmins))
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

        f.close()
        print "Done."
        print

      except:
        print >> sys.stderr, "Error updating Config file."
        print >> sys.stderr


      # Updating sudo
      print "Updating sudo..."
      for file in glob.glob("%s/*.yml" % (pathAnsible)):
	print "File: %s..." % (file)
     	if var_sudoUserNodes == "no":
	  subprocess.call("sed -i 's/become:\s*\([yY]es\|[tT]rue\)/become: no/g' %s" % (file), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)	
	else:
	  subprocess.call("sed -i 's/become:\s*\([nN]o\|[fF]alse\)/become: yes/g' %s" % (file), shell=True, stdout=open('/dev/null','w'), stderr=subprocess.STDOUT)
      print "Done."
      print


      # Updating Inventory
      print "Updating inventory..."
      try:
        invAnsible = open(inventoryAnsible, 'w') 
        invMysql = open(inventoryMysql, 'w')
        invNagios = open(inventoryNagios, 'w')
        invMunin = open(inventoryMunin, 'w')
        invWeb = open(inventoryWeb, 'w')
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
	if var_hostOpenvas != var_hostAnsible and var_hostOpenvas != var_hostMysql and var_hostOpenvas != var_hostNagios and var_hostOpenvas != var_hostMunin and var_hostOpenvas != var_hostWeb:
          invServers.write("%s\n" % (IPtoName(var_hostOpenvas)))
        invServers.write("\n")


        invAnsible.close()
	invMysql.close()
	invNagios.close()
	invMunin.close()
	invWeb.close()
	invOpenvas.close()
  	invServers.close()

        print "Done."
        print

      except:
        print >> sys.stderr, "Error updating inventory."
        # Restoring Production File from backup 
        print >> sys.stderr, "Restoring Production file from backup..."
        shutil.copy("%s.back" % (productionFile), productionFile)
        print >> sys.stderr, "Done."
        sys.exit(30)  


      # Calling Playbooks
      print
      print "Calling Playbooks..."
      print

      # Deleting Ansible crontab entries 
      print "Deleting Ansible crontab entries..."
      print 
      subprocess.call("ansible-playbook %s/ansible.yml -t cronStop -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True) 
      print 
      print "Done."
      print 

      # Installing Ansible
      if var_hostAnsible != def_hostAnsible:
        print "Configuring Ansible server..."
        print 
        retCode = subprocess.call("ansible-playbook %s/ansible.yml -t install,config -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(31)
        print 
        print "Done."
        print 

      # Installing Mysql Server 
      if var_hostMysql != def_hostMysql or var_passwdMysqlRoot != def_passwdMysqlRoot or var_passwdMysqlInventory != def_passwdMysqlInventory:
        print "Configuring Mysql Server..."
        print 
        retCode = subprocess.call("ansible-playbook %s/mysql.yml -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again" 
          sys.exit(32)
        print 
        print "Done."
        print 

      # Installing Web Server 
      if var_hostWeb != def_hostWeb or var_passwdWebAdmin != def_passwdWebAdmin or var_hostsAdmins != def_hostsAdmins:
        print "Configuring Web Server..."
        print 
        retCode = subprocess.call("ansible-playbook %s/web.yml -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(33)
        print 
        print "Done."
        print 

      # Installing Munin Server 
      if var_hostMunin != def_hostMunin:
        print "Configuring Munin Server..."
        print 
        retCode = subprocess.call("ansible-playbook %s/munin.yml -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(34)
        print 
        print "Done."
        print 

      # Installing Nagios Server
      if var_hostNagios != def_hostNagios:
        print "Configuring Nagios Server..."
        print
        retCode = subprocess.call("ansible-playbook %s/nagios.yml -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(35)
        print 
        print "Done."
        print

      # Installing Openvas Server
      if var_hostOpenvas != def_hostOpenvas or var_passwdOpenvas != def_passwdOpenvas:
        print "Configuring Openvas Server..."
        print
        retCode = subprocess.call("ansible-playbook %s/openvas.yml -t install,config -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(36)
        print
        print "Done."
        print

      # Scanning Networks to discover hosts (nodes and outsiders)
      if var_subnets != def_subnets or var_exclude != def_exclude:
        print "Scanning Networks to discover hosts (nodes and outsiders)..."
        print
        retCode = subprocess.call("ansible-playbook %s/outsiders.yml -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(37)
        print
        print "Done."
        print

      # Installing software nodes
      if var_subnets != def_subnets or var_exclude != def_exclude or var_hostNagios != def_hostNagios or var_hostMunin != def_hostMunin:
        print "Configuring Nodes..."
        print
        retCode = subprocess.call("ansible-playbook %s/nodes.yml -t install -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(38)
        print
        print "Done."
        print

      # Getting basic data from nodes
      if var_subnets != def_subnets or var_exclude != def_exclude or var_hostNagios != def_hostNagios or var_hostMunin != def_hostMunin or var_hostMysql != def_hostMysql or var_hostAnsible != def_hostAnsible:
        print "Getting basic data from nodes..."
        print
        retCode = subprocess.call("ansible-playbook %s/nodes.yml -t dataDB -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True) 
        if retCode != 0:
          print >> sys.stderr, "Error!!! Solve the problem and configure again"
          sys.exit(39)
        print
        print "Done."
        print

      if var_winNodes == "y":
        # Getting data from windows node
        if var_subnets != def_subnets or var_exclude != def_exclude or var_hostNagios != def_hostNagios or var_hostMunin != def_hostMunin or var_hostMysql != def_hostMysql or var_hostAnsible != def_hostAnsible:
          print "Getting data from windows nodes..."
          print
          retCode = subprocess.call("ansible-playbook %s/winNodes.yml" % (pathAnsible), shell=True)
          if retCode != 0:
            print >> sys.stderr, "Error!!! Solve the problem and configure again"
            sys.exit(40)
          print
          print "Done."
          print

      # Adding Ansible crontab entries
      print "Adding Ansible crontab entries..."
      print
      subprocess.call("ansible-playbook %s/ansible.yml -t cronStart -u %s -s" % (pathAnsible,var_sshUserNodes), shell=True)
      print
      print "Done."
      print

    else:
      print "Cancelled."
      print



if __name__ == '__main__':
	    main()

