#!/usr/bin/python

import subprocess
import sys
import os
import readline


# Configuration Files
pathAnsible = "/etc/ansible"
pathConfig = "%s/group_vars/all" % (pathAnsible)
pathDirectoryErrors = "/var/log/ansible"
pathFileErrors = "%s/errors.log" % (pathDirectoryErrors)
pathFileMysqlErrors = "%s/mysql-errors.log" % (pathDirectoryErrors)
pathFileExesList = "%s/summary.log" % (pathDirectoryErrors)
pathFilesSQL = "/root/inventory"
pathInventory = "%s/inventory" % (pathAnsible)
pathDataBaseSQL = "%s/roles/mysql/files/root/inventory/createTables.sql" % (pathAnsible)


def raw_input_def(prompt, default):
    def pre_input_hook():
        readline.insert_text(default)
        readline.redisplay()

    readline.set_pre_input_hook(pre_input_hook)
    try:
      return raw_input(prompt)
    finally:
      readline.set_pre_input_hook(None)


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


def printMenu():

    print "################ CONTROL MENU ###################"
    print "##                                             ##"
    print "##  0. Help                                    ##"
    print "##  1. (Re)Configure System                    ##"
    print "##  2. Configure Extra Variables               ##"
    print "##  3. Add Node(s)                             ##"
    print "##  4. Stop/Start/Restart System               ##"
    print "##  5. Scan Network                            ##"
    print "##  6. Install Node(s)                         ##"
    print "##  7. Get Data from Node(s)                   ##"
    print "##  8. Get Data from Windows Nodes             ##"
    print "##  9. Scan Vulnerabilities                    ##"
    print "##  e. Check System Errors                     ##"
    print "##  m. Check DB (SQL) Errors                   ##"
    print "##  c. Clean System & DB Errors                ##"
    print "##  l. List Servers & Nodes                    ##"
    print "##  s. View System Configuration               ##"
    print "##  x. View Executions List                    ##"
    print "##  r. Log Running Executions (CTRL+C to exit) ##"
    print "##  q. Quit Menu                               ##"
    print "##                                             ##"
    print "#################################################"


def selectOption():

    answer = None
    legal_answers = ['0','1','2','3','4','5','6','7', '8', '9', 'e', 'm', 'c', 'l', 's', 'x', 'r', 'q']
    tried = False
    while answer not in legal_answers:
        print "%s" % "Invalid input, select again" if tried else ""
        answer = raw_input('Select option: ')
        tried = True

    return answer


