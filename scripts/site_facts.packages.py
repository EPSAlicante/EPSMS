#!/usr/bin/python
# The source code packaged with this file is Free Software, Copyright (C) 2016 by
# Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: <epsms at eps.ua.es>.
# It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise.
# You can get copies of the licenses here: http://www.affero.org/oagpl.html
# AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".


import subprocess
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


def formatCad(cad):
    try:
      retCad = json.dumps(cad.replace("'","\"")).replace("\\u","\\\\u")[1:-1]

      return retCad

    except:
      return ""


def getPackageManager():
    # Getting Package Manager
    packageManager = subprocess.Popen("((%s --version >/dev/null && echo 'rpm') || (%s --version >/dev/null && echo 'conary') || (%s --version >/dev/null && echo 'dpkg') || (%s --version >/dev/null && echo 'emerge') || (%s --version >/dev/null && echo 'pacman') || (%s >/dev/null && echo 'pkgtools') || (%s >/dev/null && echo 'pkgutil') || (%s --version >/dev/null && echo 'zypper') || (%s >/dev/null && echo 'slackpkg') || (%s >/dev/null && echo 'installpkg') ||  echo 'unknown') 2>%s" % (path('rpm'), path('conary'), path('dpkg-query'), path('equery'), path('pacman'), path('pkg_info'), path('pkgutil'), path('zypper'), path('slackpkg'), path('installpkg'), errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    return packageManager


def show_packages(type):

    if type == 'rpm':
      command = "%s -qa --queryformat '%%{name} %%{version}-%%{release}.%%{arch} %%{size}\n'|sort" % (path('rpm'))

    elif type == 'conary':
      command = "%s query -i|%s -e '^Name' -e '^Version' -e '^Size'|tr '\n' ' '|%s 's/Name/\\nName/g'|%s 's/^Name//g'|%s 's/Build.*Version//g'|%s 's/Label.*Size//g'|tr '\t' ' '|tr -d ' '|%s 's/^://g'|tr ':' ' '|%s -v '^$'" % (path('conary'), grep, sed, sed, sed, sed, sed, grep)

    elif type == 'dpkg':
      command = "%s -W --showformat='${Package} ${Version}.${Architecture} ${Installed-Size}\n'|sort" % (path('dpkg-query'))

    elif type == 'emerge':
      command = "%s list '*' --format='$name $fullversion'|sort" % (path('equery'))

    elif type == 'installpkg' or type == 'slackpkg':
      command = "ls -1 /var/log/packages|rev|sed 's/-/ /3'|rev"

    elif type == 'pacman':
      command = "%s -Q|uniq|sort" % (path('pacman'))

    elif type == 'pkgtools':
      command = "%s -as|%s -v '^$' |%s -iv '^Package'|%s -iv '^Total size'|%s 'BEGIN {RS=\"\"}{gsub(/:\\n/,\" \",$0); print $0}'|tr '\t' ' '|tr -s ' '|cut -d' ' -f3,4|rev|%s 's/-/ /'|rev|%s 's/^.*://'|%s -v '^$'" % (path('pkg_info'), grep, grep, grep, awk, sed, sed, grep)

    elif type == 'pkgutil':
      command = "%s -A|tr -s ' '|%s -v '^$'|%s -iv '^Package'|%s -iv 'not installed'|cut -d',' -f1|sort" % (path('pkgutil'), grep, grep, grep)

    elif type == 'zypper':
      command = "%s search -iv -t package|tr '\t' ' '|tr -s ' '|%s -e ' name:' -e ' evr:' -e ' installsize:' -e ' arch:'|tr '\n' ' '|%s 's/ name:/ \nname:/g'|tr -s ' '|%s 's/name: //g'|%s 's/ arch: / /g'|%s 's/ evr: / /g'|%s 's/ installsize: / /g'|%s '{ print $1 \" \" $2 \".\" $3 \" \" $4 }'|uniq|sort" % (path('zypper'), grep, sed, sed, sed, sed, sed, awk)

    else:
      command = "echo >/dev/null" 

    print "    \"packages\": ["
    cont = 1
    packages = subprocess.Popen("(%s) 2>%s" % (command, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)

    packagesLines = packages.stdout.readlines()
    maxPackages = len(packagesLines)

    for line in packagesLines:
      data=line.split()
      name = data[0]
      version = data[1]

      if len(data) == 3:
	try:
          size = str(int(data[2]))
  	except:
	  size = "0"
      else:
        size = "0"

      if type == 'dpkg':
	try:
          size = str(int(size)*1024)
	except:
	  size = "0"

      print "      {"
      print "        \"name\": \"%s\"," % (formatCad(name))
      print "        \"version\": \"%s\"," % (formatCad(version))
      print "        \"size\": \"%s\"" % (formatCad(size))
      if cont < maxPackages: 
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

    # Looking for commands path
    global awk, bash, grep, find, sed
    awk = path('gawk','awk')
    bash = getShell()
    grep = path('ggrep','grep')
    find = path('gfind','find')
    sed = path('gsed','sed')

    show_packages(getPackageManager())

    show_pie()



if __name__ == '__main__':
    main()

