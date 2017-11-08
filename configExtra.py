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

# Config Scan Openvas
configScanOpenvasOptions = [ "Discovery", "Host Discovery", "System Discovery", "Full and fast", "Full and fast ultimate", "Full and very deep", "Full and very deep ultimate" ]

# Frequency Range
frequencyRangeMinutes = "5 6 10 12 15 20 30 60"

# Max Errors
maxErrors = 3



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
          if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
          elif value.startswith("\"") and value.endswith("\""):
            value = value[1:-1] 

    return value


def isInt(cad):
    try: 
        int(cad)
        return True
    except ValueError:
        return False


def inRange(value,min,max):
    try:
	if isInt(value) and isInt(min) and isInt(max) and (int(min) <= int(value) <= int(max)): 
            return True
	else:
	    return False
    except:
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


def checkFrequency(value,range):
    # Checking frequency
    rangeList = range.split(' ')
    if value in rangeList:
        return True
    else:
        return False


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


def checkCronField(cad,type):
    try:
	# Max and Min values
	if type == "minute":
	    minVal=0
	    maxVal=59
	elif type == "hour":
            minVal=0
            maxVal=23
        elif type == "day":
            minVal=1
            maxVal=31
        elif type == "month":
            minVal=1
            maxVal=12
        elif type == "weekday":
            minVal=1
            maxVal=7
	else:
	    return False

	# Checking field
    	if cad == "*":
            return True
    	elif inRange(cad,minVal,maxVal):
	    return True
    	elif cad.startswith("*/"):
	    if inRange(cad.split('/',1)[1],minVal,maxVal):
	    	return True
	    else:
		return False
    	elif "," in cad:
	    arrValues = cad.split(',')
	    for val in arrValues:
	    	if not (isInt(val) and inRange(val,minVal,maxVal)):
		    return False
	    return True
	elif "-" in cad:
	    arrValues = cad.split('-',1)
	    if not inRange(arrValues[0],minVal,maxVal):
		return False
            if not inRange(arrValues[1],minVal,maxVal):
                return False
	    return True
    	else:
	    return False

    except:
	return False




