#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".

import subprocess
import sys
import os
import shutil
import datetime


# Configuration Files
pathAnsible = "/etc/ansible"
pathCentosVersion = "/etc/centos-release"
fileTGZ = "ansible.tgz"


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
      sys.exit(1)
    else: 
      print "Python %s detected (OK)" % str(sys.version_info)

    print
    # Check Linux distribution and Version (Debian Squeeze or Centos 6 needed)
    print "Checking SO version..." 
    if os.access(pathCentosVersion, os.R_OK):
      cadVersion = subprocess.Popen("cat %s" % (pathCentosVersion), shell=True, stdout=subprocess.PIPE)
      version = cadVersion.stdout.read().split(' ')[2]
      if version.split('.')[0] != "6":
        print >> sys.stderr, ""
	print >> sys.stderr, "CentOS %s detected (ERROR). CentOS 6 required" % version
        sys.exit(2)
      else:
        print "CentOS %s detected (OK)" % version
    else:
      pritn >> sys.stderr, ""
      print >> sys.stderr, "CentOS 6 required"
      sys.exit(2)

    print
    # Installing ansible
    print "Installing Ansible and dependencies"
    retCode = subprocess.call("yum -y --enablerepo=epel install ansible sshpass", shell=True)
    if retCode == 0:
      # Looking for '/etc/ansible' directory
      if os.access(pathAnsible, os.R_OK): 
 	print
	print "%s directory detected" % pathAnsible
 	try:
	  shutil.move(pathAnsible, "%s-%s" % (pathAnsible,datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
	  print "Moving %s to %s-%s" % (pathAnsible,pathAnsible,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
	  try:
	    os.mkdir(pathAnsible)
	    print "Creating %s directory" % pathAnsible
	    print
	    pathTGZ = os.path.dirname(os.path.realpath(__file__))
	    if os.access("%s/%s" % (pathTGZ,fileTGZ), os.R_OK): 	
	      print "Unzipping %s/%s..." % (pathTGZ,fileTGZ) 
	      retCode = subprocess.call("cd %s && tar xvpzf %s/%s" % (pathAnsible,pathTGZ,fileTGZ), shell=True)
	      if retCode == 0:
		print
		print "Installed!!!"
		print
		print "Control Menu: /etc/ansible/menu.py"
		print
	      else:
                print >> sys.stderr, ""
                print >> sys.stderr, "Error unzipping %s/%s in %s" % (pathTGZ,fileTGZ,pathAnsible)
		sys.exit(8)
	    else:
              print >> sys.stderr, ""
              print >> sys.stderr, "Error, file %s/%s not found" % (pathTGZ,fileTGZ) 
	      sys.exit(7)
	  except:
            print >> sys.stderr, ""
            print >> sys.stderr, "Error creating %s directory" % (pathAnsible)
	    sys.exit(6)
        except:
	  print >> sys.stderr, ""
	  print >> sys.stderr, "Error moving %s directory to %s-%s" % (pathAnsible,pathAnsible,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
	  sys.exit(5)
      else:
	print >> sys.stderr, ""
	print >> sys.stderr, "'/etc/ansible' directory not found"
        sys.exit(4)
    else:
      print >> sys.stderr, ""
      print >> sys.stderr, "Error installing Ansible and dependencies"
      sys.exit(3)

    sys.exit(0)    





if __name__ == '__main__':
    main()


