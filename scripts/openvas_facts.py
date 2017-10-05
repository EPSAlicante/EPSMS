#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
import socket
import os
import sys
import re
import time
import codecs
import shlex


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


def formatCad(cad):
    try:
      retCad = json.dumps(cad.replace("'","\"").replace("{%","(%").replace("%}","%)").replace("{{","((").replace("}}","))")).replace("\\u","\\\\u")[1:-1]
      return retCad

    except:
      return ""


def getFormat(formatType):

    ret = subprocess.Popen("(omp -u admin -w %s -F|tr '\t' ' '|tr -s ' '|grep -i ' %s$'|cut -d' ' -f1) 2>%s" % (passwdAdmin, formatType, errorLog), shell=True, executable='/bin/bash', stdout=subprocess.PIPE).stdout.read().strip()
    return ret


def show_openvas():

    formatReport = getFormat("CSV Hosts")

    print "    \"openvas\": {"

    if formatReport != "":

	hostResults = subprocess.Popen("(omp -u admin -w %s -R %s -f %s|grep -i -e ',%s,' -e '^%s,') 2>%s" % (passwdAdmin, scan, formatReport, server, socket.gethostbyname(server), errorLog), shell=True, executable='/bin/bash', stdout=subprocess.PIPE).stdout.read().strip().split(',')

	if len(hostResults) >= 12:	
          print "      \"Server\": \"%s\"," % (formatCad(server))
          print "      \"IP\": \"%s\"," % (formatCad(hostResults[0]))
	  print "      \"ScanId\": \"%s\"," % (scan)
          print "      \"CVSS\": \"%s\"," % (formatCad(hostResults[5]))
          print "      \"Severity\": \"%s\"," % (formatCad(hostResults[6]))
          print "      \"TotalHigh\": \"%s\"," % (formatCad(hostResults[7]))
          print "      \"TotalMedium\": \"%s\"," % (formatCad(hostResults[8]))
          print "      \"TotalLow\": \"%s\"," % (formatCad(hostResults[9]))
          print "      \"TotalLog\": \"%s\"," % (formatCad(hostResults[10]))
          print "      \"TotalFalsePositive\": \"%s\"," % (formatCad(hostResults[11]))

	  formatReport = getFormat("CSV Results")
	  IPserver = hostResults[0]

	  try:
            totalResults = int(subprocess.Popen("(omp -u admin -w %s -R %s -f %s|tr '\n' ' '|sed 's/%s,/\\n%s,/g'|grep -i '^%s,'|wc -l) 2>%s" % (passwdAdmin, scan, formatReport, IPserver, IPserver, IPserver, errorLog), shell=True, executable='/bin/bash', stdout=subprocess.PIPE).stdout.read())
	  except:
	    totalResults = 0
 
          countResults = 1
          print "      \"Results\": ["

	  if totalResults > 0:

	    dataResults = subprocess.Popen("(omp -u admin -w %s -R %s -f %s|tr '\n' ' '|sed 's/%s,/\\n%s,/g'|grep -i '^%s,'|tr -s ' ') 2>%s" % (passwdAdmin, scan, formatReport, IPserver, IPserver, IPserver, errorLog), shell=True, executable='/bin/bash', stdout=subprocess.PIPE)

	    for lineResults in dataResults.stdout.readlines():

	      # Get fields 1-4
	      lineResults = lineResults.strip().split(',',6)
	      fieldPort = lineResults[2]
	      fieldProtocol = lineResults[3]
	      fieldCVSS = lineResults[4]
	      fieldSeverity = lineResults[5]

	      # Get fields 5,6 
	      nextResults = lineResults[6][1:].split('","',2)
	      fieldNVTName = nextResults[0] 
	      fieldSummary = nextResults[1]

	      # Get field 7
	      nextResults = nextResults[2].split('",',1)
	      fieldSpecificResult = nextResults[0]

	      # Get field 8
	      nextResults = nextResults[1].split(',',1)
	      fieldNVTOID = nextResults[0]

	      # Get field 9
              nextResults = nextResults[1][1:].split('",',1)
              fieldCVE = nextResults[0]

	      # Get field 10
              nextResults = nextResults[1].split(',',1)
              fieldTaskId = nextResults[0] 

              # Get field 11 
              nextResults = nextResults[1][1:].split('",',1)
              fieldTaskName = nextResults[0]

              # Get field 12,13
              nextResults = nextResults[1].split(',',2)
              fieldStartScan = nextResults[0][:-1].replace("T"," ")
	      fieldResultId = nextResults[1]

	      # Get rest of fields
	      nextResults = nextResults[2][1:].split('","',8)
	      fieldImpact = nextResults[0]
	      fieldSolution = nextResults[1]
	      fieldAffectedSoftware = nextResults[2]
	      fieldVulnerabilityInsight = nextResults[3]
	      fieldDetectionMethod = nextResults[4]
	      fieldProductDetectionResult = nextResults[5]
	      fieldBID = nextResults[6]
	      fieldCERT = nextResults[7]
	      fieldOtherRef = nextResults[8][:-1]

	      print "          {"
	      print "            \"Id\": \"%d\"," % (countResults)
              print "            \"TaskId\": \"%s\"," % (formatCad(fieldTaskId))
              print "            \"TaskName\": \"%s\"," % (formatCad(fieldTaskName))
              print "            \"StartScan\": \"%s\"," % (formatCad(fieldStartScan))
              print "            \"ResultId\": \"%s\"," % (formatCad(fieldResultId))
              print "            \"Port\": \"%s\"," % (formatCad(fieldPort))
              print "            \"Protocol\": \"%s\"," % (formatCad(fieldProtocol))
	      print "            \"CVSS\": \"%s\"," % (formatCad(fieldCVSS))
	      print "            \"Severity\": \"%s\"," % (formatCad(fieldSeverity))
	      print "            \"NVTName\": \"%s\"," % (formatCad(fieldNVTName))
              print "            \"NVTOID\": \"%s\"," % (formatCad(fieldNVTOID))
	      print "            \"Summary\": \"%s\"," % (formatCad(fieldSummary))
	      print "            \"SpecificResult\": \"%s\"," % (formatCad(fieldSpecificResult))
              print "            \"Impact\": \"%s\"," % (formatCad(fieldImpact))
              print "            \"Solution\": \"%s\"," % (formatCad(fieldSolution))
              print "            \"AffectedSoftware\": \"%s\"," % (formatCad(fieldAffectedSoftware))
	      print "            \"VulnerabilityInsight\": \"%s\"," % (formatCad(fieldVulnerabilityInsight))
	      print "            \"DetectionMethod\": \"%s\"," % (formatCad(fieldDetectionMethod))
	      print "            \"ProductDetectionResult\": \"%s\"," % (formatCad(fieldProductDetectionResult))
	      print "            \"BID\": \"%s\"," % (formatCad(fieldBID))
              print "            \"CVE\": \"%s\"," % (formatCad(fieldCVE))
	      print "            \"CERT\": \"%s\"," % (formatCad(fieldCERT))
	      print "            \"OtherRef\": \"%s\"" % (formatCad(fieldOtherRef))
              print "          }%s" % (("",",") [ countResults < totalResults ])

	      countResults += 1

          print "      ]"

        else:
          print "      \"Server\": \"%s\"," % (formatCad(server))
          print "      \"IP\": \"\","
          print "      \"ScanId\": \"%s\"," % (scan)
          print "      \"CVSS\": \"0.0\","
          print "      \"Severity\": \"-----\","
          print "      \"TotalHigh\": \"0\","
          print "      \"TotalMedium\": \"0\","
          print "      \"TotalLow\": \"0\","
          print "      \"TotalLog\": \"0\","
          print "      \"TotalFalsePositive\": \"0\","
	  print "      \"Results\": ["
	  print "      ]"


    print "    },"


