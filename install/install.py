#!/usr/bin/python

import subprocess
import sys
import os
import platform
import shutil
import datetime


# Configuration Files
pathAnsible = "/etc/ansible"
pathCentosVersion = "/etc/centos-release"
pathAnsibleLibrary = "/usr/share/ansible"
pathAnsibleLogs = "/var/log/ansible"
fileAnsibleCFG = "%s/ansible.cfg" % (pathAnsible)
findModArgs = "/usr/lib/python2.?/site-packages/ansible/parsing/mod_args.py"
findFactsLib = "/usr/lib/python2.?/site-packages/ansible/module_utils/facts.py"
fileTGZ = "ansible.tgz"
versionAnsible = "ansible-2.3.2.0"
yumConf = "/etc/yum.conf"


def main():

    # Clear screen
    os.system("clear")
    # System Installation
    print
    print "Installation of EPS Monitoring System"
    print

    # Check Python Version
    print "Checking Python version..."
    if sys.version_info < (2, 6) or sys.version_info > (3, 0):
      print >> sys.stderr, "Python %s detected (ERROR). Python 2.6 required or greater (not 3.X)" % str(sys.version_info)
      print >> sys.stderr, "Read INSTALL help"
      print >> sys.stderr, ""
      sys.exit(1)
    else: 
      print "Python %s detected (OK)" % str(sys.version_info)

    print
    # Check Linux distribution and Version (Centos 6 required)
    print "Checking SO version..." 
    if os.access(pathCentosVersion, os.R_OK):
      cadVersion = subprocess.Popen("cat %s" % (pathCentosVersion), shell=True, stdout=subprocess.PIPE)
      version = cadVersion.stdout.read().split(' ')[2]
      if version.split('.')[0] != "6":
	print >> sys.stderr, "CentOS %s detected (ERROR). CentOS 6 required" % version
	print >> sys.stderr, "Read INSTALL help"
	print >> sys.stderr, ""
        sys.exit(2)
      else:
        print "CentOS %s detected (OK)" % version
    else:
      print >> sys.stderr, "CentOS 6 required"
      print >> sys.stderr, "Read INSTALL help"
      print >> sys.stderr, ""
      sys.exit(3)

    print
    # Check Linux Architecture (64 bits required)
    print "Checking Architecture..."
    arch = platform.architecture()[0]
    if arch != "64bit":
      print >> sys.stderr, "Architecture %s detected (ERROR). 64bit required" % arch 
      print >> sys.stderr, "Read INSTALL help"
      print >> sys.stderr, ""
      sys.exit(4)
    else:
      print "Architecture %s detected (OK)" % arch 

    print
    # Check LANG environment variable (UTF-8 required) 
    print "Checking LANG environment variable (UTF-8 required)..."
    cadLANG = subprocess.Popen("grep '^LANG' /etc/sysconfig/i18n|cut -d'=' -f2", shell=True, stdout=subprocess.PIPE)
    lang = cadLANG.stdout.read().strip().strip('"')
    if "UTF-8" in lang:
        print "LANG (%s) detected (OK)" % lang
    else:
        print >> sys.stderr, "LANG (%s) detected (ERROR). UTF-8 required" % lang
	print >> sys.stderr, "Read INSTALL help"
	print >> sys.stderr, ""
        sys.exit(5)

    print
    # Check Ansible package (EPEL repository enabled)
    print "Checking Ansible package (EPEL repository has to be enabled)..."
    cadAnsible = subprocess.Popen("yum list ansible 2>/dev/null|grep '^ansible'|tr -s ' '", shell=True, stdout=subprocess.PIPE)
    ansible = cadAnsible.stdout.read().strip()
    if "ansible" in ansible:
	print "Ansible package (%s) detected (OK)" % ansible
    else:
        print >> sys.stderr, "Ansible package not found (ERROR). EPEL repository enabled is required"
	print >> sys.stderr, "Read INSTALL help"
	print >> sys.stderr, ""
        sys.exit(6)

    print

    # Updating CentOS
    print "Updating CentOS"
    retCode = subprocess.call("yum -y update", shell=True)
    if retCode != 0:
      print >> sys.stderr, ""
      print >> sys.stderr, "Error updating CentOS" 
      sys.exit(7)
      
    # Installing ansible
    print
    print "Installing %s" % (versionAnsible)
    ret1Code = subprocess.call("yum -y install %s" % (versionAnsible), shell=True)

    if ret1Code == 0:
      print
      print "Installing required tools"
      ret2Code = subprocess.call("yum -y install sshpass python-pip libselinux-python", shell=True)

    if ret1Code == 0 and ret2Code == 0:
      # Avoid ansible update (exclude from yum)
      print
      print "Excluding ansible from %s to avoid updates" % (yumConf)
      ret3Code = subprocess.call("(grep '^exclude=' %s && sed -i 's/^exclude=/exclude=ansible* /g' %s) || echo 'exclude=ansible*' >> %s" % (yumConf,yumConf,yumConf), shell=True)
      if ret3Code != 0:
	print
	print "Ansible not excluded from %s. To avoid ansibles software updates (keeping stability), you should add 'exclude=ansible*' in %s file" % (yumConf,yumConf)
	print

      # Looking for '/etc/ansible' directory
      if os.access(pathAnsible, os.R_OK): 
 	print
	print "%s directory detected" % pathAnsible
 	try:
	  shutil.move(pathAnsible, "%s-%s" % (pathAnsible,datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
	  print "Moving %s to %s-%s" % (pathAnsible,pathAnsible,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

        except:
          print >> sys.stderr, ""
          print >> sys.stderr, "Error moving %s directory to %s-%s" % (pathAnsible,pathAnsible,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
          sys.exit(8)

      try:
	os.mkdir(pathAnsible)
	print "Creating %s directory" % pathAnsible
	print
	pathTGZ = os.path.dirname(os.path.realpath(__file__))

      except:
        print >> sys.stderr, ""
        print >> sys.stderr, "Error creating %s directory" % (pathAnsible)
        sys.exit(9)


      try:

	if os.access("%s/%s" % (pathTGZ,fileTGZ), os.R_OK): 	
	  print "Unzipping %s/%s..." % (pathTGZ,fileTGZ) 
	  retCode = subprocess.call("cd %s && tar xpzf %s/%s" % (pathAnsible,pathTGZ,fileTGZ), shell=True)
	  if retCode == 0:
	    print
    	    print "Ansible installed."

	    print
	    print "Configuring Ansible..."

	    # Create pathAnsibleLibrary directory
	    if not os.path.exists(pathAnsibleLibrary):
    	      os.makedirs(pathAnsibleLibrary)
	      print
	      print "%s directory created" % (pathAnsibleLibrary)

	    # Create Logs Ansible directory
            if not os.path.exists(pathAnsibleLogs):
              os.makedirs(pathAnsibleLogs)
              print
              print "%s directory created" % (pathAnsibleLogs)

	    # Set scp_if_ssh = True in fileAnsibleCFG 
	    retCode = subprocess.call("(grep '^scp_if_ssh' %s && (grep '^scp_if_ssh' %s|grep -i true || (sed -i 's/scp_if_ssh/#scp_if_ssh/' %s && false)) || sed -i 's/\[ssh_connection\]/\[ssh_connection\]\\nscp_if_ssh = True/' %s) > /dev/null" % (fileAnsibleCFG,fileAnsibleCFG,fileAnsibleCFG,fileAnsibleCFG), shell=True)	
	    print
	    print "'scp_if_ssh = True' verified in %s" % (fileAnsibleCFG)

            # Set force_color = 1 in fileAnsibleCFG
            retCode = subprocess.call("(grep '^force_color' %s && (grep '^force_color' %s|grep -i '1' || (sed -i 's/force_color/#force_color/' %s && false)) || sed -i 's/\[defaults\]/\[defaults\]\\nforce_color = 1/' %s) > /dev/null" % (fileAnsibleCFG,fileAnsibleCFG,fileAnsibleCFG,fileAnsibleCFG), shell=True)
            print
            print "'force_color = 1' verified in %s" % (fileAnsibleCFG)

	    # Add db_facts in mod_args.py 
	    fileModArgs = subprocess.Popen("find %s|head -1" % (findModArgs), shell=True, stdout=subprocess.PIPE).stdout.read().strip()
	    if fileModArgs != "":
	      retCode = subprocess.call("(grep 'db_facts' %s || sed -i \"s/RAW_PARAM_MODULES = (\[/RAW_PARAM_MODULES = (\[\\n    'db_facts',/\" %s) > /dev/null" % (fileModArgs,fileModArgs), shell=True)
	      print
	      print "'db_facts' added in %s" % (fileModArgs)
	    else:
	      print "mod_args.py file not found"

            # Fix error uptime_seconds for Solaris in facts.py 
 	    fileFactsLib = subprocess.Popen("find %s|head -1" % (findFactsLib), shell=True, stdout=subprocess.PIPE).stdout.read().strip()
	    if fileFactsLib != "":
	      retCode = subprocess.call("(grep \"self\.facts\['uptime_seconds'\] = int(float(out\.split('\\\\t')\[1\]\.split(',')\[0\]))\" %s || sed -i \"s/self\.facts\['uptime_seconds'\] = int(float(out\.split('\\\\t')\[1\]))/self\.facts\['uptime_seconds'\] = int(float(out\.split('\\t')\[1\]\.split(',')\[0\]))/\" %s) > /dev/null" % (fileFactsLib,fileFactsLib), shell=True)
              print
              print "Modified %s" % (fileModArgs)
            else:
              print "facts.py file not found"

	    # Install html2text python library
	    print
	    retCode = subprocess.call("pip install html2text 2> /dev/null", shell=True)
	    print
	    print "html2text python library installed"

	    print
	    print "Ansible configured."
	    print
	    print "-------------------------------------------------------------------"
	    print
	    print "Control Menu: /etc/ansible/menu.py (select option '1' to configure)"
	    print
	    print "-------------------------------------------------------------------"

	  else:
            print >> sys.stderr, ""
            print >> sys.stderr, "Error unzipping %s/%s in %s" % (pathTGZ,fileTGZ,pathAnsible)
	    sys.exit(10)

        else:
          print >> sys.stderr, ""
          print >> sys.stderr, "Error, file %s/%s not found" % (pathTGZ,fileTGZ) 
	  sys.exit(11)

      except Exception as e:
        print >> sys.stderr, ""
        print >> sys.stderr, "Error Configuring Ansible: %s" % (e) 
        sys.exit(12)

    else:
      print >> sys.stderr, ""
      print >> sys.stderr, "Error installing ansible and dependencies"
      sys.exit(13)

    sys.exit(0)    





if __name__ == '__main__':
    main()

