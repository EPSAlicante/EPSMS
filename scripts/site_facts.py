#!/usr/bin/python

import subprocess
import socket
import datetime
import codecs
try:
  import json
except ImportError:
  import simplejson as json




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


def typeOS():
    retOS = subprocess.Popen("%s -s 2>%s" % (path('uname'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    return retOS.stdout.read().strip()


def dmidecode_OK():
    retCode = subprocess.call("%s >/dev/null 2>%s" % (path('dmidecode'), errorLog), shell=True, executable='%s' % (bash)) 
    return retCode


def dmidecode_Command(type):
    # Versions of dmidecode bedore 2.7 don't have -t parameter
    retCode = subprocess.call("(%s -t %s) >/dev/null 2>%s" % (path('dmidecode'), type, errorLog), shell=True, executable='%s' % (bash))
    if retCode == 0:
      # dmidecode 2.7+ 
      retCommand = "%s -t %s" % (path('dmidecode'), type)  
    else:
      # dmidecode 2.6-
      retCommand = "%s|%s ':a;N;$!ba;s/\\n/#X#X#X#X#X#/g'|%s 's/#X#X#X#X#X#Handle /\\nHandle /g'|%s -i 'DMI type %s,'|%s 's/#X#X#X#X#X#/\\n/g'" % (path('dmidecode'), type, sed, sed, grep, sed)

    return retCommand
 

def formatCad(cad):
    try:
#      if isinstance(cad,basestring):
#        retCad = cad.replace("\\","\\\\").replace("\"","\\\"").replace("'","\\\"").replace("\(","\\(").replace("\)","\\)").replace("\[","\\[").replace("\]","\\]").replace("\{","\\{").replace("\}","\\}")
#      else:
#        retCad = cad

      retCad = json.dumps(cad.replace("'","\"")).replace("\\u","\\\\u")[1:-1]

      #return retCad.encode('utf-8','replace')
      return retCad

    except:
      return ""


def isHex(cad):
    try:
      int(cad,16)
      return True
    except ValueError:
      return False
 

def show_system():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(1), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE) 
    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0
    
    if totalData > 0:
      print "    \"system\": {"
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(1), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():    
	line = line.strip()
	# Looking for next Handle
        if line.find("Handle") == 0:
	  if countData > 1:
	    break

	  handle = line.split(',')[0].split(' ')[1].strip() 
	  print "        \"Handle\": \"%s\"," % (formatCad(handle))      
	  countData += 1

	else:
	  # Data in label:value format
	  if line.find(":") >= 0: 		
	    label = line.split(':')[0].strip()  
	    value = line.split(':')[1].strip()
	    if label in ['Manufacturer', 'Product Name', 'Version', 'Serial Number', 'UUID', 'Wake-up Type']:
	      # Printing last Data
	      if lastData != "":
		print "%s," % (lastData)

              # Getting Wake-up Type label (label name to Wake-Up Type)
              if label == "Wake-up Type":
                lastData = "        \"Wake-Up Type\": \"%s\"" % (formatCad(value))

              else:
	        # Getting new Data
	        lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))		

      # Printing last Data
      if lastData != "":
	print "%s" % (lastData) 
	
      print "    },"


def show_processor():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(4), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"processor\": ["
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(4), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      modeFlag = 0
      lastFlag = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next handle
        if line.find("Handle") == 0:
	  if countData > 1:
	    # Flag mode? Writing last Flag
	    if modeFlag == 1:
	      print "%s" % (lastFlag)
	      print "        }%s" % ("",",") [ signature == "" or serialNumber == "" ]
	      modeFlag = 0
	      lastFlag = ""	
 
	    # Printing last Data
            if lastData != "":
              print "%s%s" % (lastData, ("",",") [ signature == "" or serialNumber == "" ])
              lastData = ""
	
	    # Signature must be printed 
	    if signature == "":
	      print "        \"Signature\": \"None\"%s" % ("",",") [ serialNumber == "" ] 

            # Serial Number must be printed
            if serialNumber == "":
              print "        \"Serial Number\": \"None\""
	      
	    # Closing previous handle
            print "      },"

          # Opening new handle
          print "      {"
          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1
	  signature = ""
	  serialNumber = ""

        else:
	  # Data in label:value format
          if line.find(":") >= 0:
	    # Getting label and value
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Socket Designation', 'Type', 'Family', 'Manufacturer', 'Signature', 'ID', 'Version', 'Voltage', 'External Clock', 'Max Speed', 'Current Speed', 'Status', 'Upgrade', 'L1 Cache Handle', 'L2 Cache Handle', 'L3 Cache Handle', 'Serial Number']:
              # Flag mode? Writing last Flag
              if modeFlag == 1:
                print "%s" % (lastFlag)
                print "        },"
                modeFlag = 0
                lastFlag = ""

	      # Printing last Data
              elif lastData != "":
                print "%s," % (lastData)

              # Signature printed
              if label == "Signature":
                signature = "OK"

              # Serial Number printed
              if label == "Serial Number":
                serialNumber = "OK"

              # Getting Manufacturer label (label name to Vendor)
              if label == "Manufacturer":
                lastData = "        \"Vendor\": \"%s\"" % (formatCad(value))

	      else:
	        # Getting new Data
                lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

	    elif label == "Flags":
	      # Printing last Data
              if lastData != "":
                print "%s," % (lastData)
		lastData = ""

	      # Putting Flag mode
	      modeFlag = 1
	      lastFlag = ""
	      print "        \"%s\": { " % (formatCad(label))	

	  else:
	    if modeFlag == 1:
	      # Printing last Flag 
	      if lastFlag != "":
		print "%s," % (lastFlag)

	      # Getting new Flag 
	      if line.strip() != "":
	        lastFlag = "          \"%s\": \"True\"" % (formatCad(line.strip()))
	       
      # Printing last Data
      if lastData != "":
        print "%s%s" % (lastData, ("",",") [ signature == "" or serialNumber == "" ])

      # Printing last Flag
      elif modeFlag == 1:
        print "%s" % (lastFlag)
        print "        }%s" % ("",",") [ signature == "" or serialNumber == "" ] 

      # Signature must be printed  
      if signature == "":
        print "        \"Signature\": \"None\"%s" % ("",",") [ serialNumber == "" ] 

      # Serial Number must be printed
      if serialNumber == "":
        print "        \"Serial Number\": \"None\""

      # Closing last handle
      print "      }"

      print "    ],"


