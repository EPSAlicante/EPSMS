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

# Config Scan Openvas
configScanOpenvasOptions = [ "Discovery", "Host Discovery", "System Discovery", "Full and fast", "Full and fast ultimate", "Full and very deep", "Full and very deep ultimate" ]

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
    print "###############################"
    print " Extra variables Configuration "
    print "###############################"
    print

    ###### Path Inventory Directory ######
    var_pathInventoryDirectory = getValueFromFile(configExtra, 'pathInventoryDirectory:', ':')
    if not var_pathInventoryDirectory:
      var_pathInventoryDirectory = "/root/inventory"

    correct = False
    count = 0
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
        sys.exit(2)


    ###### Path Executables List ######
    var_pathExes = getValueFromFile(configExtra, 'pathExes:', ':')
    if not var_pathExes:
      var_pathExes = "/bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin /opt/csw /boot" 

    correct = False
    count = 0
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
        sys.exit(3)


    ###### Path No Executables List ######
    var_pathNoExes = getValueFromFile(configExtra, 'pathNoExes:', ':')
    if not var_pathNoExes:
      var_pathNoExes = ""

    inputValue = raw_input_def('Directories not to search exes (separated by white spaces): ', var_pathNoExes)
    var_pathNoExes = inputValue.strip()
    print


    ###### Config Scan Openvas ######
    var_configScanOpenvas = getValueFromFile(configExtra, 'configScanOpenvas:', ':')
    if not var_configScanOpenvas:
      var_configScanOpenvas = "Full and fast"

    correct = False
    count = 0
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
          sys.exit(4)


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
    while not correct:
      inputValue = raw_input_def('Openvas Crontab (minute hour day weekday): ', var_cadCronOpenvas)
      if inputValue.strip():
        # Checking cad -> minute hour day weekday
        arr = inputValue.split(' ')
	if len(arr) == 4:
	  # Checking minute
	  if arr[0] == "*" or (isInt(arr[0]) and (0 <= int(arr[0]) <= 59)):
	    # Checking hour
     	    if arr[1] == "*" or (isInt(arr[1]) and (0 <= int(arr[1]) <= 23)):
	      # Checking day of month
	      if arr[2] == "*" or (isInt(arr[2]) and (1 <= int(arr[2]) <= 31)): 
		# Checking day of week
		if arr[3] == "*" or (isInt(arr[3]) and (0 <= int(arr[3]) <= 7)):
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
          sys.exit(5)


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
    while not correct:
      inputValue = raw_input_def('Database Update Openvas Crontab (minute hour day month weekday): ', var_cadUpdateCronOpenvas)
      if inputValue.strip():
        # Checking cad -> minute hour day month weekday
        arr = inputValue.split(' ')
        if len(arr) == 5:
          # Checking minute
          if arr[0] == "*" or (isInt(arr[0]) and (0 <= int(arr[0]) <= 59)):
            # Checking hour
            if arr[1] == "*" or (isInt(arr[1]) and (0 <= int(arr[1]) <= 23)):
              # Checking day of month
              if arr[2] == "*" or (isInt(arr[2]) and (1 <= int(arr[2]) <= 31)):
                # Checking month
                if arr[3] == "*" or (isInt(arr[3]) and (1 <= int(arr[3]) <= 12)):
                  # Checking day of week
                  if arr[4] == "*" or (isInt(arr[4]) and (0 <= int(arr[4]) <= 7)):
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
          sys.exit(6)


    ###### Exclude Openvas Servers List ######
    var_excludeServersListOpenvas = getValueFromFile(configExtra, 'excludeServersListOpenvas:', ':')
    def_excludeServersListOpenvas = var_excludeServersListOpenvas
    if not var_excludeServersListOpenvas:
      var_excludeServersListOpenvas = ""

    inputValue = raw_input_def('Exclude Openvas Servers List (separated by white spaces): ', var_excludeServersListOpenvas)
    var_excludeServersListOpenvas = inputValue.strip()
    print


    ##### Create Openvas Special Group? #####
    var_specialGroupOpenvas = getValueFromFile(configExtra, 'specialGroupOpenvas:', ':')
    def_specialGroupOpenvas = var_specialGroupOpenvas
    if var_specialGroupOpenvas != "y" and var_specialGroupOpenvas != "n":
      var_specialGroupOpenvas = "n"

    inputValue = question("Do you want to create Openvas Special Group?", var_specialGroupOpenvas, 3) 
    if inputValue:
      var_specialGroupOpenvas = inputValue


    ###### Openvas Special Servers List ######
    var_specialServersListOpenvas = getValueFromFile(configExtra, 'specialServersListOpenvas:', ':')
    def_specialServersListOpenvas = var_specialServersListOpenvas
    if not var_specialServersListOpenvas:
      var_specialServersListOpenvas = ""

    if var_specialGroupOpenvas == "y":
      correct = False
      count = 0
      while not correct:
        inputValue = raw_input_def('Openvas Special Servers List (separated by white spaces): ', var_specialServersListOpenvas)
        if inputValue.strip():
          correct = True
          var_specialServersListOpenvas = inputValue.strip()
          print
          continue
        else:
          print >> sys.stderr, "ERROR: No value"
          print >> sys.stderr

        count += 1
        if count > maxErrors:
          print >> sys.stderr, "Too many Errors. Exiting..."
          sys.exit(7)


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
      while not correct:
        inputValue = raw_input_def('Openvas Special Group Crontab (minute hour day month weekday): ', var_cadSpecialCronOpenvas)
        if inputValue.strip():
          # Checking cad -> minute hour day month weekday
          arr = inputValue.split(' ')
          if len(arr) == 5:
            # Checking minute
            if arr[0] == "*" or (isInt(arr[0]) and (0 <= int(arr[0]) <= 59)):
              # Checking hour
              if arr[1] == "*" or (isInt(arr[1]) and (0 <= int(arr[1]) <= 23)):
                # Checking day of month
                if arr[2] == "*" or (isInt(arr[2]) and (1 <= int(arr[2]) <= 31)):
		  # Checking month
		  if arr[3] == "*" or (isInt(arr[3]) and (1 <= int(arr[3]) <= 12)):
                    # Checking day of week
                    if arr[4] == "*" or (isInt(arr[4]) and (0 <= int(arr[4]) <= 7)):
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
            sys.exit(8)




    ###### SUMMARY ######
    print
    print "---------------------------------------"
    print "          Extra Configuration          "
    print "---------------------------------------"
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
	  if line.startswith("subnets:") or line.startswith("exclude:") or line.startswith("hostsAdmins:"):
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

	f.close()
        print "Generated."
        print

      except:
        print >> sys.stderr, "Error opening file: %s" % (productionFileTmp)
        sys.exit(9)

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
        sys.exit(10)      
  
      print "Updating Extra file..."
      try:
        f = open(configExtra, 'w')

        f.write("### Extra variables ###\n")
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
        subprocess.call("ansible-playbook %s/ansible.yml -t cronStop -u %s -s; ansible-playbook %s/ansible.yml -t cronStart -u %s -s" % (pathAnsible,var_sshUserNodes,pathAnsible,var_sshUserNodes), shell=True) 
        print 
        print "Done."
        print 


    else:
      print "Cancelled."
      print



if __name__ == '__main__':
	    main()