def show_cabecera():
    print "{"
    print "  \"ansible_facts\": {"


def show_pie():
    print "    \"changed\": false"
    print "  }"
    print "}" 


def main():

    global awk, bash, find, grep, sed
    awk = path('gawk','awk')
    bash = getShell()
    find = path('gfind','find')
    grep = path('ggrep','grep')
    sed = path('gsed','sed')

    global passwdAdmin
    passwdAdmin = "" 
    global server
    server = ""
    global scan
    scan = ""

    # read the argument string from the arguments file
    if len(sys.argv) > 1:
      args_file = sys.argv[1]
      args_data = file(args_file).read()

      arguments = shlex.split(args_data)

      for arg in arguments:

        if "=" in arg:

          (key, value) = arg.split("=", 1)

          if key == "passwd":
            passwdAdmin = value

          if key == "host":
            server = value

          if key == "scanID":
            scan = value


      if passwdAdmin == "" or server == "" or scan == "":

        print json.dumps({
          "failed" : True,
          "msg"    : "failed getting argument 'passwd' 'host' or 'scanID'"
        })
        sys.exit(1)

    else:
        print json.dumps({
          "failed" : True,
          "msg"    : "failed: no arguments"
        })
        sys.exit(1)

    
    show_cabecera()
    show_openvas()
    show_pie()



if __name__ == '__main__':
    main()