def show_memory():
    # Getting Total Memory Handles
    numData5 = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(5), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    numData16 = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(16), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    numData17 = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(17), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData5.stdout.read()) + int(numData16.stdout.read()) + int(numData17.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"memory\": {"

      # Getting Total Array Handles
      numArrayData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(16), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      totalArrayData = int(numArrayData.stdout.read())

      print "      \"arrays\": ["
      # Executing dmidecode to get Data
      arrayData = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(16), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countArrayData = 1
      lastArrayData = ""
      for arrayLine in arrayData.stdout.readlines():
	arrayLine = arrayLine.strip()
        # Looking for next Handle
        if arrayLine.find("Handle") == 0:
          if countArrayData > 1:
            # Printing last Data
            if lastArrayData != "":
              print "%s" % (lastArrayData)
              lastArrayData = ""

            # Closing previous handle
            print "        },"

          # Opening new Handle
          print "        {"
          handle = arrayLine.split(',')[0].split(' ')[1].strip()
          print "          \"Handle\": \"%s\"," % (formatCad(handle))
          countArrayData += 1

        else:
          # Data in label:value format
          if arrayLine.find(":") >= 0:
            label = arrayLine.split(':')[0].strip()
            value = arrayLine.split(':')[1].strip()
            if label in ['Location', 'Use', 'Error Correction Type', 'Maximum Capacity', 'Number Of Devices']:
              # Printing last Data
              if lastArrayData != "":
                print "%s," % (lastArrayData)

              # Getting new Data
              lastArrayData = "          \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastArrayData != "":
        print "%s" % (lastArrayData)

      # Closing last Handle
      print "        }"

      print "      ],"


      # Getting Total Controller Handles
      numControllerData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(5), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      totalControllerData = int(numControllerData.stdout.read())

      # Executing dmidecode to get Data
      controllerData = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(5), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countControllerData = 1
      lastControllerData = ""
      for controllerLine in controllerData.stdout.readlines():
	controllerLine = controllerLine.strip()
        # Looking Handle
        if controllerLine.find("Handle") == 0:
	  countControllerData += 1
	  if countControllerData > 1:
	    break

	else:
          # Data in label:value format
          if controllerLine.find(":") >= 0:
            label = controllerLine.split(':')[0].strip()
            value = controllerLine.split(':')[1].strip()
            if label in ['Maximum Memory Module Size', 'Maximum Total Memory Size']:
              # Printing Data
              print "          \"%s\": \"%s\"," % (formatCad(label),formatCad(value))


      # Getting Total Slot Handles
      numSlotData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(17), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      totalSlotData = int(numSlotData.stdout.read())

      print "      \"slots\": ["
      # Executing dmidecode to get Data
      slotData = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(17), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countSlotData = 1
      lastSlotData = ""
      for slotLine in slotData.stdout.readlines():
	slotLine = slotLine.strip()
        # Looking for next Handle
        if slotLine.find("Handle") == 0:
          if countSlotData > 1:
            # Printing last Data
            if lastSlotData != "":
              print "%s%s" % (lastSlotData, ("",",") [ speed == "" ]) 
              lastSlotData = ""

            # Speed must be printed
            if speed == "":
              print "          \"Speed\": \"None\""

            # Closing previous handle
            print "        },"

          # Opening new Handle
          print "        {"
          handle = slotLine.split(',')[0].split(' ')[1].strip()
          print "          \"Handle\": \"%s\"," % (formatCad(handle))
          countSlotData += 1
	  speed = ""

        else:
          # Data in label:value format
          if slotLine.find(":") >= 0:
            label = slotLine.split(':')[0].strip()
            value = slotLine.split(':')[1].strip()
            if label in ['Locator', 'Bank Locator', 'Size', 'Speed', 'Type']:
              # Printing last Data
              if lastSlotData != "":
                print "%s," % (lastSlotData)

              # Speed printed
              if label == "Speed":
                speed = "OK"

              # Getting new Data
              lastSlotData = "          \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

              # Getting Length label (label name to SlotLength)
            elif label == "Array Handle":
                lastSlotData = "          \"Array\": \"%s\"" % (formatCad(value))

      # Printing last Data
      if lastSlotData != "":
        print "%s%s" % (lastSlotData, ("",",") [ speed == "" ])

      # Speed must be printed
      if speed == "":
        print "          \"Speed\": \"None\""

      # Closing last Handle
      print "        }"

      print "      ]"

      print "    },"


def show_bios():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(0), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"bios\": {"
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(0), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      modeChar = 0
      lastChar = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next handle
        if line.find("Handle") == 0:
	  if countData > 1:
	    break

          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            # Getting label and value
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Vendor', 'Release Date', 'Version', 'ROM Size', 'Runtime Size']:
              # Char mode? Writing last Char
              if modeChar == 1:
                print "%s" % (lastChar)
                print "        },"
                modeChar = 0
                lastChar = ""

              # Printing last Data
              elif lastData != "":
                print "%s," % (lastData)

              # Getting new Data
              lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

            elif label == "Characteristics":
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)
                lastData = ""

              # Putting Char mode
              modeChar = 1
              lastChar = ""
              print "        \"%s\": { " % (formatCad(label))

          else:
            if modeChar == 1:
              # Printing last Char 
              if lastChar != "":
                print "%s," % (lastChar)

              # Getting new Char 
	      if line.strip() != "": 
	        lastChar = "          \"%s\": \"True\"" % (formatCad(line.strip()))

      # Printing last Data
      if lastData != "":
        print "%s" % (lastData)

      # Printing last Char 
      elif modeChar == 1:
        print "%s" % (lastChar)
        print "        }"

      print "    },"


def show_baseboard():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(2), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"baseboard\": ["
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(2), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next Handle
        if line.find("Handle") == 0:
          if countData > 1:
            # Printing last Data
            if lastData != "":
              print "%s" % (lastData)
              lastData = ""

            # Closing previous handle
            print "      },"

          # Opening new Handle
          print "      {"
          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Manufacturer', 'Product Name', 'Version', 'Serial Number']:
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)

              # Getting new Data
              lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastData != "":
        print "%s" % (lastData)

      # Closing last Handle
      print "      }"

      print "    ],"


def show_baseboard_device():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(10), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"baseboarddevice\": ["
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(10), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():
	line = line.strip()
	# Getting handle info
	if line.find("Handle") == 0:
	  handle = line.split(',')[0].split(' ')[1].strip() 

        # Looking for next Device 
        elif line.find("On Board Device") == 0:
          if countData > 1:
            # Printing last Data
            if lastData != "":
              print "%s" % (lastData)
              lastData = ""

            # Closing previous Device
            print "      },"

          # Opening new Device
          print "      {"
	  # Getting device number
	  if line.split(' ')[3].strip() != "Information":
            handleDevice = handle  + " (" + line.split(' ')[3].strip() + ")"
	  else:
	    handleDevice = handle
          print "        \"Handle\": \"%s\"," % (formatCad(handleDevice))
          countData += 1

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Type', 'Description', 'Status']:
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)

              # If Configuration label, split in enabled and level
              if label == "Status":
                if value == "Enabled":
                  lastData = "        \"Enabled\": \"True\""
                else:
                  lastData = "        \"Enabled\": \"False\""

	      else:
                # Getting new Data
                lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastData != "":
        print "%s" % (lastData)

      # Closing last Device
      print "      }"

      print "    ],"


def show_chassis():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(3), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"chassis\": {"
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(3), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next Handle
        if line.find("Handle") == 0:
          if countData > 1:
	    break

          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Manufacturer', 'Type', 'Version', 'Serial Number']:
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)

              # Getting new Data
              lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastData != "":
        print "%s" % (lastData)

      print "    },"


def show_cache():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(7), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"cache\": ["
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(7), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next Handle
        if line.find("Handle") == 0:
          if countData > 1:
            # Printing last Data
            if lastData != "":
              print "%s" % (lastData)
              lastData = ""

            # Closing previous handle
            print "      },"

          # Opening new Handle
          print "      {"
          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Socket Designation', 'Configuration', 'Operational Mode', 'Location', 'Installed Size', 'Maximum Size']:
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)

	      # If Configuration label, split in enabled and level
	      if label == "Configuration":
		# Getting Enabled field
		valueEnabled = value.split(',')[0].strip()	
		if valueEnabled == "Enabled":
		  print "        \"Enabled\": \"True\","
		else:
		  print "        \"Enabled\": \"False\","
		# Getting Level field 
		valueLevel = value.split(',')[2].strip().split(' ')[1]
		lastData = "        \"Level\": \"%s\"" % (formatCad(valueLevel))
		
	      else:
                # Getting new Data
                lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastData != "":
        print "%s" % (lastData)

      # Closing last Handle
      print "      }"

      print "    ],"


def show_connector():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(8), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"connector\": ["
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(8), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next Handle
        if line.find("Handle") == 0:
          if countData > 1:
            # Printing last Data
            if lastData != "":
              print "%s" % (lastData)
              lastData = ""

            # Closing previous handle
            print "      },"

          # Opening new Handle
          print "      {"
          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Internal Reference Designator', 'Internal Connector Type', 'External Reference Designator', 'External Connector Type', 'Port Type']:
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)

              # Getting new Data
              lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastData != "":
        print "%s" % (lastData)

      # Closing last Handle
      print "      }"

      print "    ],"