def main():

  try:

    # Clear screen
    os.system("clear")

    ###### ssh User ######
    var_sshUserNodes = getValueFromFile(configFile, 'sshUserNodes:', ':')
    # Check if system is has been configured
    if not var_sshUserNodes:
      print >> sys.stderr, "System not configured, select option 1"
      print >> sys.stderr
      sys.exit(1)


    # Variable to control reload configuration
    reload = False

    # System configuration
    print "########################################"
    print "      Extra variables Configuration     "
    print "########################################"
    print

    ###### Read Only User ######
    print
    print "----------------------------------------------------"
    print "A read only user can be created to access all server"
    print "Leave empty to not create"
    print "----------------------------------------------------"
    print

    var_readUser = getValueFromFile(configExtra, 'readUser:', ':')
    def_readUser = var_readUser
    if not var_readUser:
      var_readUser = ""

    inputValue = raw_input_def('Read Only User to access all servers (leave empty to not create): ', var_readUser)
    var_readUser = inputValue.strip()
    print


    ##### Password Read Only User #####
    if var_readUser != "":
      var_passwdReadUser = getValueFromFile(configExtra, 'passwdReadUser:', ':')
      def_passwdReadUser = var_passwdReadUser
      if not var_passwdReadUser:
        var_passwdReadUser = var_readUser 

      correct = False
      count = 0
      print
      print "--------------------------"
      print "Password of read only user"
      print "--------------------------"
      print
      while not correct:
        inputValue = raw_input_def('Password Read Only User: ', var_passwdReadUser)
        if inputValue:
          correct = True
          var_passwdReadUser = inputValue
          print
          continue
        else:
          print >> sys.stderr, "ERROR: No value"
          print >> sys.stderr

        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(2)


      ###### Hosts Read User ######
      var_hostsReadUser = getValueFromFile(configExtra, 'hostsReadUser:', ':')
      if var_hostsReadUser == "''":
        var_hostsReadUser = ""
      def_hostsReadUser = var_hostsReadUser

      correct = False
      count = 0
      print
      print "-----------------------------------------------------"
      print "Read Only User Hosts (allowed to acccess all Servers)"
      print "Leave empty to permit access from everywhere"
      print "-----------------------------------------------------"
      print
      while not correct:
        inputValue = raw_input_def('Hosts Read Only User (IP addresses separated by white spaces): ', var_hostsReadUser)
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
          var_hostsReadUser = inputValue.strip()
          print "Everything is OK"
          print


        if not correct:
          count += 1
          if count > maxErrors:
            print >> sys.stderr, "Too many Errors. Exiting..."
            sys.exit(3)


    ###### Path Inventory Directory ######
    var_pathInventoryDirectory = getValueFromFile(configExtra, 'pathInventoryDirectory:', ':')
    if not var_pathInventoryDirectory:
      var_pathInventoryDirectory = "/root/inventory"

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Mysql Server stores SQL files (with data collected) on a temporal directory, to "
    print "execute them and insert or update data on database"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Path Inventory Directory (directory to generate and execute SQL files): ', var_pathInventoryDirectory)
      if inputValue.strip():
        correct = True
        var_pathInventoryDirectory = inputValue
        print
        continue
      else:
        print >> sys.stderr, "ERROR: No value"

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(4)


    ###### Path Executables List ######
    var_pathExes = getValueFromFile(configExtra, 'pathExes:', ':')
    if not var_pathExes:
      var_pathExes = "/bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin /opt/csw /boot" 

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Ansible Server gets information from executable files. We can define a list of "
    print "paths to search them"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Directories to search exes (separated by white spaces): ', var_pathExes)
      if inputValue.strip():
	correct = True
        var_pathExes = inputValue.strip()
        print
	continue
      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(5)


    ###### Path No Executables List ######
    var_pathNoExes = getValueFromFile(configExtra, 'pathNoExes:', ':')
    if not var_pathNoExes:
      var_pathNoExes = ""

    print
    print "------------------------------------------------------------"
    print "We can define a list of paths NOT to search executable files"
    print "------------------------------------------------------------"
    print
    inputValue = raw_input_def('Directories not to search exes (separated by white spaces): ', var_pathNoExes)
    var_pathNoExes = inputValue.strip()
    print


    ###### Config Scan Openvas ######
    var_configScanOpenvas = getValueFromFile(configExtra, 'configScanOpenvas:', ':')
    if not var_configScanOpenvas:
      var_configScanOpenvas = "Full and fast"

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Openvas Scan Configuration. Available options: 'Discovery', 'Host Discovery', "
    print "'System Discovery', 'Full and fast', 'Full and fast ultimate', 'Full and very "
    print "deep' and 'Full and very deep ultimate'"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Config Scan Openvas (%s): ' % (configScanOpenvasOptions), var_configScanOpenvas)
      if inputValue.strip():
        if inputValue.strip() in configScanOpenvasOptions:
          correct = True
          var_configScanOpenvas = inputValue.strip()
          print
        else:
          print >> sys.stderr, "ERROR: Incorrect value. Options: %s" % (configScanOpenvasOptions)
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value. Options: %s" % (configScanOpenvasOptions)
        print >> sys.stderr

      if not correct:
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(6)


    ###### Set Openvas Crontab ######
    var_minutesCronOpenvas = getValueFromFile(configExtra, 'minutesCronOpenvas:', ':')
    def_minutesCronOpenvas = var_minutesCronOpenvas
    var_hoursCronOpenvas = getValueFromFile(configExtra, 'hoursCronOpenvas:', ':')
    def_hoursCronOpenvas = var_hoursCronOpenvas
    var_dayCronOpenvas = getValueFromFile(configExtra, 'dayCronOpenvas:', ':')
    def_dayCronOpenvas = var_dayCronOpenvas
    var_weekdayCronOpenvas = getValueFromFile(configExtra, 'weekdayCronOpenvas:', ':')
    def_weekdayCronOpenvas = var_weekdayCronOpenvas

    var_cadCronOpenvas = var_minutesCronOpenvas + " " + var_hoursCronOpenvas + " " + var_dayCronOpenvas + " " + var_weekdayCronOpenvas

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Set crontab: minutes, hours, day and weekday (month is defined in option 1 of "
    print "menu: 'Configure System') for Openvas checking vulnerabilities"
    print "--------------------------------------------------------------------------------"
    print
    print "Month: %s" % (getValueFromFile(productionFile, 'cronOpenvas:', ':'))
    print
    while not correct:
      inputValue = raw_input_def('Openvas Crontab (minute hour day weekday): ', var_cadCronOpenvas)
      if inputValue.strip():
        # Checking cad -> minute hour day weekday
        arr = inputValue.split(' ')
	if len(arr) == 4:
	  # Checking minute
	  if checkCronField(arr[0],"minute"):
	    # Checking hour
     	    if checkCronField(arr[1],"hour"):
	      # Checking day of month
	      if checkCronField(arr[2],"day"): 
		# Checking day of week
		if checkCronField(arr[3],"weekday"):
		  correct = True
		  print

      if correct:
	var_minutesCronOpenvas = arr[0]
	var_hoursCronOpenvas = arr[1]
	var_dayCronOpenvas = arr[2]
	var_weekdayCronOpenvas = arr[3]

	if var_minutesCronOpenvas != def_minutesCronOpenvas or var_hoursCronOpenvas != def_hoursCronOpenvas or var_dayCronOpenvas != def_dayCronOpenvas or var_weekdayCronOpenvas != def_weekdayCronOpenvas:
	  reload = True

      else:
        print >> sys.stderr, "ERROR: Openvas Crontab (minute hour day weekday)"
        print >> sys.stderr, "minute: 0-59  hour: 0-23  day: 1-31  weekday: 0-7"
        print >> sys.stderr
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(7)


    ###### Set Database Update Openvas Crontab ######
    var_minutesUpdateCronOpenvas = getValueFromFile(configExtra, 'minutesUpdateCronOpenvas:', ':')
    def_minutesUpdateCronOpenvas = var_minutesUpdateCronOpenvas
    var_hoursUpdateCronOpenvas = getValueFromFile(configExtra, 'hoursUpdateCronOpenvas:', ':')
    def_hoursUpdateCronOpenvas = var_hoursUpdateCronOpenvas
    var_dayUpdateCronOpenvas = getValueFromFile(configExtra, 'dayUpdateCronOpenvas:', ':')
    def_dayUpdateCronOpenvas = var_dayUpdateCronOpenvas
    var_monthUpdateCronOpenvas = getValueFromFile(configExtra, 'monthUpdateCronOpenvas:', ':')
    def_monthUpdateCronOpenvas = var_monthUpdateCronOpenvas
    var_weekdayUpdateCronOpenvas = getValueFromFile(configExtra, 'weekdayUpdateCronOpenvas:', ':')
    def_weekdayUpdateCronOpenvas = var_weekdayUpdateCronOpenvas

    var_cadUpdateCronOpenvas = var_minutesUpdateCronOpenvas + " " + var_hoursUpdateCronOpenvas + " " + var_dayUpdateCronOpenvas + " "  + var_monthUpdateCronOpenvas + " " + var_weekdayUpdateCronOpenvas

    correct = False
    count = 0
    print
    print "--------------------------------------------------------------------------------"
    print "Openvas synchronizes its database with new NVT (Network Vulnerability Tests)"
    print "Set crontab: minutes, hours, day, month and weekday for Openvas Database update"
    print "--------------------------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Database Update Openvas Crontab (minute hour day month weekday): ', var_cadUpdateCronOpenvas)
      if inputValue.strip():
        # Checking cad -> minute hour day month weekday
        arr = inputValue.split(' ')
        if len(arr) == 5:
          # Checking minute
	  if checkCronField(arr[0],"minute"):
            # Checking hour
	    if checkCronField(arr[1],"hour"):
              # Checking day of month
	      if checkCronField(arr[2],"day"):
                # Checking month
		if checkCronField(arr[3],"month"):
                  # Checking day of week
		  if checkCronField(arr[4],"weekday"):
                    correct = True
                    print

      if correct:
        var_minutesUpdateCronOpenvas = arr[0]
        var_hoursUpdateCronOpenvas = arr[1]
        var_dayUpdateCronOpenvas = arr[2]
        var_monthUpdateCronOpenvas = arr[3]
        var_weekdayUpdateCronOpenvas = arr[4]

        if var_minutesUpdateCronOpenvas != def_minutesUpdateCronOpenvas or var_hoursUpdateCronOpenvas != def_hoursUpdateCronOpenvas or var_dayUpdateCronOpenvas != def_dayUpdateCronOpenvas or var_monthUpdateCronOpenvas != def_monthUpdateCronOpenvas or var_weekdayUpdateCronOpenvas != def_weekdayUpdateCronOpenvas:
          reload = True

      else:
        print >> sys.stderr, "ERROR: Database Update Openvas Crontab (minute hour day month weekday)"
        print >> sys.stderr, "minute: 0-59  hour: 0-23  day: 1-31  month: 1-12  weekday: 0-7"
        print >> sys.stderr
        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(8)


    ###### Exclude Openvas Hosts List ######
    var_excludeServersListOpenvas = getValueFromFile(configExtra, 'excludeServersListOpenvas:', ':')
    def_excludeServersListOpenvas = var_excludeServersListOpenvas
    if not var_excludeServersListOpenvas:
      var_excludeServersListOpenvas = ""

    print
    print "------------------------------------------"
    print "List of hosts NOT to check vulnerabilities"
    print "------------------------------------------"
    print
    inputValue = raw_input_def('Exclude Openvas Hosts List (separated by white spaces): ', var_excludeServersListOpenvas)
    var_excludeServersListOpenvas = inputValue.strip()
    print


    ##### Create Openvas Special Group? #####
    var_specialGroupOpenvas = getValueFromFile(configExtra, 'specialGroupOpenvas:', ':')
    def_specialGroupOpenvas = var_specialGroupOpenvas
    if var_specialGroupOpenvas != "y" and var_specialGroupOpenvas != "n":
      var_specialGroupOpenvas = "n"

    print
    print "--------------------------------------------------------------------------------"
    print "A Openvas Special Group of hosts could be defined to check vulnerabilities with "
    print "a different frequency than the rest"
    print "--------------------------------------------------------------------------------"
    print
    inputValue = question("Do you want to create Openvas Special Group?", var_specialGroupOpenvas, 3) 
    if inputValue:
      var_specialGroupOpenvas = inputValue

      if var_specialGroupOpenvas != def_specialGroupOpenvas:
        reload = True


    ###### Openvas Special Hosts List ######
    var_specialServersListOpenvas = getValueFromFile(configExtra, 'specialServersListOpenvas:', ':')
    def_specialServersListOpenvas = var_specialServersListOpenvas
    if not var_specialServersListOpenvas:
      var_specialServersListOpenvas = ""

    if var_specialGroupOpenvas == "y":
      correct = False
      count = 0
      print
      print "------------------------------------------------"
      print "List of hosts belonging to Openvas Special Group"
      print "------------------------------------------------"
      print
      while not correct:
        inputValue = raw_input_def('Openvas Special Hosts List (separated by white spaces): ', var_specialServersListOpenvas)
        if inputValue.strip():
          correct = True
          var_specialServersListOpenvas = inputValue.strip()
          print

          if var_specialServersListOpenvas != def_specialServersListOpenvas:
            reload = True

          continue
        else:
          print >> sys.stderr, "ERROR: No value"
          print >> sys.stderr

        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(9)


    ###### Set Openvas Special Group Crontab ######
    var_minutesSpecialCronOpenvas = getValueFromFile(configExtra, 'minutesSpecialCronOpenvas:', ':')
    def_minutesSpecialCronOpenvas = var_minutesSpecialCronOpenvas
    var_hoursSpecialCronOpenvas = getValueFromFile(configExtra, 'hoursSpecialCronOpenvas:', ':')
    def_hoursSpecialCronOpenvas = var_hoursSpecialCronOpenvas
    var_daySpecialCronOpenvas = getValueFromFile(configExtra, 'daySpecialCronOpenvas:', ':')
    def_daySpecialCronOpenvas = var_daySpecialCronOpenvas
    var_monthSpecialCronOpenvas = getValueFromFile(configExtra, 'monthSpecialCronOpenvas:', ':')
    def_monthSpecialCronOpenvas = var_monthSpecialCronOpenvas
    var_weekdaySpecialCronOpenvas = getValueFromFile(configExtra, 'weekdaySpecialCronOpenvas:', ':')
    def_weekdaySpecialCronOpenvas = var_weekdaySpecialCronOpenvas

    if var_specialGroupOpenvas == "y":
      var_cadSpecialCronOpenvas = var_minutesSpecialCronOpenvas + " " + var_hoursSpecialCronOpenvas + " " + var_daySpecialCronOpenvas + " "  + var_monthSpecialCronOpenvas + " " + var_weekdaySpecialCronOpenvas

      correct = False
      count = 0
      print
      print "--------------------------------------------------------------------------------"
      print "Set crontab: minutes, hours, day, month and weekday for checking vulnerabilities"
      print " of Openvas Special Group" 
      print "--------------------------------------------------------------------------------"
      print
      while not correct:
        inputValue = raw_input_def('Openvas Special Group Crontab (minute hour day month weekday): ', var_cadSpecialCronOpenvas)
        if inputValue.strip():
          # Checking cad -> minute hour day month weekday
          arr = inputValue.split(' ')
          if len(arr) == 5:
            # Checking minute
            if checkCronField(arr[0],"minute"):
              # Checking hour
              if checkCronField(arr[1],"hour"):
                # Checking day of month
                if checkCronField(arr[2],"day"):
                  # Checking month
                  if checkCronField(arr[3],"month"):
                    # Checking day of week
                    if checkCronField(arr[4],"weekday"):
                      correct = True
                      print

        if correct:
          var_minutesSpecialCronOpenvas = arr[0]
          var_hoursSpecialCronOpenvas = arr[1]
          var_daySpecialCronOpenvas = arr[2]
	  var_monthSpecialCronOpenvas = arr[3]
          var_weekdaySpecialCronOpenvas = arr[4]

          if var_minutesSpecialCronOpenvas != def_minutesSpecialCronOpenvas or var_hoursSpecialCronOpenvas != def_hoursSpecialCronOpenvas or var_daySpecialCronOpenvas != def_daySpecialCronOpenvas or var_monthSpecialCronOpenvas != def_monthSpecialCronOpenvas or var_weekdaySpecialCronOpenvas != def_weekdaySpecialCronOpenvas:
            reload = True

        else:
          print >> sys.stderr, "ERROR: Special Openvas Group Crontab (minute hour day month weekday)"
          print >> sys.stderr, "minute: 0-59  hour: 0-23  day: 1-31  month: 1-12  weekday: 0-7"
          print >> sys.stderr
          count += 1
          if count > maxErrors:
            print >> sys.stderr, "Too many Errors. Exiting..."
            sys.exit(10)


    ###### Set Munin-InfluxDB frequency (minutes) exporting data ######
    var_minutesCronMuninInfluxDB = getValueFromFile(configExtra, 'minutesCronMuninInfluxDB:', ':')
    def_minutesCronMuninInfluxDB = var_minutesCronMuninInfluxDB
    if not var_minutesCronMuninInfluxDB:
      var_minutesCronMuninInfluxDB = "5"

    correct = False
    count = 0
    print
    print "-------------------------------------------------------------"
    print "Set frequency (minutes) exporting data from Munin to InfluxDB"
    print "-------------------------------------------------------------"
    print
    while not correct:
      inputValue = raw_input_def('Frequency to export data from Munin to InfluxDB in minutes (%s minutes): ' % (frequencyRangeMinutes), var_minutesCronMuninInfluxDB)
      if inputValue.strip():
        # Checking frequency 
	if checkFrequency(inputValue.strip(),frequencyRangeMinutes):	
	  correct = True
	  var_minutesCronMuninInfluxDB = inputValue.strip()
	  print
	else:
          print >> sys.stderr, "ERROR: Incorrect value. Range (%s minutes)" % (frequencyRangeMinutes)
          print >> sys.stderr

      else:
        print >> sys.stderr, "ERROR: No value"
        print >> sys.stderr

      count += 1
      if count > maxErrors:
        print >> sys.stderr, "Too many Errors. Exiting..."
        sys.exit(11)



    ###### SUMMARY ######
    print
    print "---------------------------------------"
    print "          Extra Configuration          "
    print "---------------------------------------"
    print "Read Only User: %s" % (var_readUser)
    if var_readUser != "":
      print "Password Read Only User: %s" % (var_passwdReadUser)
      print "Hosts Read Only User: %s" % (var_hostsReadUser if var_hostsReadUser != "" else "ALL")
    print "Path Inventory Directory: %s" % (var_pathInventoryDirectory)
    print "Directories to Search Executables: %s" % (var_pathExes)
    print "Directories not to Search Executables (exclude): %s" % (var_pathNoExes)
    print "Config Scan Openvas: %s" % (var_configScanOpenvas)
    print "Openvas Crontab (minuntes hours day weekday): %s" % (var_cadCronOpenvas)
    print "Database Update Openvas Crontab (minute hour day month weekday): %s" % (var_cadUpdateCronOpenvas)
    print "Exclude Openvas Servers List: %s" % (var_excludeServersListOpenvas)
    print "Create Openvas Special Group? %s" % (var_specialGroupOpenvas)
    if var_specialGroupOpenvas == "y":
      print "Openvas Special Servers List: %s" % (var_specialServersListOpenvas)
      print "Openvas Special Group Crontab: %s" % (var_cadSpecialCronOpenvas)
    print "Frequency exporting data from Munin to InfluxDB: %s" % (var_minutesCronMuninInfluxDB)
    print "---------------------------------------"
    print



    if question("Config and reload?", "y", 3) == "y":
      print "Generating Production File..."
      try:
        f = open(productionFileTmp, 'w')
        mainFile = open(configFile, 'r')

        f.write("### FILE GENERATED BY ANSIBLE. DON'T TOUCH ###\n")
        f.write("\n") 
        for line in mainFile.readlines():
	  if line.startswith("subnets:") or line.startswith("exclude:") or (line.startswith("hostsAdmins:") and not line.startswith("hostsAdmins: ''")):
	    arrLine = line.split(':', 1) 
	    f.write("%s:\n" % (arrLine[0]))
	    arrData = arrLine[1].strip().split(' ')
	    for data in arrData:
	      f.write("- %s\n" % (data))
	  else:
            f.write("%s" % (line))

        mainFile.close()
	f.write("\n")
        f.write("### Extra variables ###\n")
	f.write("\n")
	f.write("# Read Only User\n")
	f.write("readUser: %s\n" % (var_readUser if var_readUser != "" else "''"))
	f.write("\n")
	if var_readUser != "":
          f.write("# Password Read Only User\n")
          f.write("passwdReadUser: %s\n" % (var_passwdReadUser if var_readUser != "" else "''"))
          f.write("\n")
          f.write("# Hosts Read Only User\n")
          if var_hostsReadUser != "":
            f.write("hostsReadUser:\n")
            arr = var_hostsReadUser.split(' ')
            for x in arr:
              f.write("- %s\n" % (x))
          else:
            f.write("hostsReadUser: ''\n")
          f.write("\n")
        f.write("# Path Inventory Directory\n")
        f.write("pathInventoryDirectory: %s\n" % (var_pathInventoryDirectory))
	f.write("\n")
	f.write("# Path Exes List\n")
	f.write("pathExes: %s\n" % (var_pathExes))
	f.write("\n")
	f.write("# Path No Exes List\n")
        f.write("pathNoExes: %s\n" % (var_pathNoExes if var_pathNoExes != "" else "''"))
	f.write("\n")
	f.write("# Config Scan Openvas: 'Discovery', 'Host Discovery', 'System Discovery', 'Full and Fast', 'Full and fast ultimate', 'Full and very deep', 'Full and very deep ultimate'\n")
	f.write("configScanOpenvas: %s\n" % (var_configScanOpenvas))
	f.write("\n")
        f.write("# Cron Openvas (minutes)\n")
        f.write("minutesCronOpenvas: %s\n" % (var_minutesCronOpenvas if '*' not in var_minutesCronOpenvas else "'" + var_minutesCronOpenvas + "'"))
        f.write("\n")
	f.write("# Cron Openvas (hours)\n")
	f.write("hoursCronOpenvas: %s\n" % (var_hoursCronOpenvas if '*' not in var_hoursCronOpenvas else "'" + var_hoursCronOpenvas + "'"))
	f.write("\n")
        f.write("# Cron Openvas (day)\n")
        f.write("dayCronOpenvas: %s\n" % (var_dayCronOpenvas if '*' not in var_dayCronOpenvas else "'" + var_dayCronOpenvas + "'"))
        f.write("\n")
	f.write("# Cron Openvas (weekday)\n")
	f.write("weekdayCronOpenvas: %s\n" % (var_weekdayCronOpenvas if '*' not in var_weekdayCronOpenvas else "'" + var_weekdayCronOpenvas + "'"))
	f.write("\n")
        f.write("# Special Openvas Group (y/n)\n")
        f.write("specialGroupOpenvas: %s\n" % (var_specialGroupOpenvas))
        f.write("\n")
        f.write("# Special Openvas Servers List\n")
        f.write("specialServersListOpenvas: %s\n" % (var_specialServersListOpenvas if var_specialServersListOpenvas != "" else "''"))
        f.write("\n")
        f.write("# Special Cron Openvas (minutes)\n")
        f.write("minutesSpecialCronOpenvas: %s\n" % (var_minutesSpecialCronOpenvas if '*' not in var_minutesSpecialCronOpenvas else "'" + var_minutesSpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (hours)\n")
        f.write("hoursSpecialCronOpenvas: %s\n" % (var_hoursSpecialCronOpenvas if '*' not in var_hoursSpecialCronOpenvas else "'" + var_hoursSpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (day)\n")
        f.write("daySpecialCronOpenvas: %s\n" % (var_daySpecialCronOpenvas if '*' not in var_daySpecialCronOpenvas else "'" + var_daySpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (weekday)\n")
        f.write("weekdaySpecialCronOpenvas: %s\n" % (var_weekdaySpecialCronOpenvas if '*' not in var_weekdaySpecialCronOpenvas else "'" + var_weekdaySpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (month)\n")
        f.write("monthSpecialCronOpenvas: %s\n" % (var_monthSpecialCronOpenvas if '*' not in var_monthSpecialCronOpenvas else "'" + var_monthSpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Exclude Openvas Servers List\n")
        f.write("excludeServersListOpenvas: %s\n" % (var_excludeServersListOpenvas if var_excludeServersListOpenvas != "" else "''"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (minutes)\n")
        f.write("minutesUpdateCronOpenvas: %s\n" % (var_minutesUpdateCronOpenvas if '*' not in var_minutesUpdateCronOpenvas else "'" + var_minutesUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (hours)\n")
        f.write("hoursUpdateCronOpenvas: %s\n" % (var_hoursUpdateCronOpenvas if '*' not in var_hoursUpdateCronOpenvas else "'" + var_hoursUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (day)\n")
        f.write("dayUpdateCronOpenvas: %s\n" % (var_dayUpdateCronOpenvas if '*' not in var_dayUpdateCronOpenvas else "'" + var_dayUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (weekday)\n")
        f.write("weekdayUpdateCronOpenvas: %s\n" % (var_weekdayUpdateCronOpenvas if '*' not in var_weekdayUpdateCronOpenvas else "'" + var_weekdayUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (month)\n")
        f.write("monthUpdateCronOpenvas: %s\n" % (var_monthUpdateCronOpenvas if '*' not in var_monthUpdateCronOpenvas else "'" + var_monthUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Frequency MuninInfluxDB (minutes)\n")
        f.write("minutesCronMuninInfluxDB: %s\n" % (var_minutesCronMuninInfluxDB))
        f.write("\n")

	f.close()
        print "Generated."
        print

      except:
        print >> sys.stderr, "Error opening file: %s" % (productionFileTmp)
        sys.exit(12)

      print "Updating Production File..."
      try:
        # Backup Production file
        print "Backup of Production file as '.back'" 
        shutil.copy(productionFile, "%s.back" % (productionFile))
	os.chmod("%s.back" % (productionFile), 0600)
        # Move Temp file to Production file
        print "Moving from Temp to Production..."
        shutil.move(productionFileTmp, productionFile)
	os.chmod(productionFile, 0600)
        print "Done."
        print
      except:
        print >> sys.stderr, "Error updating Production file."
        sys.exit(13)      
  
      print "Updating Extra file..."
      try:

        # Backup Config Extra 
        shutil.copy(configExtra, "%s.back" % (configExtra))
        print "Saved Old Config Extra as '.back'"
        os.chmod("%s.back" % (configExtra), 0600)
        os.chmod(configExtra, 0600)

        f = open(configExtra, 'w')

        f.write("### Extra variables ###\n")
        f.write("\n")
        f.write("# Read Only User\n")
        f.write("readUser: %s\n" % (var_readUser if var_readUser != "" else "''"))
        f.write("\n")
	if var_readUser != "":
          f.write("# Password Read Only User\n")
          f.write("passwdReadUser: %s\n" % (var_passwdReadUser if var_readUser != "" else "''"))
          f.write("\n")
          f.write("# Hosts Read Only User\n")
          f.write("hostsReadUser: %s\n" % (var_hostsReadUser if var_hostsReadUser != "" else "''"))
          f.write("\n")
        f.write("# Path Inventory Directory\n")
        f.write("pathInventoryDirectory: %s\n" % (var_pathInventoryDirectory))
        f.write("\n")
        f.write("# Path Exes List\n")
        f.write("pathExes: %s\n" % (var_pathExes))
        f.write("\n")
        f.write("# Path No Exes List\n")
        f.write("pathNoExes: %s\n" % (var_pathNoExes if var_pathNoExes != "" else "''"))
	f.write("\n")
        f.write("# Config Scan Openvas: 'Discovery', 'Host Discovery', 'System Discovery', 'Full and Fast', 'Full and fast ultimate', 'Full and very deep', 'Full and very deep ultimate'\n")
        f.write("configScanOpenvas: %s\n" % (var_configScanOpenvas))
        f.write("\n")
        f.write("# Cron Openvas (minutes)\n")
        f.write("minutesCronOpenvas: %s\n" % (var_minutesCronOpenvas if '*' not in var_minutesCronOpenvas else "'" + var_minutesCronOpenvas + "'"))
        f.write("\n")
        f.write("# Cron Openvas (hours)\n")
        f.write("hoursCronOpenvas: %s\n" % (var_hoursCronOpenvas if '*' not in var_hoursCronOpenvas else "'" + var_hoursCronOpenvas + "'"))
        f.write("\n")
        f.write("# Cron Openvas (day)\n")
        f.write("dayCronOpenvas: %s\n" % (var_dayCronOpenvas if '*' not in var_dayCronOpenvas else "'" + var_dayCronOpenvas + "'"))
        f.write("\n")
        f.write("# Cron Openvas (weekday)\n")
        f.write("weekdayCronOpenvas: %s\n" % (var_weekdayCronOpenvas if '*' not in var_weekdayCronOpenvas else "'" + var_weekdayCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Openvas Group (y/n)\n")
        f.write("specialGroupOpenvas: %s\n" % (var_specialGroupOpenvas))
        f.write("\n")
        f.write("# Special Openvas Servers List\n")
        f.write("specialServersListOpenvas: %s\n" % (var_specialServersListOpenvas if var_specialServersListOpenvas != "" else "''"))
        f.write("\n")
        f.write("# Special Cron Openvas (minutes)\n")
        f.write("minutesSpecialCronOpenvas: %s\n" % (var_minutesSpecialCronOpenvas if '*' not in var_minutesSpecialCronOpenvas else "'" + var_minutesSpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (hours)\n")
        f.write("hoursSpecialCronOpenvas: %s\n" % (var_hoursSpecialCronOpenvas if '*' not in var_hoursSpecialCronOpenvas else "'" + var_hoursSpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (day)\n")
        f.write("daySpecialCronOpenvas: %s\n" % (var_daySpecialCronOpenvas if '*' not in var_daySpecialCronOpenvas else "'" + var_daySpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (weekday)\n")
        f.write("weekdaySpecialCronOpenvas: %s\n" % (var_weekdaySpecialCronOpenvas if '*' not in var_weekdaySpecialCronOpenvas else "'" + var_weekdaySpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Special Cron Openvas (month)\n")
        f.write("monthSpecialCronOpenvas: %s\n" % (var_monthSpecialCronOpenvas if '*' not in var_monthSpecialCronOpenvas else "'" + var_monthSpecialCronOpenvas + "'"))
        f.write("\n")
        f.write("# Exclude Openvas Servers List\n")
        f.write("excludeServersListOpenvas: %s\n" % (var_excludeServersListOpenvas if var_excludeServersListOpenvas != "" else "''"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (minutes)\n")
        f.write("minutesUpdateCronOpenvas: %s\n" % (var_minutesUpdateCronOpenvas if '*' not in var_minutesUpdateCronOpenvas else "'" + var_minutesUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (hours)\n")
        f.write("hoursUpdateCronOpenvas: %s\n" % (var_hoursUpdateCronOpenvas if '*' not in var_hoursUpdateCronOpenvas else "'" + var_hoursUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (day)\n")
        f.write("dayUpdateCronOpenvas: %s\n" % (var_dayUpdateCronOpenvas if '*' not in var_dayUpdateCronOpenvas else "'" + var_dayUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (weekday)\n")
        f.write("weekdayUpdateCronOpenvas: %s\n" % (var_weekdayUpdateCronOpenvas if '*' not in var_weekdayUpdateCronOpenvas else "'" + var_weekdayUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Database Update Cron Openvas (month)\n")
        f.write("monthUpdateCronOpenvas: %s\n" % (var_monthUpdateCronOpenvas if '*' not in var_monthUpdateCronOpenvas else "'" + var_monthUpdateCronOpenvas + "'"))
        f.write("\n")
        f.write("# Frequency MuninInfluxDB (minutes)\n")
        f.write("minutesCronMuninInfluxDB: %s\n" % (var_minutesCronMuninInfluxDB))
        f.write("\n")

        f.close()
        print "Done."
        print

      except:
        print >> sys.stderr, "Error updating Extra file."
        print >> sys.stderr


      if reload:
        # Deleting Ansible crontab entries 
        print "Reloading (Deleting and Creating Ansible crontab entries)..."
        print 
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); (ansible-playbook %s/ansible.yml -t cronStop -u %s -s; ansible-playbook %s/ansible.yml -t cronStart -u %s -s) 2>&1|tee /var/log/ansible/.configExtra-cronRestart.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS System Restart (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-cronRestart.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-cronRestart.$timestamp.log.tmp; echo \"### System Restart (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,var_sshUserNodes,pathAnsible,var_sshUserNodes), shell=True)
        print 
        print "Done."
        print 

      if var_minutesCronMuninInfluxDB != def_minutesCronMuninInfluxDB:
	print "Reconfiguring MuninInfluxDB to modify exporting frequency..."
	print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/grafana.yml -t munininfluxdb -u %s -s 2>&1|tee /var/log/ansible/.configExtra-munininfluxdb.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS MuninInfluxDB (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-munininfluxdb.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-munininfluxdb.$timestamp.log.tmp; echo \"### MuninInfluxDB (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,var_sshUserNodes), shell=True)
        print
        print "Done."
        print
      
      if var_readUser != def_readUser or (var_readUser != "" and (var_passwdReadUser != def_passwdReadUser or var_hostsReadUser != def_hostsReadUser)):
	if var_readUser != "":
          print "Reconfiguring system to allow read access to user '%s'..." % (var_readUser)
	if def_readUser != "" and var_readUser != def_readUser:
	  print "Reconfiguring system to deny read access to user '%s'..." % (def_readUser)
        print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/mysql.yml -t config,createDB,firewall --extra-vars \"readUserOld=%s\" -u %s -s 2>&1|tee /var/log/ansible/.configExtra-mysql.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS Mysql Firewall (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-mysql.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-mysql.$timestamp.log.tmp; echo \"### Mysql Firewall (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,def_readUser if def_readUser != "" else "''",var_sshUserNodes), shell=True)
        print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/web.yml -t config,phpMyAdmin,firewall --extra-vars \"readUserOld=%s\" -u %s -s 2>&1|tee /var/log/ansible/.configExtra-web.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS Web Firewall (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-web.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-web.$timestamp.log.tmp; echo \"### Web Firewall (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,def_readUser if def_readUser != ""  else "''",var_sshUserNodes), shell=True)
        print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/nagios.yml -t config,firewall --extra-vars \"readUserOld=%s\" -u %s -s 2>&1|tee /var/log/ansible/.configExtra-nagios.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS Nagios Firewall (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-nagios.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-nagios.$timestamp.log.tmp; echo \"### Nagios Firewall (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,def_readUser if def_readUser != ""  else "''",var_sshUserNodes), shell=True)
        print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/munin.yml -t config,firewall --extra-vars \"readUserOld=%s\" -u %s -s 2>&1|tee /var/log/ansible/.configExtra-munin.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS Munin Firewall (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-munin.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-munin.$timestamp.log.tmp; echo \"### Munin Firewall (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,def_readUser if def_readUser != ""  else "''",var_sshUserNodes), shell=True)
	print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/grafana.yml -t config,influxdb,firewall --extra-vars \"readUserOld=%s\" -u %s -s 2>&1|tee /var/log/ansible/.configExtra-grafana.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS Grafana Firewall (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-grafana.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-grafana.$timestamp.log.tmp; echo \"### Grafana Firewall (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,def_readUser if def_readUser != ""  else "''",var_sshUserNodes), shell=True)
	print
	subprocess.call("ini=$(date); timestamp=$(date +\"%%y%%m%%d-%%H%%M\"); ansible-playbook %s/openvas.yml -t config,readUser,firewall --skip-tags dataDB --extra-vars \"readUserOld=%s\" -u %s -s 2>&1|tee /var/log/ansible/.configExtra-openvas.$timestamp.log.tmp; [ $? -gt 0 ] && ((echo; echo \"### ERRORS Openvas Firewall (extra configuration) - $ini TO $(date) ###\"; echo; cat /var/log/ansible/.configExtra-openvas.$timestamp.log.tmp) >> /var/log/ansible/errors.log); rm -f /var/log/ansible/.configExtra-openvas.$timestamp.log.tmp; echo \"### Openvas Firewall (extra configuration) - $ini TO $(date) ###\" >> /var/log/ansible/summary.log;" % (pathAnsible,def_readUser if def_readUser != ""  else "''",var_sshUserNodes), shell=True)
        print
        print "Done."
        print

    else:
      print "Cancelled."
      print

  except KeyboardInterrupt:
    print
    print "Extra Configuration interrumped"
    print


if __name__ == '__main__':
	    main()

