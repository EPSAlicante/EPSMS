#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
import sys
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
      retCad = json.dumps(cad.replace("'","\"")).replace("\\u","\\\\u")[1:-1]

      return retCad

    except:
      return ""


def typeOS():
    retOS = subprocess.Popen("uname -s 2>%s" % (errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
    return retOS.stdout.read().strip()


def getPackageManager():
    # Getting Package Manager
    packageManager = subprocess.Popen("((%s --version >/dev/null && echo 'rpm') || (%s --version >/dev/null && echo 'conary') || (%s --version >/dev/null && echo 'dpkg') || (%s --version >/dev/null && echo 'emerge') || (%s --version >/dev/null && echo 'pacman') || (%s >/dev/null && echo %s'-pkgtools') || (%s >/dev/null && echo 'pkgutil') || (%s --version >/dev/null && echo 'zypper') || (%s >/dev/null && echo 'slackpkg') || (%s >/dev/null && echo 'installpkg') ||  echo 'unknown') 2>%s" % (path('rpm'), path('conary'), path('dpkg'), path('equery'), path('pacman'), path('pkg_info'), typeOS(), path('pkgutil'), path('zypper'), path('slackpkg'), path('installpkg'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    return packageManager


def show_exes(type,dirExes,dirNoExes):

    paramExes = dirExes
    paramNoExes = ""
    if dirNoExes != "":
      listNoExes = dirNoExes.split(' ')

      countNoExes = 0
      for dir in listNoExes:
        if countNoExes == 0: 
	  paramNoExes += " \( -path '%s'" % (dir)
        else:
      	  paramNoExes += " -o -path '%s'" % (dir)

        countNoExes += 1

      paramNoExes += " \) -prune"


    print "    \"exes\": ["

    # If there are paths 
    if paramExes != "":
      cont = 1
      command = "%s %s -ignore_readdir_race -type d %s -o -type f \( -perm -u+x -o -perm -g+x -o -perm -o+x \) -ls|%s '{print $5,$6,$3,$7,substr($0,index($0,$11))}'" % (find, paramExes, paramNoExes, awk)
      exes = subprocess.Popen("(%s) 2>%s" % (command, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

      exesLines = exes.stdout.readlines()
      maxExes = len(exesLines) 

      for line in exesLines:
        exeUser = line.split(' ')[0]
        exeGroup = line.split(' ')[1]
        exePerms = line.split(' ')[2]
        exeSize = line.split(' ')[3]
        exeName = line.split(' ',4)[4].strip() 
        if type == 'rpm':
          package = subprocess.Popen("([ -r \"%s\" ] && %s -qf \"%s\") 2>%s" % (exeName, path('rpm'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'conary':
	  package = subprocess.Popen("([ -r \"%s\" ] && %s query --path \"%s\"|cut -d':' -f1) 2>%s" % (exeName, path('conary'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'dpkg':
          package = subprocess.Popen("([ -r \"%s\" ] && %s -S \"%s\"|cut -d':' -f1) 2>%s" % (exeName, path('dpkg'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'emerge':
	  package = subprocess.Popen("([ -r \"%s\" ] && %s -q belongs -e \"%s\"|cut -d'/' -f2) 2>%s" % (exeName, path('equery'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'installpkg' or type == 'slackpkg':
	  package = subprocess.Popen("([ -r \"%s\" ] && [ -d \"/var/log/packages\" ] && %s -l \"`echo \"%s\"|cut -c2-`\" /var/log/packages/*|%s 's@/var/log/packages/@@') 2>%s" % (exeName, grep, exeName, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'pacman':
	  package = subprocess.Popen("([ -r \"%s\" ] && %s -Qoq \"%s\") 2>%s" % (exeName, path('pacman'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'FreeBSD-pkgtools':
	  package = subprocess.Popen("([ -r \"%s\" ] && %s -W \"%s\"|%s 's/.* package //g') 2>%s" % (exeName, path('pkg_info'), exeName, sed, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'OpenBSD-pkgtools':
          package = subprocess.Popen("([ -r \"%s\" ] && %s -E \"%s\"|cut -d' ' -f1) 2>%s" % (exeName, path('pkg_info'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'pkgutil':
          package = subprocess.Popen("([ -r \"%s\" ] && %s -F \"%s\"|head -1|gawk '{print $2}') 2>%s" % (exeName, path('pkgutil'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        elif type == 'zypper':
	  package = subprocess.Popen("([ -r \"%s\" ] && %s what-provides \"%s\"|%s '^i '|cut -d'|' -f2|tr -d ' ') 2>%s" % (exeName, path('zypper'), exeName, grep, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        else:
	  package = subprocess.Popen("(echo '') 2>%s" % (errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE) 

        package.wait()
        if package.returncode == 0:
	  packageName = package.stdout.read().strip().replace("\n"," ")
        else:
          packageName = ""

        # Signature
        if typeOS().endswith('BSD'):
	  signature = subprocess.Popen("[ -r \"%s\" ] && (%s \"%s\"|cut -d'=' -f2|tr -d ' ') 2>%s" % (exeName, path('md5','md5sum'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        else:
	  signature = subprocess.Popen("[ -r \"%s\" ] && (%s \"%s\"|cut -d' ' -f1) 2>%s" % (exeName, path('md5','md5sum'), exeName, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

        signatureCode = signature.stdout.read().strip()

        print "      {"
        print "        \"name\": \"%s\"," % (formatCad(exeName))
        print "        \"package\": \"%s\"," % (formatCad(packageName))
        print "        \"size\": \"%s\"," % (formatCad(exeSize))
        print "        \"user\": \"%s\"," % (formatCad(exeUser))
        print "        \"group\": \"%s\"," % (formatCad(exeGroup))
        print "        \"perms\": \"%s\"," % (formatCad(exePerms))
        print "        \"signature\": \"%s\"" % (formatCad(signatureCode))
        if cont < maxExes: 
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

    # Optional arguments
    pathExes = ""
    pathNoExes = ""

    # read the argument string from the arguments file
    if len(sys.argv) > 1:

      args_file = sys.argv[1]
      args_data = file(args_file).read()

      arguments = shlex.split(args_data)

      for arg in arguments:

        if "=" in arg:

          (key, value) = arg.split("=", 1)

          if key == "pathExes":
            pathExes = value
            if pathExes.startswith("'"):
              pathExes = pathExes[1:]
              if pathExes.endswith("'"):
                pathExes = pathExes[:-1]

          if key == "pathNoExes":
            pathNoExes = value
            if pathNoExes.startswith("'"):
              pathNoExes = pathNoExes[1:]
              if pathNoExes.endswith("'"):
                pathNoExes = pathNoExes[:-1]


      if pathExes:

        show_cabecera()

        # Looking for commands path
        global awk, bash, find, grep, sed
        awk = path('gawk','awk')
        bash = getShell()
        find = path('gfind','find')
        grep = path('ggrep','grep')
        sed = path('gsed','sed')

        show_exes(getPackageManager(),pathExes,pathNoExes)
        show_pie()

      else:
        print json.dumps({
          "failed" : True,
          "msg"    : "failed getting argument 'pathExes'"
        })
        sys.exit(1)

    else:
      print json.dumps({
        "failed" : True,
        "msg"    : "failed: no arguments"
      })
      sys.exit(1)




if __name__ == '__main__':
    main()