def execOption(opt):

    if opt == '0':
      ## Help Menu ##
      retCode = subprocess.call("%s/help.py" % (pathAnsible), shell=True)

    elif opt == '1':
      ## Configure System ##
      retCode = subprocess.call("%s/configure.py" % (pathAnsible), shell=True)

    elif opt == '2':
      ## Configure Extra variables ##
      retCode = subprocess.call("%s/configExtra.py" % (pathAnsible), shell=True)

    elif opt == '3':
      ## Configure hosts as nodes ##
      systemConfigured = "yes"
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if not sshUserNodes:
        systemConfigured = "no"
	# Ask ssh User
	print
	sshUserNodes = raw_input('System not configured yet. What user will you use? ')
      if sshUserNodes: 
        # Repeat loop until user decide to finish ('again' variable)
        again = "y"
	# This variable will be 0 if any of configurations is OK 
        retCodeTotal = 1 
        while again == "y":
	  # Ask host name or IP
	  print
	  try:
	    host = raw_input('Hostname or IP: ')
          except KeyboardInterrupt:
	    host = ""
            print
            print "Interrupted"
            print

	  if host:
	    print
            retCode = subprocess.call("%s/scripts/setupNode.py %s %s" % (pathAnsible,host,sshUserNodes), shell=True)
  	    retCodeTotal = retCodeTotal * retCode 
	  else:
	    print >> sys.stderr, "You have to introduce a name or IP"
	    print >> sys.stderr

	  # Configure another host?
          print
          again = question("Do you want to configure another host?", "n", 3)

	# If any of configurations was OK then will refresh inventory scanning subnets 
        if retCodeTotal == 0 and systemConfigured == "yes":
          print "Scanning subnet to add host to inventory..."
          retCode = subprocess.call("ansible-playbook %s/outsiders.yml -t dataDB; ansible-playbook %s/nodes.yml -t install" % (pathAnsible,pathAnsible), shell=True)
          print
	  
      else:
        print >> sys.stderr, "You have to introduce a ssh User"
        print >> sys.stderr

    elif opt == '4':
      ## Stop/Start/Restart System ##
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')      
      if sshUserNodes:
        try:
          operation = raw_input('Operation (stop, start or restart): ')

          if operation == "stop":
            # Stop System
            print
            print "ansible-playbook %s/ansible.yml -t cronStop" % (pathAnsible)
            print
            retCode = subprocess.call("ansible-playbook %s/ansible.yml -t cronStop" % (pathAnsible), shell=True)
          elif operation == "start":
            # Start System
            print
            print "ansible-playbook %s/ansible.yml -t cronStart" % (pathAnsible)
            print
            retCode = subprocess.call("ansible-playbook %s/ansible.yml -t cronStart" % (pathAnsible), shell=True)
          elif operation == "restart":
            # Start System
            print
            print "ansible-playbook %s/ansible.yml -t cronStop && ansible-playbook %s/ansible.yml -t cronStart" % (pathAnsible,pathAnsible)
            print
            retCode = subprocess.call("ansible-playbook %s/ansible.yml -t cronStop && ansible-playbook %s/ansible.yml -t cronStart" % (pathAnsible,pathAnsible), shell=True)

          else:
            print >> sys.stderr
            print >> sys.stderr, "Option %s not valid (Valid options: stop, start, or restart)" % (operation)
            print >> sys.stderr

        except KeyboardInterrupt:
          nodeName = ""
          print
          print "Interrupted"
          print

      else:
	print >> sys.stderr, "System not configured, select option 1"
	print >> sys.stderr

    elif opt == '5':
      ## Scan Network to discover nodes and outsiders ##
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        print
        print "ansible-playbook %s/outsiders.yml -t dataDB" % (pathAnsible) 
	retCode = subprocess.call("ansible-playbook %s/outsiders.yml -t dataDB" % (pathAnsible), shell=True)
      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == '6':
      ## Install nodes ##
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        # Ask hostname (fqdn)
        print
        try:
          nodeName = raw_input('Node (hostname) or All (enter): ').lower()

          if nodeName:
            nodeInventory = subprocess.Popen("(cat %s/nodes|grep -e '^%s$' -e '^%s\\.'|head -1) 2>/dev/null" % (pathInventory,nodeName,nodeName), shell=True, stdout=subprocess.PIPE).stdout.read()
            if nodeInventory != "":
              print
              print "ansible-playbook %s/nodes.yml -t install --limit %s" % (pathAnsible,nodeInventory)
              retCode = subprocess.call("ansible-playbook %s/nodes.yml -t install --limit %s" % (pathAnsible,nodeInventory), shell=True)
            else:
              print >> sys.stderr
              print >> sys.stderr, "Hostname %s is not a node" % (nodeName)
              print >> sys.stderr

          else:
            print
            print "ansible-playbook %s/nodes.yml -t install" % (pathAnsible)
            retCode = subprocess.call("ansible-playbook %s/nodes.yml -t install" % (pathAnsible), shell=True)

        except KeyboardInterrupt:
          nodeName = ""
          print
          print "Interrupted"
          print

      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == '7':
      ## Get data (basic|package|exe|all) from nodes ##
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        # Type of data: basic, packages, exes or all
        print
        typeList = raw_input('Getting data of basic, packages, exes or all (b/p/e/a): ')
        if typeList == 'b':
          paramData = '-t dataDB'
        elif typeList == 'p':
          paramData = '-t dataPackagesDB'
        elif typeList == 'e':
          paramData = '-t dataExesDB'
        elif typeList == 'a':
          paramData = ''
        else:
          # By default 'all'
          paramData = ''

        # Ask hostname (fqdn) 
        print
        try:
          nodeName = raw_input('Node (hostname) or All (enter): ').lower()

          if nodeName:
	    nodeInventory = subprocess.Popen("(cat %s/nodes|grep -e '^%s$' -e '^%s\\.'|head -1) 2>/dev/null" % (pathInventory,nodeName,nodeName), shell=True, stdout=subprocess.PIPE).stdout.read()
 	    if nodeInventory != "": 
              print
              print "ansible-playbook %s/nodes.yml %s --limit %s" % (pathAnsible,paramData,nodeInventory)
	      retCode = subprocess.call("ansible-playbook %s/nodes.yml %s --limit %s" % (pathAnsible,paramData,nodeInventory), shell=True)
	    else:
	      print >> sys.stderr
              print >> sys.stderr, "Hostname %s is not a node" % (nodeName)
              print >> sys.stderr
	  
          else:
            print
            print "ansible-playbook %s/nodes.yml %s" % (pathAnsible,paramData)
	    retCode = subprocess.call("ansible-playbook %s/nodes.yml %s" % (pathAnsible,paramData), shell=True) 

        except KeyboardInterrupt:
          nodeName = ""
          print
          print "Interrupted"
          print

      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == '8':
      ## Get data from windows nodes ##
      # Windows Nodes configured?
      winNodes = getValueFromFile(pathConfig, 'winNodes:', ':')
      if winNodes and winNodes == 'y':
        print
        print "ansible-playbook %s/winNodes.yml" % (pathAnsible)
        retCode = subprocess.call("ansible-playbook %s/winNodes.yml" % (pathAnsible), shell=True)

      else:
        print >> sys.stderr, "Windows Nodes not configured, select option 1"
        print >> sys.stderr

    elif opt == '9':
      ## Scan vulnerabilities (Openvas) ##
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        # Ask hostname List 
        print
        try:
          hostNameList = raw_input('Hosts List (separated by spaces) or All (enter): ').lower()	

          if hostNameList:
	    hostInventoryList = []
	    errorInventory = False 

	    for hostName in hostNameList.strip().split(' '):
              hostInventory = subprocess.Popen("(cat %s/*|grep -e '^%s$' -e '^%s\\.'|head -1) 2>/dev/null" % (pathInventory,hostName,hostName), shell=True, stdout=subprocess.PIPE).stdout.read().strip()
	      if hostInventory != "":
		hostInventoryList.append(hostInventory)
              else:
                print >> sys.stderr
                print >> sys.stderr, "Hostname %s is not in inventory" % (hostName)
                print >> sys.stderr
		errorInventory = True
		break 

	    if not errorInventory:
	      cadList = ','.join(hostInventoryList) 
	      cadList = '{\"Name\":\"%s\"}' % cadList
	      cadList = cadList.replace(',', '\"},{\"Name\":\"')
              print
              print "ansible-playbook %s/openvas.yml -t dataDB --extra-vars '{\"serversList\":[%s]}'" % (pathAnsible,cadList)
              retCode = subprocess.call("ansible-playbook %s/openvas.yml -t dataDB --extra-vars '{\"serversList\":[%s]}'" % (pathAnsible,cadList), shell=True)

          else:
            print
            print "ansible-playbook %s/openvas.yml -t dataDB" % (pathAnsible)
            retCode = subprocess.call("ansible-playbook %s/openvas.yml -t dataDB" % (pathAnsible), shell=True)

        except KeyboardInterrupt:
          nodeName = ""
          print
          print "Interrupted"
          print

      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == 'e': 
      ## Check errors file (System) ##
      # Check directory
      if os.path.isdir(pathDirectoryErrors):
	# Check errors file
	if os.access(pathFileErrors, os.R_OK):
          # Type of list: summary or details 
          print
          typeList = raw_input('There are errors. View summary or details (s/d): ')
	  if typeList == 's':
	    #retCode = subprocess.call("less %s|grep '###'" % (pathFileErrors), shell=True)
	    retCode = subprocess.call("grep -h -e '### ' -e '^fatal: ' -e '^failed: ' %s|sed '/### /{x;p;x;G;}'|sed '/^fatal:/G'|sed '/^failed:/G'|less" % (pathFileErrors), shell=True)
	    print
	  elif typeList == 'd':
            retCode = subprocess.call("less %s" % (pathFileErrors), shell=True)
	    print
	  else:
	    print >> sys.stderr, "Error: available options 's' (summary) or 'd' (details)"
            print >> sys.stderr
	else:
	  print
	  print "No errors"
	  print
      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == 'm':
      ## Check errors file (DB) ##
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      # Get hostMysql value
      hostMysql = getValueFromFile(pathConfig, 'hostMysql:', ':')     
      if sshUserNodes and hostMysql: 
        print
        print "Checking mysql file errors in Mysql Server..."
        # Check directory 
        retCodeDir = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo ls -ld %s' > /dev/null 2> /dev/null" % (hostMysql,sshUserNodes,pathDirectoryErrors), shell=True)
        if retCodeDir == 0:
          # Check file
          retCodeFile = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo ls -l %s' > /dev/null 2> /dev/null" % (hostMysql,sshUserNodes,pathFileMysqlErrors), shell=True)
          if retCodeFile == 0:
            # Type of list: summary or details
            print
            typeList = raw_input('There are errors. View summary or details (s/d): ')
            if typeList == 's':
              retCode = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo cat %s'|grep '###'|less" % (hostMysql,sshUserNodes,pathFileMysqlErrors), shell=True)
              print
            elif typeList == 'd':
              retCode = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo cat %s'|less" % (hostMysql,sshUserNodes,pathFileMysqlErrors), shell=True)
              print
            else:
              print >> sys.stderr, "Error: available options 's' (summary) or 'd' (details)"
              print >> sys.stderr
          else:
            print
            print "No errors"
            print
        else:
          print >> sys.stderr, "System not configured, select option 1"
          print >> sys.stderr
      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == 'c':
      ## Clean System & DB errors files ##
      ## System Errors ##
      # Check directory
      if os.path.isdir(pathDirectoryErrors):
        # Check errors file
        if os.access(pathFileErrors, os.R_OK):
          # Delete file
          retCode = subprocess.call("rm -f %s" % (pathFileErrors), shell=True)
          if retCode == 0:
            print 
            print "System Errors file deleted." 
            print
          else:
            print >> sys.stderr, "Error deleting errors file (System)"
            print >> sys.stderr
        else:
          print
          print "No errors (System)"
          print

        ## DB Errors ##
        # Get sshUserNodes value
        sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
        # Get hostMysql value
        hostMysql = getValueFromFile(pathConfig, 'hostMysql:', ':')
        if sshUserNodes and hostMysql:
          # Check directory
          retCodeDir = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo ls -ld %s' > /dev/null 2> /dev/null" % (hostMysql,sshUserNodes,pathDirectoryErrors), shell=True)
          if retCodeDir == 0:
            # Check file
            retCodeFile = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo ls -l %s' > /dev/null 2> /dev/null" % (hostMysql,sshUserNodes,pathFileMysqlErrors), shell=True)
            if retCodeFile == 0:
              # Delete file 
              retCode = subprocess.call("ansible all -i %s, -u %s -s -m shell -a 'sudo rm -f %s; find %s -type f -name \"*.sql.error\" -exec rm -f {} \;' > /dev/null 2> /dev/null" % (hostMysql,sshUserNodes,pathFileMysqlErrors,pathFilesSQL), shell=True)
              if retCode == 0:
                print "DB Errors file deleted."
                print
              else:     
                print >> sys.stderr, "Error deleting errors file (DB)"
                print >> sys.stderr
            else:
              print "No errors (DB)"
              print
          else:
            print >> sys.stderr, "System not configured, select option 1"
            print >> sys.stderr
        else:
          print >> sys.stderr, "System not configured, select option 1"
          print >> sys.stderr
      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr


    elif opt == 'l':
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        ## List of servers & nodes ##
        if os.access("%s/ansible" % (pathInventory), os.R_OK) and os.access("%s/mysql" % (pathInventory), os.R_OK) and os.access("%s/web" % (pathInventory), os.R_OK) and os.access("%s/nagios" % (pathInventory), os.R_OK) and os.access("%s/munin" % (pathInventory), os.R_OK) and os.access("%s/openvas" % (pathInventory), os.R_OK) and os.access("%s/nodes" % (pathInventory), os.R_OK) and os.access("%s/winNodes" % (pathInventory), os.R_OK) and os.access("%s/outsiders" % (pathInventory), os.R_OK):
          retCode = subprocess.call("cat %(path)s/ansible %(path)s/mysql %(path)s/web %(path)s/nagios %(path)s/munin %(path)s/openvas %(path)s/nodes %(path)s/winNodes %(path)s/outsiders | less" % { 'path': pathInventory }, shell=True)
          print
        else:
          print >> sys.stderr, "System not configured, select option 1"
          print >> sys.stderr
      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == 's':
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        ## View system configuration (variables) ##
        if os.access(pathConfig, os.R_OK):
          retCode = subprocess.call("less %s" % (pathConfig), shell=True)
          print
        else:
          print >> sys.stderr, "System not configured, select option 1"
          print >> sys.stderr     
      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == 'x':
      ## View executions List of Ansible ##
      # Check directory
      if os.path.isdir(pathDirectoryErrors):
        # Check errors file
        if os.access(pathFileExesList, os.R_OK):
          retCode = subprocess.call("less %s" % (pathFileExesList), shell=True)
          print
        else:
          print
          print "No executions"
          print

      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    elif opt == 'r':
      ## View Log running executions 
      # Get sshUserNodes value
      sshUserNodes = getValueFromFile(pathConfig, 'sshUserNodes:', ':')
      if sshUserNodes:
        totalExes = int(subprocess.Popen("(ls -la %s/.*.tmp|awk '{print $6,$7,$8,$5,substr($9,length(\"%s\")+2)}'|wc -l) 2> /dev/null" % (pathDirectoryErrors,pathDirectoryErrors), shell=True, stdout=subprocess.PIPE).stdout.read())
	if totalExes > 0:
          # List running executions
	  print
          print "List of running executions"
          print
	  exes = [""] 
	  countExes = 1
          for lineExes in subprocess.Popen("ls -la %s/.*.tmp|awk '{print $6,$7,$8,$5,substr($9,length(\"%s\")+2)}' 2> /dev/null" % (pathDirectoryErrors,pathDirectoryErrors), shell=True, stdout=subprocess.PIPE).stdout.readlines():
	    print "(%s) %s" %(countExes,lineExes)
	    exes.append(lineExes.split(' ')[4].strip()) 
	    countExes += 1

          # Ask execution (number) 
          try:
	    print
	    correct = False
	    count = 0
            inputValue = raw_input('Number Execution or ALL (enter): ')
	       
	    if inputValue:
	      try:
		numberExe = int(inputValue)
	      except:
		numberExe = ""

	      if numberExe <= 0 or numberExe > totalExes:
		numberExe = ""

	    else:
	      numberExe = ""
		
          except KeyboardInterrupt:
            numberExe = ""

	else:
	  numberExe = ""

	# Selecting Log File
	if numberExe != "":
          try:
            retCode = subprocess.call("echo; echo '%s LOGS'; echo; grep '^TASK ' %s/%s; echo; tail -f %s/%s" % (exes[int(numberExe)],pathDirectoryErrors,exes[int(numberExe)],pathDirectoryErrors,exes[int(numberExe)]), shell=True)
          except KeyboardInterrupt:
            print
	else:
          print
          print "No log files"
          print

      else:
        print >> sys.stderr, "System not configured, select option 1"
        print >> sys.stderr

    else:
      print "Option %s not valid" % (opt)

    raw_input("Press Enter to show Control Menu ") 



def main():

    option = '-1'

    while option != 'q':
      try:
        os.system("clear")
        print
        printMenu()
        option = selectOption() 
        if option != 'q':
          execOption(option)

      except KeyboardInterrupt:
	option = 'q'
	print
	print "Interrupted"
	print

    print 
    print "Bye"
    print
    sys.exit(0)



if __name__ == '__main__':
	    main()