def show_slot():
    # Getting Total Handles
    numData = subprocess.Popen("(%s|%s '^Handle'|wc -l) 2>%s" % (dmidecode_Command(9), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    try:
      totalData = int(numData.stdout.read())
    except:
      totalData = 0

    if totalData > 0:
      print "    \"slot\": ["
      # Executing dmidecode to get Data
      data = subprocess.Popen("(%s) 2>%s" % (dmidecode_Command(9), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      lastData = ""
      for line in data.stdout.readlines():
	line = line.strip()
        # Looking for next Handle
        if line.find("Handle") == 0:
          if countData > 1:
            # Printing last Data
            if lastData != "":
              print "%s%s" % (lastData, ("",",") [ id == "" ]) 
              lastData = ""

            # ID must be printed
            if id == "":
              print "        \"SlotId\": \"None\""

            # Closing previous handle
            print "      },"

          # Opening new Handle
          print "      {"
          handle = line.split(',')[0].split(' ')[1].strip()
          print "        \"Handle\": \"%s\"," % (formatCad(handle))
          countData += 1
	  id = ""

        else:
          # Data in label:value format
          if line.find(":") >= 0:
            label = line.split(':')[0].strip()
            value = line.split(':')[1].strip()
            if label in ['Designation', 'Type', 'Current Usage', 'Length', 'ID']: 
              # Printing last Data
              if lastData != "":
                print "%s," % (lastData)

              # If Type label, split in Type SlotBusWidth and Type SlotType 
              if label == "Type":
                # Getting SlotBusWidth field
                valueSlotBusWidth = value.split(' ')[0].strip()
		print "        \"Type SlotBusWidth\": \"%s\"," % (formatCad(valueSlotBusWidth))
                # Getting SlotType field
                valueSlotType = value.split(' ', 1)[1].strip()
                lastData = "        \"Type SlotType\": \"%s\"" % (formatCad(valueSlotType))

              # Getting Length label (label name to SlotLength)
              elif label == "Length":
                lastData = "        \"SlotLength\": \"%s\"" % (formatCad(value))

	      # Getting ID label (label name to SlotId)
	      elif label == "ID":
		id = "OK"
		lastData = "        \"SlotId\": \"%s\"" % (formatCad(value))
 
	      else:
                # Getting new Data
                lastData = "        \"%s\": \"%s\"" % (formatCad(label),formatCad(value))

      # Printing last Data
      if lastData != "":
        print "%s%s" % (lastData, ("",",") [ id == "" ])

      # ID must be printed
      if id == "":
        print "        \"SlotId\": \"None\""

      # Closing last Handle
      print "      }"

      print "    ],"


def show_modules():
    # Getting Modules
    if typeOS() == "SunOS": 
      totalModules = int(subprocess.Popen("(%s|tr -s ' '|%s 's/^ *//'|%s -v '^Id'|%s '{ print $6 \" \" $1 \" \" $5 \" \" }'|sort|uniq|wc -l) 2>%s" % (path('modinfo'), sed, grep, awk, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    else:
      totalModules = int(subprocess.Popen("(cat /proc/modules|wc -l) 2>%s" % (errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    if totalModules > 0:
      print "    \"module\": ["  
      # Reading modules to get Data
      if typeOS() == "SunOS":
	data = subprocess.Popen("(%s|tr -s ' '|%s 's/^ *//'|%s -v '^Id'|%s '{ print $6 \" \" $1 \" \" $5 \" \" }'|sort|uniq) 2>%s" % (path('modinfo'), sed, grep, awk, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      else:
        data = subprocess.Popen("(cat /proc/modules| cut -d' ' -f1|sort) 2>%s" % (errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      countData = 1
      for line in data.stdout.readlines():
	if typeOS() == "SunOS":
	  module = line.strip().split(' ')[0]
	  moduleId = line.strip().split(' ')[1]
	  version = line.strip().split(' ')[2]
	  srcversion = line.strip().split(' ')[2]
	  description = subprocess.Popen("(%s -i %s|%s %s|tr -s ' '|%s 's/^ *//'|head -1|cut -d' ' -f7-) 2>%s" % (path('modinfo'), moduleId, grep, moduleId, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip() 
	  filename = author = license = vermagic = depends = "" 
	else:
          module = line.strip()
	  filename = subprocess.Popen("(%s %s|%s '^filename:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  author = subprocess.Popen("(%s %s|%s '^author:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  description = subprocess.Popen("(%s %s|%s '^description:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  license = subprocess.Popen("(%s %s|%s '^license:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  version = subprocess.Popen("(%s %s|%s '^version:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  srcversion = subprocess.Popen("(%s %s|%s '^srcversion:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  vermagic = subprocess.Popen("(%s %s|%s '^vermagic:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  depends = subprocess.Popen("(%s %s|%s '^depends:'|head -1|cut -d':' -f2) 2>%s" % (path('modinfo'), module, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "     {"
        print "       \"name\": \"%s\"," % (formatCad(module))
        print "       \"filename\": \"%s\"," % (formatCad(filename))
        print "       \"author\": \"%s\"," % (formatCad(author))
        print "       \"description\": \"%s\"," % (formatCad(description))
        print "       \"license\": \"%s\"," % (formatCad(license))
        print "       \"version\": \"%s\"," % (formatCad(version))
        print "       \"srcversion\": \"%s\"," % (formatCad(srcversion))
        print "       \"vermagic\": \"%s\"," % (formatCad(vermagic))
        print "       \"depends\": \"%s\"" % (formatCad(depends))
        print "     }%s" % (("",",") [ countData < totalModules ])
        countData += 1

      print "    ],"


def show_interfaces():
    # Getting Total Interfaces
    if typeOS() == "SunOS" or typeOS().endswith("BSD"): 
      totalInterfaces = int(subprocess.Popen("(%s -a inet|%s ': '|%s 'flags'|cut -d':' -f1|wc -l) 2>%s" % (path('ifconfig'), grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    else:
      totalInterfaces = int(subprocess.Popen("(%s -a|%s -v '^\t'|%s -v '^ '|%s -v '^$'|cut -d' ' -f1|%s 's/:$//g'|wc -l) 2>%s" % (path('ifconfig'), grep, grep, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    if totalInterfaces > 0:
      print "    \"interfaces\": ["
      # Executing ifconfig to get Data
      if typeOS() == "SunOS" or typeOS().endswith("BSD"):
        data = subprocess.Popen("(%s -a inet|%s ': '|%s 'flags'|cut -d':' -f1) 2>%s" % (path('ifconfig'), grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      else:
	data = subprocess.Popen("(%s -a|%s -v '^\t'|%s -v '^ '|%s -v '^$'|cut -d' ' -f1|%s 's/:$//g') 2>%s" % (path('ifconfig'), grep, grep, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      for line in data.stdout.readlines():
	device = line.strip()
	print "      {"
	print "        \"device\": \"%s\"," % (device)
	if typeOS() == "SunOS" or typeOS().endswith("BSD"):
	  address = subprocess.Popen("(%s %s|%s 'inet '|%s 's/^.*inet //'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	else:
	  address = subprocess.Popen("(%s %s|%s 'inet addr:'|%s 's/^.*inet addr://'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	  if address == "":
	    # Another version of ifconfig
	    address = subprocess.Popen("(%s %s|%s 'inet '|%s 's/^.*inet //'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	print "        \"address\": \"%s\"," % (address)
	print "        \"namedns\": \"%s\"," % (("",socket.getfqdn(address).lower()) [ address != "" ])

	if typeOS() == "SunOS" or typeOS().endswith("BSD"):
	  netmask = subprocess.Popen("(%s %s|%s 'inet '|%s 's/^.*netmask //'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	else:
          netmask = subprocess.Popen("(%s %s|%s 'Mask:'|%s 's/^.*Mask://'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	  if netmask =="":
	    # Another version of ifconfig
	    netmask = subprocess.Popen("(%s %s|%s 'netmask '|%s 's/^.*netmask //'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	# If netmask in Hex, convert to decimal	
	if isHex(netmask):
          if netmask.startswith('0x'):
            netmaskHex = netmask.replace('0x','')
	  else:
  	    netmaskHex = netmask

          netmaskBytes = ["".join(x) for x in zip(*[iter(netmaskHex)]*2)]
          netmaskBytes = [int(x, 16) for x in netmaskBytes]
          netmask = ".".join(str(x) for x in netmaskBytes)

	if address != "" and netmask != "":
	  addressArray = address.split('.')
	  netmaskArray = netmask.split('.')
	  networkArray = [str(int(addressArray[x]) & int(netmaskArray[x])) for x in range(0,4)]
	  network = '.'.join(networkArray)

	else:
	  network = ""

	print "        \"netmask\": \"%s\"," % (netmask)
	print "        \"network\": \"%s\"," % (network)

        macaddress = subprocess.Popen("(%s %s|%s -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}') 2>%s" % (path('ifconfig'), device, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	if macaddress == "":
          macaddress = subprocess.Popen("(%s %s|%s 'ether '|tr '\t' ' '|%s 's/[[:space:]]* / /g'|cut -d' ' -f3) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "        \"macaddress\": \"%s\"," % (macaddress)

        if typeOS().endswith("BSD"):
          mtu = subprocess.Popen("(%s %s|%s -i ' mtu '|%s 's/^.*mtu //I') 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	elif typeOS() == "SunOS":
	  mtu = subprocess.Popen("(%s %s|%s -i ' mtu '|cut -d':' -f2|tr '\t' ' '|%s 's/[[:space:]]* / /g'|cut -d' ' -f4) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
 	else:	
          mtu = subprocess.Popen("(%s %s|%s -i 'MTU:'|cut -d':' -f2|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  if mtu == "":
            mtu = subprocess.Popen("(%s %s|%s -i ' mtu '|cut -d':' -f2|tr '\t' ' '|%s 's/[[:space:]]* / /g'|cut -d' ' -f4) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "        \"mtu\": %s," % (("0",mtu) [ mtu != "" ])

	if typeOS().endswith("BSD"):
          type = subprocess.Popen("(%s %s|%s 'media: '|cut -d':' -f2|%s 's/^. *//g'|cut -d' ' -f1) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	elif typeOS() == "SunOS":
	  type = subprocess.Popen("(%s %s|%s -o -i -e 'LOOPBACK' -e 'ETHER') 2>%s" % (path('ifconfig'), device, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	else:
          type = subprocess.Popen("(%s %s|%s 'Link encap:'|%s 's/HWaddr/:/'|cut -d':' -f2) 2>%s" % (path('ifconfig'), device, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  if type == "":
            type = subprocess.Popen("(%s %s|%s ' txqueuelen '|cut -d'(' -f2|cut -d')' -f1) 2>%s" % (path('ifconfig'), device, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	if type == "Ethernet":
	  type = "ether"
	elif type == "Local Loopback":
	  type = "loopback"
	else:
	  type = type.lower()
	  
        print "        \"type\": \"%s\"," % (type)

	active = subprocess.Popen("(%s %s|%s -o 'RUNNING') 2>%s" % (path('ifconfig'), device, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "        \"active\": %s" % (("false","true") [ active == "RUNNING" ])

	print "      }%s" % (("",",") [ countData < totalInterfaces ])
	countData += 1

      print "    ],"
    

def show_routes():
    # Getting Total Routes
    if typeOS() == "SunOS" or typeOS().endswith("BSD"):
      numRoutes = subprocess.Popen("(%s -rn -f inet|%s -i -e '^[0-9]' -e '^default'|tr -s ' '|wc -l) 2>%s" % (path('netstat'), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      totalRoutes = int(numRoutes.stdout.read())

    else:
      numRoutes = subprocess.Popen("(%s -rn|%s '^[0-9]'|tr -s ' '|wc -l) 2>%s" % (path('netstat'), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      totalRoutes = int(numRoutes.stdout.read())

    if totalRoutes > 0:
      print "    \"routes\": ["

      # Executing netstat to get Data
      if typeOS() == "SunOS" or typeOS().endswith("BSD"):
	data = subprocess.Popen("(%s -rn -f inet|%s -i -e '^[0-9]' -e '^default'|tr -s ' ') 2>%s" % (path('netstat'), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      else:
	data = subprocess.Popen("(%s -rn|%s '^[0-9]'|tr -s ' ') 2>%s" % (path('netstat'), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countData = 1
      destination = gateway = mask = flags = interface = ""
      for line in data.stdout.readlines():
        route = line.strip()
        print "      {"

	if typeOS() == "SunOS":
          destination = route.split(' ')[0].strip()
          gateway = route.split(' ')[1].strip()
          flags = route.split(' ')[2].strip()
	  try:
            interface = route.split(' ')[5].strip()
	  except:
	    interface = ""

	elif typeOS().endswith("BSD"):
          destination = route.split(' ')[0].strip()
          gateway = route.split(' ')[1].strip()
          flags = route.split(' ')[2].strip()
          try:
            interface = route.split(' ')[5].strip()
          except:
            interface = ""

    	else: 
          destination = route.split(' ')[0].strip()
          gateway = route.split(' ')[1].strip()
          mask = route.split(' ')[2].strip()
          flags = route.split(' ')[3].strip()
          interface = route.split(' ')[7].strip()

	print "        \"num\": \"%s\"," % (countData)
        print "        \"destination\": \"%s\"," % (destination)
	print "        \"gateway\": \"%s\"," % (gateway)
	print "        \"mask\": \"%s\"," % (mask)
	print "        \"flags\": \"%s\"," % (flags)
	print "        \"interface\": \"%s\"" % (interface)
        print "      }%s" % (("",",") [ countData < totalRoutes ])
        countData += 1

      print "    ],"


def show_users():
    # Getting Total Users
    numUsers = subprocess.Popen("(cat /etc/passwd|%s -v '^$'|%s -v '^#'|wc -l) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    totalUsers = int(numUsers.stdout.read())
    if totalUsers > 0:
      print "    \"lusers\": ["
      # Getting Users
      countUsers = 1
      usersData = subprocess.Popen("(cat /etc/passwd|%s -v '^$'|%s -v '^#'|sort) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for lineUser in usersData.stdout.readlines():
	print "      {"
	name = lineUser.split(':')[0].strip()
	# Getting Password Type and Last Change
	passwdData = lineUser.split(':')[1].strip()
	if passwdData != "x": 	
	  passwdType = "Crypted"  
	  lastChange = ""
	else:
	  # Checking shadow File 
	  shadowData = subprocess.Popen("(cat /etc/shadow|%s '^%s:') 2>%s" % (grep, name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	  shadowLine = shadowData.stdout.read().strip()
	  if shadowLine != "":
	    passwd = shadowLine.split(':')[1].strip()
	    if passwd == "*LK*":
	      passwdType = "User Blocked"
	    elif passwd.startswith('*') or passwd.startswith('!') or passwd == "NP":
	      passwdType = "Password Blocked" 
	    elif passwd == "":
	      passwdType = "No password" 
	    else:
	      passwdType = "Crypted"

	    # Change days to seconds (from shadow file)
	    try:
	      lastChangeSeconds = int(shadowLine.split(':')[2].strip())*86400
	      lastChange = datetime.datetime.fromtimestamp(lastChangeSeconds).strftime("%Y-%m-%d")
	    except:
	      lastChange = "" 
	  else:
	    passwdType = ""
	    lastChange = ""
	
	uid = lineUser.split(':')[2].strip()
	gid = lineUser.split(':')[3].strip()
	description = lineUser.split(':')[4].strip()
	home = lineUser.split(':')[5].strip()
	shell = lineUser.split(':')[6].strip()
        print "        \"name\": \"%s\"," % (name)
        print "        \"uid\": \"%s\"," % (uid)
	print "        \"gid\": \"%s\"," % (gid)
	print "        \"passwdType\": \"%s\"," % (passwdType)
	print "        \"lastChange\": \"%s\"," % (lastChange)
	print "        \"description\": \"%s\"," % (formatCad(description))
	print "        \"home\": \"%s\"," % (formatCad(home))
	print "        \"shell\": \"%s\"" % (formatCad(shell))

        print "      }%s" % (("",",") [ countUsers < totalUsers ])
        countUsers += 1

      print "    ],"


def show_groups():
    # Getting Total Groups
    numGroups = subprocess.Popen("(cat /etc/group|%s -v '^$'|%s -v '^#'|wc -l) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    totalGroups = int(numGroups.stdout.read())
    if totalGroups > 0:
      print "    \"lgroups\": ["
      # Getting Groups
      countGroups = 1
      groupsData = subprocess.Popen("(cat /etc/group|%s -v '^$'|%s -v '^#'|sort) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for lineGroup in groupsData.stdout.readlines():
	print "      {"
	name = lineGroup.split(':')[0].strip()
	gid = lineGroup.split(':')[2].strip()
	usersData = lineGroup.split(':')[3].strip()
	print "        \"name\": \"%s\"," % (name)	
	print "        \"gid\": \"%s\"," % (gid)
	# Getting Users
	print "        \"users\": ["
	if usersData != "":
	  usersList = map(str.strip, usersData.split(','))
	  usersList = filter(bool, usersList)
	  countUsers = 1
          for user in usersList:
            print "          \"%s\"%s" % (user.strip(), ("",",") [ countUsers < len(usersList) ])
            countUsers += 1
	
	print "        ]"

        print "      }%s" % (("",",") [ countGroups < totalGroups ])
        countGroups += 1

      print "    ],"


def show_sudoers():
    # /etc/sudoers exists?
    sudoersFile = int(subprocess.Popen("([ -r /etc/sudoers ] && echo '1' || echo '0') 2>%s" % (errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if sudoersFile > 0:
      print "    \"sudoers\": {"
      # Getting Defaults
      print "      \"defaults\": [" 
      totalDefaults = int(subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s -i '^Defaults'|tr '\t' ' '|tr -s ' '|wc -l) 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
      countDefaults = 1
      dataDefaults = subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s -i '^Defaults'|tr '\t' ' '|tr -s ' ') 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for lineDefault in dataDefaults.stdout.readlines():
	print "        {"
	print "          \"num\": \"%s\"," % (countDefaults)
	print "          \"rule\": \"%s\"" % (formatCad(lineDefault.strip()))
	print "        }%s" % (("",",") [ countDefaults < totalDefaults ])
	countDefaults += 1

      print "      ],"

      # Getting User_Alias
      print "      \"userAlias\": ["
      totalUserAlias = int(subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^User_Alias'|%s 's/User_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' '|wc -l) 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
      dataUserAlias = subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^User_Alias'|%s 's/User_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' ') 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countUserAlias = 1
      for lineUserAlias in dataUserAlias.stdout.readlines():
	print "        {"
	rule = lineUserAlias.strip()
	label = lineUserAlias.strip().split('=',1)[0].strip()
	usersList = lineUserAlias.strip().split('=',1)[1].strip().split(',')
	print "          \"numAlias\": \"%s\"," % (countUserAlias)
	print "          \"rule\": \"%s\"," % (rule)
        print "          \"label\": \"%s\"," % (label)
	print "          \"items\": ["
        countUsers = 1
        for user in usersList:
          print "            {"
          print "              \"numItem\": \"%s\"," % (countUsers)
          print "              \"item\": \"%s\"" % (user.strip())
          print "            }%s" % (("",",") [ countUsers < len(usersList) ])
          countUsers += 1

        print "          ]"
	print "        }%s" % (("",",") [ countUserAlias < totalUserAlias ])
	countUserAlias += 1
	
      print "      ],"

      # Getting Runas_Alias
      print "      \"runasAlias\": ["
      totalRunasAlias = int(subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^Runas_Alias'|%s 's/Runas_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' '|wc -l) 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
      dataRunasAlias = subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^Runas_Alias'|%s 's/Runas_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' ') 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countRunasAlias = 1
      for lineRunasAlias in dataRunasAlias.stdout.readlines():
        print "        {"
        rule = lineRunasAlias.strip()
        label = lineRunasAlias.strip().split('=',1)[0].strip()
        runasList = lineRunasAlias.strip().split('=',1)[1].strip().split(',')
	print "          \"numAlias\": \"%s\"," % (countRunasAlias)
        print "          \"rule\": \"%s\"," % (rule)
        print "          \"label\": \"%s\"," % (label)
        print "          \"items\": ["
        countRunas = 1
        for runas in runasList:
          print "            {"
          print "              \"numItem\": \"%s\"," % (countRunas)
          print "              \"item\": \"%s\"" % (runas.strip())
          print "            }%s" % (("",",") [ countRunas < len(runasList) ])
          countRunas += 1

        print "          ]"
        print "        }%s" % (("",",") [ countRunasAlias < totalRunasAlias ])
        countRunasAlias += 1

      print "      ],"

      # Getting Host_Alias
      print "      \"hostAlias\": ["
      totalHostAlias = int(subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^Host_Alias'|%s 's/Host_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' '|wc -l) 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
      dataHostAlias = subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^Host_Alias'|%s 's/Host_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' ') 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countHostAlias = 1
      for lineHostAlias in dataHostAlias.stdout.readlines():
        print "        {"
        rule = lineHostAlias.strip()
        label = lineHostAlias.strip().split('=',1)[0].strip()
        hostsList = lineHostAlias.strip().split('=',1)[1].strip().split(',')
	print "          \"numAlias\": \"%s\"," % (countHostAlias)
        print "          \"rule\": \"%s\"," % (rule)
        print "          \"label\": \"%s\"," % (label)
        print "          \"items\": ["
        countHosts = 1
        for host in hostsList:
          print "            {"
          print "              \"numItem\": \"%s\"," % (countHosts)
          print "              \"item\": \"%s\"" % (host.strip())
          print "            }%s" % (("",",") [ countHosts < len(hostsList) ])
          countHosts += 1

        print "          ]"
        print "        }%s" % (("",",") [ countHostAlias < totalHostAlias ])
        countHostAlias += 1

      print "      ],"

      # Getting Cmnd_Alias
      print "      \"cmndAlias\": ["
      totalCmndAlias = int(subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^Cmnd_Alias'|%s 's/Cmnd_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' '|wc -l) 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
      dataCmndAlias = subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -i '^Cmnd_Alias'|%s 's/Cmnd_Alias//Ig'|%s 's/\\t//g'|tr ':' '\n'|tr '\t' ' ') 2>%s" % (sed, sed, grep, sed, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countCmndAlias = 1
      for lineCmndAlias in dataCmndAlias.stdout.readlines():
        print "        {"
	rule = lineCmndAlias.strip()
        label = lineCmndAlias.strip().split('=',1)[0].strip()
        cmndsList = lineCmndAlias.strip().split('=',1)[1].strip().split(',')
	print "          \"numAlias\": \"%s\"," % (countCmndAlias)
	print "          \"rule\": \"%s\"," % (rule)
	print "          \"label\": \"%s\"," % (label)
        print "          \"items\": ["
        countCmnds = 1
        for cmnd in cmndsList:
          print "            {"
          print "              \"numItem\": \"%s\"," % (countCmnds)
          print "              \"item\": \"%s\"" % (cmnd.strip())
          print "            }%s" % (("",",") [ countCmnds < len(cmndsList) ])
          countCmnds += 1

        print "          ]"
        print "        }%s" % (("",",") [ countCmndAlias < totalCmndAlias ])
        countCmndAlias += 1

      print "      ],"

      # Getting User Specification 
      print "      \"userSpec\": ["
      totalUserSpec = int(subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -v '^#'|%s -iv '^Defaults'|%s -iv '^User_Alias'|%s -iv '^Runas_Alias'|%s -iv '^Host_Alias'|%s -iv '^Cmnd_Alias'|%s '='|%s '{ gsub(/ : /, \"\\n\"$1\" \"); print }'|tr '\t' ' '|wc -l) 2>%s" % (sed, sed, grep, grep, grep, grep, grep, grep, grep, awk, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
      dataUserSpec = subprocess.Popen("(cat /etc/sudoers|%s 's/#.*//g'|%s ':a;N;$!ba;s/\\\\\\n/ /g'|%s -v '^#'|%s -iv '^Defaults'|%s -iv '^User_Alias'|%s -iv '^Runas_Alias'|%s -iv '^Host_Alias'|%s -iv '^Cmnd_Alias'|%s '='|%s '{ gsub(/ : /, \"\\n\"$1\" \"); print }'|tr '\t' ' ') 2>%s" % (sed, sed, grep, grep, grep, grep, grep, grep, grep, awk, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countUserSpec = 1
      for lineUserSpec in dataUserSpec.stdout.readlines():
        print "        {"
        rule = lineUserSpec.strip()
        user = lineUserSpec.strip().split('=',1)[0].split(' ',1)[0].strip()
	host = lineUserSpec.strip().split('=',1)[0].split(' ',1)[1].strip()
	if ('(' in lineUserSpec.strip().split('=',1)[1]) and (')' in lineUserSpec.strip().split('=',1)[1]):
	  runas = lineUserSpec.strip().split('=',1)[1].split('(',1)[1].split(')',1)[0].strip()
	  cmnd = lineUserSpec.strip().split('=',1)[1].split(')',1)[1].strip()
	else:
	  runas = ""
	  cmnd = lineUserSpec.strip().split('=',1)[1].strip()

	print "          \"num\": \"%s\"," % (countUserSpec)
        print "          \"rule\": \"%s\"," % (rule)
	print "          \"userItem\": \"%s\"," % user
	print "          \"hostItem\": \"%s\"," % host 
        print "          \"runasItem\": \"%s\"," % runas 
        print "          \"cmndItem\": \"%s\"" % cmnd 
        print "        }%s" % (("",",") [ countUserSpec < totalUserSpec ])
        countUserSpec += 1

      print "      ]"

      print "    },"


def show_resolver():
    print "    \"resolver\": {"
    # Getting Domain 
    domain = subprocess.Popen("(cat /etc/resolv.conf|%s '^domain'|tail -1|%s 's/^domain//') 2>%s" % (grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"domain\": \"%s\"," % (domain)

    # Getting Search domains
    search = subprocess.Popen("(cat /etc/resolv.conf|%s '^search'|tail -1|%s 's/^search//') 2>%s" % (grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"search\": \"%s\"," % (search)    

    # Getting Nameserver 
    totalNS = int(subprocess.Popen("(cat /etc/resolv.conf|%s '^nameserver'|head -3|wc -l) 2>%s" % (grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    countNS = 1
    dataNS = subprocess.Popen("(cat /etc/resolv.conf|%s '^nameserver'|%s 's/^nameserver//'|head -3) 2>%s" % (grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    for lineNS in dataNS.stdout.readlines():
      print "      \"ns%s\": \"%s\"," % (countNS, lineNS.strip())
      countNS += 1

    # If namserver count less than 3
    while countNS <= 3:
      print "      \"ns%s\": \"\"," % (countNS) 
      countNS += 1

    # Getting Options
    totalOptions = int(subprocess.Popen("(cat /etc/resolv.conf|%s '^options'|wc -l) 2>%s" % (grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    countOptions = 1
    dataOptions = subprocess.Popen("(cat /etc/resolv.conf|%s '^options'|%s 's/^options//') 2>%s" % (grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    print "      \"options\": ["
    for lineOption in dataNS.stdout.readlines():
      print "      \"%s\"%s" % (lineOption.strip(), ("",",") [ countOptions < totalOptions ])
      countOptions += 1

    print "      ]"

    print "    },"


def show_hosts():
    print "    \"hosts\": ["
    # Getting hosts 
    totalHosts = int(subprocess.Popen("(cat /etc/hosts|%s 's/#.*//g'|tr '\t' ' '|tr -s ' '|%s -v '^$'|wc -l) 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if totalHosts > 0:
      countHosts = 1
      dataHosts = subprocess.Popen("(cat /etc/hosts|%s 's/#.*//g'|tr '\t' ' '|tr -s ' '|%s -v '^$') 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for lineHost in dataHosts.stdout.readlines():
	print "      {"
        ipHost = lineHost.split(' ',1)[0].strip()
	print "        \"num\": \"%s\"," % (countHosts)
        print "        \"ip\": \"%s\"," % (ipHost)
	print "        \"rule\": \"%s\"," % (lineHost.strip())
	print "        \"aliases\": ["
        aliasHost = lineHost.split(' ',1)[1].split(' ')
	countAlias = 1
        for alias in aliasHost:
	  print "          {"
	  print "            \"num\": \"%s\"," % (countAlias) 
          print "            \"name\": \"%s\"" % (alias.strip())
	  print "          }%s" % (("",",") [ countAlias < len(aliasHost) ])
	  countAlias += 1
	
	print "        ]"
	print "      }%s" % (("",",") [ countHosts < totalHosts ])
        countHosts += 1

    print "    ],"

def show_iptables():
    # Getting Total Tables
    numTables = subprocess.Popen("(%s -nL >/dev/null;%s|%s '^*'|wc -l) 2>%s" % (path('iptables'), path('iptables-save'), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    totalTables = int(numTables.stdout.read()) 
    if totalTables > 0:
      print "    \"iptables\": ["
      # Getting Tables
      countTables = 1 
      tables = subprocess.Popen("(%s|%s '^\*'|cut -d '*' -f2) 2>%s" % (path('iptables-save'), grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for lineTable in tables.stdout.readlines():
	print "       {"
	table = lineTable.strip() 
	print "         \"table\": \"%s\"," % (table)
	numPolicies = subprocess.Popen("(%s -t %s|%s '^:'|wc -l) 2>%s" % (path('iptables-save'), table, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	totalPolicies = int(numPolicies.stdout.read()) 
	if totalPolicies > 0:
	  print "         \"policies\": ["
	  countPolicies = 1 
          policies = subprocess.Popen("(%s -t %s|%s '^:'|cut -d ':' -f2|cut -d ' ' -f1,2) 2>%s" % (path('iptables-save'), table, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	  for linePolicy in policies.stdout.readlines():
	    print "           {"
	    chain = linePolicy.split(' ',1)[0].strip()
	    policy = linePolicy.split(' ',1)[1].strip()
	    print "             \"chain\": \"%s\"," % (chain)		
	    print "             \"policy\": \"%s\"," % (policy)
	    print "             \"rules\": ["

	    numRules = subprocess.Popen("(%s -t %s|%s '%s'|%s -v '^:'|wc -l) 2>%s" % (path('iptables-save'), table, grep, chain, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
            totalRules = int(numRules.stdout.read())
	    if totalRules > 0:
	      countRules = 1
	      rules = subprocess.Popen("(%s -t %s|%s '%s'|%s -v '^:') 2>%s" % (path('iptables-save'), table, grep, chain, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	      for lineRule in rules.stdout.readlines():
		print "               {"	
		rule = lineRule.strip()
		print "                 \"num\": \"%s\"," % (countRules)
		print "                 \"rule\": \"%s\"," % (rule)	
		# Getting parameters
		listRules = rule.split(' ')
		srcValue = dstValue = inValue = outValue = protocolValue = "" 
		stateValue = jumpValue = sportValue = dportValue = "" 
		for index, opt in enumerate(listRules):
		  if opt.startswith('-') and index+1<len(listRules):
		    arg = listRules[index+1] 
                    if opt in ('-i', '--in-interface'):
                      inValue = arg 
                    elif opt in ('-o', '--out-interface'):
                      out = arg 
		    elif opt in ('-s', '--source', '--src'):
		      srcValue = arg 
		    elif opt in ('-d', '--destination', '--dst'):
		      dstValue = arg 
                    elif opt in ('-p', '--protocol'):
		      protocolValue = arg 
                    elif opt in ('--sport', '--sports', '--source-port', '--source-ports'):
                      sportValue = arg 
                    elif opt in ('--dport', '--dports', '--destination-port', '--destination-ports'):
                      dportValue = arg 
                    elif opt in ('-m', '--state'):
		      stateValue = arg
                    elif opt in ('-j', '--jump'):
		      jumpValue = arg 

		# Printing parameters
		print "                 \"in\": \"%s\"," % (inValue)
		print "                 \"out\": \"%s\"," % (outValue)
		print "                 \"src\": \"%s\"," % (srcValue)
		print "                 \"dst\": \"%s\"," % (dstValue)
		print "                 \"protocol\": \"%s\"," % (protocolValue)
		print "                 \"sport\": \"%s\"," % (sportValue)
		print "                 \"dport\": \"%s\"," % (dportValue)
		print "                 \"state\": \"%s\"," % (stateValue)
		print "                 \"jump\": \"%s\"" % (jumpValue)

		print "               }%s" % (("",",") [ countRules < totalRules ])
		countRules += 1

	    print "             ]"		

	    print "           }%s" % (("",",") [ countPolicies < totalPolicies ])
	    countPolicies += 1

	  print "         ]"

	print "       }%s" % (("",",") [ countTables < totalTables ])
	countTables += 1
		
      print "    ],"
      

def show_tcpWrappers():
    # Getting Total TCP Wrappers 
    if typeOS().endswith("BSD"):
      totalTWAllow = int(subprocess.Popen("(cat /etc/hosts.allow|%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'allow *$'|cut -d':' -f1|tr -d ' '|tr ',' '\n'|sort|uniq|wc -l|tr -d ' ') 2>%s" % (sed, awk, grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
      totalTWDeny = int(subprocess.Popen("(cat /etc/hosts.allow|%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'deny *$'|cut -d':' -f1|tr -d ' '|tr ',' '\n'|sort|uniq|wc -l|tr -d ' ') 2>%s" % (sed, awk, grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())

    else:
      totalTWAllow = int(subprocess.Popen("(cat /etc/hosts.allow|%s 's/#.*//g'|%s ':'|cut -d':' -f1|tr -d ' '|tr ',' '\n'|sort|uniq|wc -l) 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
      totalTWDeny = int(subprocess.Popen("(cat /etc/hosts.deny|%s 's/#.*//g'|%s ':'|cut -d':' -f1|tr -d ' '|tr ',' '\n'|sort|uniq|wc -l) 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())

    if totalTWAllow > 0 or totalTWDeny > 0:
      print "    \"tcpwrappers\": {"
      # Hosts.allow
      if totalTWAllow > 0:
	print "      \"allow\": ["
        # Getting TW Allow
        countTWAllow = 1
	if typeOS().endswith("BSD"):
	  TWAllow = subprocess.Popen("(cat /etc/hosts.allow|%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'allow *$'|cut -d':' -f1|tr -d ' '|tr ',' '\n'|sort|uniq) 2>%s" % (sed, awk, grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

	else:
	  TWAllow = subprocess.Popen("(cat /etc/hosts.allow|%s 's/#.*//g'|%s ':'|cut -d':' -f1|tr ',' '\n'|sort|uniq) 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        for lineTWAllow in TWAllow.stdout.readlines():
	  print "        {" 
          serviceTWAllow = lineTWAllow.strip()
          print "          \"service\": \"%s\"," % (serviceTWAllow)
	  if typeOS().endswith("BSD"):
            totalHostsTWAllow = int(subprocess.Popen("(cat /etc/hosts.allow |%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'allow *$'|%s '^%s\|, *%s'|%s -e :1 -e 's/\\(\\[.*\\):\\(.*\\]\\)/\\1#\\2/;t1'|cut -d':' -f2|tr '#' ':'|tr '\t' ' '|tr -s ' '|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^ *$'|sort|uniq|wc -l) 2>%s" % (sed, awk, grep, grep, grep, serviceTWAllow, serviceTWAllow, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	    hostsTWAllow = subprocess.Popen("(cat /etc/hosts.allow |%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'allow *$'|%s '^%s\|, *%s'|%s -e :1 -e 's/\\(\\[.*\\):\\(.*\\]\\)/\\1#\\2/;t1'|cut -d':' -f2|tr '#' ':'|tr '\t' ' '|tr -s ' '|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^ *$'|sort|uniq) 2>%s" % (sed, awk, grep, grep, grep, serviceTWAllow, serviceTWAllow, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

	  else:
	    totalHostsTWAllow = int(subprocess.Popen("(cat /etc/hosts.allow |%s 's/#.*//g'|%s ':'|%s '^%s\|, *%s'|cut -d':' -f2|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^$'|sort|uniq|wc -l) 2>%s" % (sed, grep, grep, serviceTWAllow, serviceTWAllow, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	    hostsTWAllow = subprocess.Popen("(cat /etc/hosts.allow |%s 's/#.*//g'|%s ':'|%s '^%s\|, *%s'|cut -d':' -f2|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^$'|sort|uniq) 2>%s" % (sed, grep, grep, serviceTWAllow, serviceTWAllow, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

	  print "          \"hosts\": ["
	  countHostsTWAllow = 1
	  for lineHostsTWAllow in hostsTWAllow.stdout.readlines():
	    print "            \"%s\"%s" % (lineHostsTWAllow.strip(), ("",",") [ countHostsTWAllow < totalHostsTWAllow ])
	    countHostsTWAllow += 1

	  print "          ]"

	  print "        }%s" % (("",",") [ countTWAllow < totalTWAllow ])

	  countTWAllow += 1

	print "      ]%s" % (("",",") [ totalTWDeny > 0 ])

      # Hosts.deny
      if totalTWDeny > 0:
        print "      \"deny\": ["
        # Getting TW Deny 
        countTWDeny = 1
	if typeOS().endswith("BSD"):
	  TWDeny = subprocess.Popen("(cat /etc/hosts.allow|%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'deny *$'|cut -d':' -f1|tr -d ' '|tr ',' '\n'|sort|uniq) 2>%s" % (sed, awk, grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

	else:
	  TWDeny = subprocess.Popen("(cat /etc/hosts.deny|%s 's/#.*//g'|%s ':'|cut -d':' -f1|tr ',' '\n'|sort|uniq) 2>%s" % (sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        for lineTWDeny in TWDeny.stdout.readlines():
          print "        {"
          serviceTWDeny = lineTWDeny.strip()
          print "          \"service\": \"%s\"," % (serviceTWDeny)
	  if typeOS().endswith("BSD"):
            totalHostsTWDeny = int(subprocess.Popen("(cat /etc/hosts.allow |%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'deny *$'|%s '^%s\|, *%s'|%s -e :1 -e 's/\\(\\[.*\\):\(.*\\]\\)/\\1#\\2/;t1'|cut -d':' -f2|tr '#' ':'|tr '\t' ' '|tr -s ' '|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^ *$'|sort|uniq|wc -l) 2>%s" % (sed, awk, grep, grep, grep, serviceTWDeny, serviceTWDeny, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	    hostsTWDeny = subprocess.Popen("(cat /etc/hosts.allow |%s 's/#.*//g'|%s 'BEGIN {RS=\"\"}{gsub(/\\\\\\n/,\" \",$0); print $0}'|%s ':'|%s 'deny *$'|%s '^%s\|, *%s'|%s -e :1 -e 's/\\(\\[.*\\):\\(.*\\]\\)/\\1#\\2/;t1'|cut -d':' -f2|tr '#' ':'|tr '\t' ' '|tr -s ' '|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^ *$'|sort|uniq) 2>%s" % (sed, awk, grep, grep, grep, serviceTWDeny, serviceTWDeny, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

	  else:
	    totalHostsTWDeny = int(subprocess.Popen("(cat /etc/hosts.deny |%s 's/#.*//g'|%s ':'|%s '^%s\|, *%s'|cut -d':' -f2|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^$'|sort|uniq|wc -l) 2>%s" % (sed, grep, grep, serviceTWDeny, serviceTWDeny, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	    hostsTWDeny = subprocess.Popen("(cat /etc/hosts.deny |%s 's/#.*//g'|%s ':'|%s '^%s\|, *%s'|cut -d':' -f2|%s '/ EXCEPT /Ib; s/ /\\n/g'|%s -v '^$'|sort|uniq) 2>%s" % (sed, grep, grep, serviceTWDeny, serviceTWDeny, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

          print "          \"hosts\": ["
          countHostsTWDeny = 1
          for lineHostsTWDeny in hostsTWDeny.stdout.readlines():
            print "            \"%s\"%s" % (lineHostsTWDeny.strip(), ("",",") [ countHostsTWDeny < totalHostsTWDeny ])
            countHostsTWDeny += 1

          print "          ]"

          print "        }%s" % (("",",") [ countTWDeny < totalTWDeny ])

          countTWDeny += 1

        print "      ]"

      print "    },"


def show_pamAccess():
    # Getting Total PAM modules calling pam_access
    if typeOS().endswith("BSD"):
      totalModules = int(subprocess.Popen("(%s -l 'pam_login_access' /etc/pam.d/*|%s -v '^#'|wc -l) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    else:
      totalModules = int(subprocess.Popen("(%s -l 'pam_access' /etc/pam.d/*|%s -v '^#'|wc -l) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    if totalModules > 0:
      print "    \"pamaccess\": {"
      print "      \"modules\": ["
      # Getting modules PAM
      if typeOS().endswith("BSD"):
        modulesData = subprocess.Popen("(%s -l 'pam_login_access' /etc/pam.d/*|%s -v '^#') 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      else:
	modulesData = subprocess.Popen("(%s -l 'pam_access' /etc/pam.d/*|%s -v '^#') 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      countModules = 1
      for lineModules in modulesData.stdout.readlines():
	print "        \"%s\"%s" % (lineModules.strip(), ("",",") [ countModules < totalModules ])
	countModules += 1

      print "      ],"

      # Getting Total PAM Access rules from access file 
      if typeOS().endswith("BSD"):      
	totalRules = int(subprocess.Popen("(cat /etc/login.access|%s -v '^#'|%s ':'|wc -l) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

      else:
	totalRules = int(subprocess.Popen("(cat /etc/security/access.conf|%s -v '^#'|%s ':'|wc -l) 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

      print "      \"rules\": ["
      # Getting rules
      countRules = 1
      if typeOS().endswith("BSD"):
	rulesData = subprocess.Popen("(cat /etc/login.access|%s -v '^#'|%s ':') 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      else:
	rulesData = subprocess.Popen("(cat /etc/security/access.conf|%s -v '^#'|%s ':') 2>%s" % (grep, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      for lineRules in rulesData.stdout.readlines():
        print "        {"
	rule = lineRules.strip()
	type = rule.split(':')[0].strip()
	usersData = rule.split(':')[1].strip()
	originsData = rule.split(':',2)[2].strip()
	print "          \"num\": \"%s\"," % (countRules)
	print "          \"rule\": \"%s\"," % (rule)	
	print "          \"type\": \"%s\"," % (type)
	
	# Getting users
	print "          \"users\": ["
	if "EXCEPT" in usersData.upper():
          print "            \"%s\"" % (usersData)
	else:
	  usersList = usersData.split(' ')
	  countUsers = 1
	  for user in usersList:
	    print "            \"%s\"%s" % (user, ("",",") [ countUsers < len(usersList) ])
	    countUsers += 1

	print "          ],"
	     
        # Getting origins
        print "          \"origins\": ["
        if "EXCEPT" in originsData.upper():
          print "            \"%s\"" % (originsData)
        else:
          originsList = originsData.split(' ')
          countOrigins = 1
          for origin in originsList:
            print "            \"%s\"%s" % (origin, ("",",") [ countOrigins < len(originsList) ])
	    countOrigins += 1

        print "          ]"

	print "        }%s" % (("",",") [ countRules < totalRules ])

	countRules += 1

      print "      ]"
      print "    },"


def show_crontabs():

    print "    \"crontabs\": ["

    # Getting Data
    if typeOS() == "SunOS":
      totalRules = int(subprocess.Popen("(for user in $(cat /etc/passwd|%s -v '^#'|cut -d ':' -f1); do (IFS=$'\n'; for rule in $((%s -l $user|%s -v '^#'|%s 's/^@hourly/0 * * * */g'|%s 's/^@daily\|^@midnight/0 0 * * */g'|%s 's/^@weekly/0 0 * * 0/g'|%s 's/^@monthly/0 0 1 * */g'|%s 's/^@yearly\|^annually/0 0 1 1 */g'|%s '^[0-9|*]'|tr '\t' ' '|tr -s ' ') 2>/dev/null); do echo \"$user $rule\"; done); done|wc -l) 2>%s" % (grep, path('crontab'), grep, sed, sed, sed, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

      rulesData = subprocess.Popen("(for user in $(cat /etc/passwd|%s -v '^#'|cut -d ':' -f1); do (IFS=$'\n'; for rule in $((%s -l $user|%s -v '^#'|%s 's/^@hourly/0 * * * */g'|%s 's/^@daily\|^@midnight/0 0 * * */g'|%s 's/^@weekly/0 0 * * 0/g'|%s 's/^@monthly/0 0 1 * */g'|%s 's/^@yearly\|^annually/0 0 1 1 */g'|%s '^[0-9|*]'|tr '\t' ' '|tr -s ' ') 2>/dev/null); do echo \"$user $rule\"; done); done) 2>%s" % (grep, path('crontab'), grep, sed, sed, sed, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    else:
      totalRules = int(subprocess.Popen("(for user in $(cat /etc/passwd|%s -v '^#'|cut -d ':' -f1); do (IFS=$'\n'; for rule in $((%s -u $user -l|%s -v '^#'|%s 's/^@hourly/0 * * * */g'|%s 's/^@daily\|^@midnight/0 0 * * */g'|%s 's/^@weekly/0 0 * * 0/g'|%s 's/^@monthly/0 0 1 * */g'|%s 's/^@yearly\|^annually/0 0 1 1 */g'|%s '^[0-9|*]'|tr '\t' ' '|tr -s ' ') 2>/dev/null); do echo \"$user $rule\"; done); done|wc -l) 2>%s" % (grep, path('crontab'), grep, sed, sed, sed, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

      rulesData = subprocess.Popen("(for user in $(cat /etc/passwd|%s -v '^#'|cut -d ':' -f1); do (IFS=$'\n'; for rule in $((%s -u $user -l|%s -v '^#'|%s 's/^@hourly/0 * * * */g'|%s 's/^@daily\|^@midnight/0 0 * * */g'|%s 's/^@weekly/0 0 * * 0/g'|%s 's/^@monthly/0 0 1 * */g'|%s 's/^@yearly\|^annually/0 0 1 1 */g'|%s '^[0-9|*]'|tr '\t' ' '|tr -s ' ') 2>/dev/null); do echo \"$user $rule\"; done); done) 2>%s" % (grep, path('crontab'), grep, sed, sed, sed, sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    countRules = 1
    for lineRules in rulesData.stdout.readlines():
      ruleUser = lineRules.strip().split(' ',6)[0]
      ruleMinute = lineRules.strip().split(' ',6)[1]
      ruleHour = lineRules.strip().split(' ',6)[2]
      ruleDay = lineRules.strip().split(' ',6)[3]
      ruleMonth = lineRules.strip().split(' ',6)[4]
      ruleDayWeek = lineRules.strip().split(' ',6)[5]
      ruleCommand = lineRules.strip().split(' ',6)[6] 
      print "      {"
      print "        \"num\": \"%s\"," % (countRules)
      print "        \"user\": \"%s\"," % (ruleUser)
      print "        \"minute\": \"%s\"," % (ruleMinute)
      print "        \"hour\": \"%s\"," % (ruleHour)
      print "        \"day\": \"%s\"," % (ruleDay)
      print "        \"month\": \"%s\"," % (ruleMonth)
      print "        \"dayWeek\": \"%s\"," % (ruleDayWeek)
      print "        \"command\": \"%s\"" % (formatCad(ruleCommand))
      print "      }%s" % (("",",") [ countRules < totalRules ])
      countRules += 1

    print "    ],"


def show_ports(protocol):
    if protocol == 'tcp':
      param = '-tln'
    else:
      param = '-uln'

    if typeOS().endswith("BSD"):
      totalPorts = int(subprocess.Popen("(%s -an -p %s |%s %s|%s -v 'ESTABLISHED'|tr -s ' '|cut -d' ' -f4|%s 's/^.*\\.//g'|sort|uniq|wc -l) 2>%s" % (path('netstat'), protocol, grep, protocol, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    elif typeOS() == "SunOS":
      totalPorts = int(subprocess.Popen("(%s -an -f inet -f inet6 -P %s|tr '\t' ' '|tr -s ' '|%s -i '%s'|%s 's/^ *//g'|cut -d' ' -f1|%s 's/^.*\\././g'|cut -d'.' -f2|cut -d' ' -f1|%s '^[0-9]'|sort|uniq|wc -l) 2>%s" % (path('netstat'), protocol, grep, ('Idle','LISTEN') [ protocol == 'tcp' ], sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    else:
      totalPorts = int(subprocess.Popen("(%s %s |%s %s|%s '{gsub(\".*:\",\"\",$4);print $4}'|sort|uniq|wc -l) 2>%s" % (path('netstat'), param, grep, protocol, awk, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())

    if totalPorts > 0:
      print "    \"%s\": [" % (protocol)
      cont = 1
      if typeOS().endswith("BSD"):
	ports = subprocess.Popen("(%s -an -p %s |%s %s|%s -v 'ESTABLISHED'|tr -s ' '|cut -d' ' -f4|%s 's/^.*\\.//g'|sort|uniq) 2>%s" % (path('netstat'), protocol, grep, protocol, grep, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      elif typeOS() == "SunOS":
	ports = subprocess.Popen("(%s -an -f inet -f inet6 -P %s|tr '\t' ' '|tr -s ' '|%s -i '%s'|%s 's/^ *//g'|cut -d' ' -f1|%s 's/^.*\\././g'|cut -d'.' -f2|cut -d' ' -f1|%s '^[0-9]'|sort|uniq) 2>%s" % (path('netstat'), protocol, grep, ('Idle','LISTEN') [ protocol == 'tcp' ], sed, sed, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      else:
	ports = subprocess.Popen("(%s %s |%s %s|%s '{gsub(\".*:\",\"\",$4);print $4}'|sort|uniq) 2>%s" % (path('netstat'), param, grep, protocol, awk, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      for line in ports.stdout.readlines():
	if typeOS().endswith("BSD"):
	  proc = subprocess.Popen("(%s|grep ':%s'|tr -s ' '|cut -d' ' -f2|head -1) 2>%s" % (path('fstat'), line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().rstrip('\n')
	  ip4 = int(subprocess.Popen("(%s -an -p %s -f inet |%s %s|%s -v 'ESTABLISHED'|tr -s ' '|cut -d' ' -f4|%s 's/^.*\\.//g'|%s %s|head -1|wc -l) 2>%s" % (path('netstat'), protocol, grep, protocol, grep, sed, grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()) 
	  bindIP4 = subprocess.Popen("(%s -an -p %s -f inet |%s %s|%s -v 'ESTABLISHED'|tr -s ' '|cut -d' ' -f4|%s %s|head -1|%s|cut -d'.' -f2-|%s) 2>%s" % (path('netstat'), protocol, grep, protocol, grep, grep, line.rstrip('\n'), path('rev'), path('rev'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  ip6 = int(subprocess.Popen("(%s -an -p %s -f inet6 |%s %s|%s -v 'ESTABLISHED'|tr -s ' '|cut -d' ' -f4|%s 's/^.*\\.//g'|%s %s|head -1|wc -l) 2>%s" % (path('netstat'), protocol, grep, protocol, grep, sed, grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	  bindIP6 = subprocess.Popen("(%s -an -p %s -f inet6 |%s %s|%s -v 'ESTABLISHED'|tr -s ' '|cut -d' ' -f4|%s %s|head -1|%s|cut -d'.' -f2-|%s) 2>%s" % (path('netstat'), protocol, grep, protocol, grep, grep, line.rstrip('\n'), path('rev'), path('rev'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	elif typeOS() == "SunOS":
	  proc = ""
          ip4 = int(subprocess.Popen("(%s -an -f inet -P %s|tr '\t' ' '|tr -s ' '|%s '%s'|cut -d' ' -f2|%s|cut -d'.' -f1|%s|%s '^%s'|head -1|wc -l) 2>%s" % (path('netstat'), protocol, grep, ('','LISTEN') [ protocol == 'tcp' ], path('rev'), path('rev'), grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
          bindIP4 = subprocess.Popen("(%s -an -f inet -P %s|tr '\t' ' '|tr -s ' '|%s '%s'|cut -d' ' -f2|%s '%s$'|%s|cut -d'.' -f2-|%s|head -1) 2>%s" % (path('netstat'), protocol, grep, ('','LISTEN') [ protocol == 'tcp' ], grep, line.rstrip('\n'), path('rev'), path('rev'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          ip6 = int(subprocess.Popen("(%s -an -f inet6 -P %s|tr '\t' ' '|tr -s ' '|%s '%s'|cut -d' ' -f2|%s|cut -d'.' -f1|%s|%s '^%s'|head -1|wc -l) 2>%s" % (path('netstat'), protocol, grep, ('','LISTEN') [ protocol == 'tcp' ], path('rev'), path('rev'), grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
          bindIP6 = subprocess.Popen("(%s -an -f inet6 -P %s|tr '\t' ' '|tr -s ' '|%s '%s'|cut -d' ' -f2|%s '%s$'|%s|cut -d'.' -f2-|%s|head -1) 2>%s" % (path('netstat'), protocol, grep, ('','LISTEN') [ protocol == 'tcp' ], grep, line.rstrip('\n'), path('rev'), path('rev'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	else:
	  proc = subprocess.Popen("(%s %s -p |%s %s|%s \":%s\"|head -1|cut -d'/' -f2|cut -d' ' -f1) 2>%s" % (path('netstat'), param, grep, protocol, grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().rstrip('\n')
          ip4 = int(subprocess.Popen("(%s %s -p --inet|%s %s|%s \":%s\"|head -1|wc -l) 2>%s" % (path('netstat'), param, grep, protocol, grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	  bindIP4 = subprocess.Popen("(%s %s -p --inet|%s %s|%s \":%s\"|tr '\t' ' '|tr -s ' '|cut -d' ' -f4|cut -d':' -f1|head -1) 2>%s" % (path('netstat'), param, grep, protocol, grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          ip6 = int(subprocess.Popen("(%s %s -p --inet6|%s %s|%s \":%s\"|head -1|wc -l) 2>%s" % (path('netstat'), param, grep, protocol, grep, line.rstrip('\n'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip())
	  bindIP6 = subprocess.Popen("(%s %s -p --inet6|%s %s|%s \":%s\"|tr '\t' ' '|tr -s ' '|cut -d' ' -f4|%s|cut -d':' -f2-|%s|head -1) 2>%s" % (path('netstat'), param, grep, protocol, grep, line.rstrip('\n'), path('rev'), path('rev'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"
        print "        \"port\": \"%s\"," % (line.rstrip('\n'))
        print "        \"ip4\": \"%s\"," % (ip4)
        print "        \"bindIP4\": \"%s\"," % (bindIP4)
        print "        \"ip6\": \"%s\"," % (ip6)
        print "        \"bindIP6\": \"%s\"," % (bindIP6)
        print "        \"process\": \"%s\"" % (proc)
        if cont < totalPorts: 
	  print "      },"
        else:
	  print "      }"

        cont += 1

      print "    ],"


def show_cabecera():
    print "{"
    print "  \"ansible_facts\": {"


def show_pie():
    print "    \"changed\": false"
    print "  }"
    print "}" 


def main():
    show_cabecera()

    global awk, bash, find, grep, sed
    awk = path('gawk','awk')
    bash = getShell()
    find = path('gfind','find')
    grep = path('ggrep','grep')
    sed = path('gsed','sed')

    if dmidecode_OK() == 0:
      show_system()
      show_processor()
      show_memory()	
      show_bios()
      show_baseboard()
      show_baseboard_device()
      show_chassis()
      show_cache()
      show_connector()
      show_slot()

    show_modules()
    show_interfaces()
    show_routes()
    show_users()
    show_groups()
    show_sudoers()
    show_resolver()
    show_hosts()
    show_iptables()
    show_tcpWrappers()
    show_pamAccess()
    show_crontabs()
    show_ports('tcp')
    show_ports('udp')

    show_pie()



if __name__ == '__main__':
    main()

