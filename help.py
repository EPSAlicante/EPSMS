#!/usr/bin/python

import subprocess
import sys
import os
import readline


# Configuration Files
pathAnsible = "/etc/ansible"
pathHelpMenu = "%s/help/MENU" % (pathAnsible)
pathHelpDescription = "%s/help/DESCRIPTION" % (pathAnsible)
pathHelpConfigure = "%s/help/CONFIGURE" % (pathAnsible)
pathHelpConfigExtra = "%s/help/CONFIGEXTRA" % (pathAnsible)
pathHelpStructure = "%s/help/STRUCTURE" % (pathAnsible)
pathHelpFAQ = "%s/help/FAQ" % (pathAnsible)
pathHelpExample = "%s/help/EXAMPLE" % (pathAnsible)


def printMenu():

    print "################## HELP MENU ####################"
    print "##                                             ##"
    print "##  1. Control Menu                            ##"
    print "##  2. System Description                      ##"
    print "##  3. Configuration                           ##"
    print "##  4. Extra Variables Configuration           ##"
    print "##  5. Structure                               ##"
    print "##  6. FAQ                                     ##"
    print "##  7. Example                                 ##"
    print "##  q. Quit Menu                               ##"
    print "##                                             ##"
    print "##  Type 'q' to end watching doc files         ##"
    print "##                                             ##"
    print "#################################################"


def selectOption():

    answer = None
    legal_answers = ['1','2','3','4','5','6','7','q']
    tried = False
    while answer not in legal_answers:
        print "%s" % "Invalid input, select again" if tried else ""
        answer = raw_input('Select option: ')
        tried = True

    return answer


def execOption(opt):

    if opt == '1':
      ## Read Control Menu Help ##
      if os.access(pathHelpMenu, os.R_OK):
	retCode = subprocess.call("less %s" % (pathHelpMenu), shell=True)
	print
      else:
	print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpMenu)
	print >> sys.stderr

    elif opt == '2':
      ## Read System Description Help ##
      if os.access(pathHelpDescription, os.R_OK):
        retCode = subprocess.call("less %s" % (pathHelpDescription), shell=True)
        print
      else:
        print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpDescription)
        print >> sys.stderr

    elif opt == '3':
      ## Read Configuration Help ##
      if os.access(pathHelpConfigure, os.R_OK):
        retCode = subprocess.call("less %s" % (pathHelpConfigure), shell=True)
        print
      else:
        print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpConfigure)
        print >> sys.stderr

    elif opt == '4':
      ## Read Extra Variables Configuration Help ##
      if os.access(pathHelpConfigExtra, os.R_OK):
        retCode = subprocess.call("less %s" % (pathHelpConfigExtra), shell=True)
        print
      else:
        print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpConfigExtra)
        print >> sys.stderr

    elif opt == '5':
      ## Read Structure Help ##
      if os.access(pathHelpStructure, os.R_OK):
        retCode = subprocess.call("less %s" % (pathHelpStructure), shell=True)
        print
      else:
        print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpStructure)
        print >> sys.stderr

    elif opt == '6':
      ## Read FAQ Help ##
      if os.access(pathHelpFAQ, os.R_OK):
        retCode = subprocess.call("less %s" % (pathHelpFAQ), shell=True)
        print
      else:
        print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpFAQ)
        print >> sys.stderr

    elif opt == '7':
      ## Read Example Help ##
      if os.access(pathHelpExample, os.R_OK):
        retCode = subprocess.call("less %s" % (pathHelpExample), shell=True)
        print
      else:
        print >> sys.stderr, "File %s don't exist or not readable" % (pathHelpExample)
        print >> sys.stderr

    else:
      print "Option %s not valid" % (opt)



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
    sys.exit(0)



if __name__ == '__main__':
	    main()

