#!/usr/bin/python

import subprocess
import socket
import datetime
import os
import sys
import re
import shlex
try:
  import json
except ImportError:
  import simplejson as json


# Configuration Files
pathAnsible = "/etc/ansible"
configAll = "%s/group_vars/all" % (pathAnsible) 


bash = "/bin/sh"

# Error Log file ('/dev/null' by default)
errorLog = "/dev/null"



def getValueFromFile(file, label, separator):
    value = ""
    if os.access(file, os.R_OK):
      f = open(file, "r")
      for line in f:
        if line.startswith(label+':'):
          value = line.split(separator,1)[1].strip() 

    return value


def winCheck():

    check = ""
    # Get global value
    check = getValueFromFile(configAll, "winNodes", ":") 

    return check


def winUser():

    user = ""
    # Get global value
    user = getValueFromFile(configAll, "winUserNodes", ":")

    return  user


def winPasswd():
    passwd = ""
    # Get global value
    passwd = getValueFromFile(configAll, "winPasswdNodes", ":")

    return passwd


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
      if isinstance(cad,basestring):
	retCad = cad.replace("\\","\\\\\\\\").replace("\"","\\\"").replace("'","\\\"").replace("\(","\\(").replace("\)","\\)").replace("\[","\\[").replace("\]","\\]").replace("\{","\\{").replace("\}","\\}").replace("\t"," ")
      else:
	retCad = cad

      # Replace non-ascii chars with ? 
      retStr = ''.join([i if ord(i) < 128 else '?' for i in retCad])

      try:
        return str(retStr)
      except:
	return unicode(retStr,'utf-8')

    except:
        return ""


def getDomainRole(code):

    arrayRoles = [ 'Standalone Workstation', 'Member Workstation', 'Standalone Server', 'Member Server', 'Backup Domain Controller', 'Primary Domain Controller']
    try:
      retValue = arrayRoles[int(code)]
    except:
      retValue = "%s (Role Code)" % (code) if code.strip() != "" else ""

    return retValue


def getPCSystemType(code):

    arrayTypes = [ 'Unspecified', 'Desktop', 'Mobile', 'Workstation', 'Enterprise Server', 'Small Office and Home Office (SOHO) Server', 'Appliance PC', 'Performance Server', 'Maximum']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getWakeUpType(code):

    arrayTypes = [ 'Reserved', 'Other', 'Unknown', 'APM Timer', 'Modem Ring', 'LAN Remote', 'Power Switch', 'PCI PME#', 'AC Power Restored']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getOSType(code):

    arrayTypes = [ 'Unknown', 'Other', 'MACROS', 'ATTUNIX', 'DGUX', 'DECNT', 'Digital Unix', 'OpenVMS', 'HPUX', 'AIX', 'MVS', 'OS400', 'OS/2', 'JavaVM', 'MSDOS', 'WIN3X', 'WIN95', 'WIN98', 'WINNT', 'WINCE', 'NCR3000', 'NetWare', 'OSF', 'DC/OS', 'Reliant UNIX', 'SCO UnixWare', 'SCO OpenServer', 'Sequent', 'IRIX', 'Solaris', 'SunOS', 'U6000', 'ASERIES', 'TandemNSK', 'TandemNT', 'BS2000', 'LINUX', 'Lynx', 'XENIX', 'VM/ESA', 'Interactive UNIX', 'BSDUNIX', 'FreeBSD', 'NetBSD', 'GNU Hurd', 'OS9', 'MACH Kernel', 'Inferno', 'QNX', 'EPOC', 'IxWorks', 'VxWorks', 'MiNT', 'BeOS', 'HP MPE', 'NextStep', 'PalmPilot', 'Rhapsody']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getProductType(code):

    arrayTypes = [ '', 'Work Station', 'Domain Controller', 'Server']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getCountryCode(code):

    arrayCountries = {'1':'United States', '7':'Russia',  '20':'Egypt', '27':'South Africa', '30':'Greece', '31':'Netherlands', '32':'Belgium', '33':'France', '34':'Spain', '36':'Hungary', '39':'Italy', '41':'Switzerland', '40':'Romania', '43':'Austria', '44':'United Kingdom', '45':'Denmark', '46':'Sweden', '47':'Norway', '48':'Poland', '49':'Germany', '51':'Peru', '52':'Mexico', '53':'Cuba', '54':'Argentina', '55':'Brazil', '56':'Chile', '57':'Colombia', '58':'Venezuela', '60':'Malaysia', '61':'Australia', '62':'Indonesia', '63':'Philippines', '64':'New Zealand', '65':'Singapore', '66':'Thailand', '81':'Japan', '82':'South Korea', '84':'Vietnam', '86':'China', '90':'Turkey', '91':'India', '92':'Pakistan', '94':'Sri Lanka', '98':'Iran', '212':'Morocco', '216':'Tunisia', '218':'Libya', '261':'Madagascar', '298':'Faroe Islands', '299':'Greenland', '350':'Gibraltar', '351':'Portugal', '352':'Luxembourg', '353':'Ireland', '354':'Iceland', '355':'Albania', '356':'Malta', '357':'Cyprus', '358':'Finland', '359':'Bulgaria', '370':'Lithuania', '371':'Latvia', '372':'Estonia', '373':'Moldova', '376':'Andorra', '377':'Monaco', '378':'San Marino', '379':'Vatican', '380':'Ukraine', '381':'Serbia', '382':'Montenegro', '383':'Kosovo', '385':'Croatia', '386':'Slovenia', '387':'Bosnia and Herzegovina', '389':'Macedonia', '420':'Czech Republic', '421':'Slovakia', '423':'Liechtenstein', '502':'Guatemala', '503':'El Salvador', '504':'Honduras', '505':'Nicaragua', '506':'Costa Rica', '507':'Panama', '509':'Haiti', '591':'Bolivia', '593':'Ecuador', '595':'Paraguay', '598':'Uruguay', '850':'North Korea', '852':'Hong Kong', '1-876':'Jamaica', '886':'Taiwan', '960':'Maldives', '961':'Lebanon', '963':'Syria', '964':'Iraq', '965':'Kuwait', '966':'Saudi Arabia', '970':'Palestine', '971':'United Arab Emirates', '972':'Israel', '974':'Qatar', '976':'Mongolia', '977':'Nepal', '992':'Tajikistan', '993':'Turkmenistan', '994':'Azerbaijan', '995':'Georgia', '996':'Kyrgyzstan', '998':'Uzbekistan'}
    try:
      if arrayCountries.has_key(code):
        retValue = arrayCountries[code]
      else:
        retValue = "%s (Country Code)" % (code) if code.strip() != "" else ""

    except:
      retValue = "%s (Country Code)" % (code) if code.strip() != "" else ""

    return retValue


def getOSLanguage(code):

    arrayLanguages = {'1':'Arabic', '4':'Chinese (Simplified)- China', '9':'English', '1025':'Arabic - Saudi Arabia', '1026':'Bulgarian', '1027':'Catalan', '1028':'Chinese (Traditional) - Taiwan', '1029':'Czech', '1030':'Danish', '1031':'German - Germany', '1032':'Greek', '1033':'English - United States', '1034':'Spanish - Traditional Sort', '1035':'Finnish', '1036':'French - France', '1037':'Hebrew', '1038':'Hungarian', '1039':'Icelandic', '1040':'Italian - Italy', '1041':'Japanese', '1042':'Korean', '1043':'Dutch - Netherlands', '1044':'Norwegian - Bokmal', '1045':'Polish', '1046':'Portuguese - Brazil', '1047':'Rhaeto-Romanic', '1048':'Romanian', '1049':'Russian', '1050':'Croatian', '1051':'Slovak', '1052':'Albanian', '1053':'Swedish', '1054':'Thai', '1055':'Turkish', '1056':'Urdu', '1057':'Indonesian', '1058':'Ukrainian', '1059':'Belarusian', '1060':'Slovenian', '1061':'Estonian', '1062':'Latvian', '1063':'Lithuanian', '1065':'Persian', '1066':'Vietnamese', '1069':'Basque (Basque)', '1070':'Serbian', '1071':'Macedonian (Macedonia (FYROM))', '1072':'Sutu', '1073':'Tsonga', '1074':'Tswana', '1076':'Xhosa', '1077':'Zulu', '1078':'Afrikaans', '1080':'Faeroese', '1081':'Hindi', '1082':'Maltese', '1084':'Scottish Gaelic (United Kingdom)', '1085':'Yiddish', '1086':'Malay - Malaysia', '2049':'Arabic - Iraq', '2052':'Chinese (Simplified) - PRC', '2055':'German - Switzerland', '2057':'English - United Kingdom', '2058':'Spanish - Mexico', '2060':'French - Belgium', '2064':'Italian - Switzerland', '2067':'Dutch - Belgium', '2068':'Norwegian - Nynorsk', '2070':'Portuguese - Portugal', '2072':'Romanian - Moldova', '2073':'Russian - Moldova', '2074':'Serbian - Latin', '2077':'Swedish - Finland', '3073':'Arabic - Egypt', '3076':'Chinese (Traditional) - Hong Kong SAR', '3079':'German - Austria', '3081':'English - Australia', '3082':'Spanish - International Sort', '3084':'French - Canada', '3098':'Serbian - Cyrillic', '4097':'Arabic - Libya', '4100':'Chinese (Simplified) - Singapore', '4103':'German - Luxembourg', '4105':'English - Canada', '4106':'Spanish - Guatemala', '4108':'French - Switzerland', '5121':'Arabic - Algeria', '5127':'German - Liechtenstein', '5129':'English - New Zealand', '5130':'Spanish - Costa Rica', '5132':'French - Luxembourg', '6145':'Arabic - Morocco', '6153':'English - Ireland', '6154':'Spanish - Panama', '7169':'Arabic - Tunisia', '7177':'English - South Africa', '7178':'Spanish - Dominican Republic', '8193':'Arabic - Oman', '8201':'English - Jamaica', '8202':'Spanish - Venezuela', '9217':'Arabic - Yemen', '9226':'Spanish - Colombia', '10241':'Arabic - Syria', '10249':'English - Belize', '10250':'Spanish - Peru', '11265':'Arabic - Jordan', '11273':'English - Trinidad', '11274':'Spanish - Argentina', '12289':'Arabic - Lebanon', '12298':'Spanish - Ecuador', '13313':'Arabic - Kuwait', '13322':'Spanish - Chile', '14337':'Arabic - U.A.E.', '14346':'Spanish - Uruguay', '15361':'Arabic - Bahrain', '15370':'Spanish - Paraguay', '16385':'Arabic - Qatar', '16394':'Spanish - Bolivia', '17418':'Spanish - El Salvador', '18442':'Spanish - Honduras', '19466':'Spanish - Nicaragua', '20490':'Spanish - Puerto Rico'}
    try:
      if arrayLanguages.has_key(code):
        retValue = arrayLanguages[code]
      else:
        retValue = "%s (OS Language)" % (code) if code.strip() != "" else ""

    except:
      retValue = "%s (OS Language)" % (code) if code.strip() != "" else ""

    return retValue


def getOperatingSystemSKU(code):

    arrayTypes = {'0':'Undefined', '1':'Ultimate Edition', '2':'Home Basic Edition', '3':'Home Premium Edition', '4':'Enterprise Edition', '5':'Home Basic N Edition', '6':'Business Edition', '7':'Standard Server Edition', '8':'Datacenter Server Edition', '9':'Small Business Server Edition', '10':'Enterprise Server Edition', '11':'Starter Edition', '12':'Datacenter Server Core Edition', '13':'Standard Server Core Edition', '14':'Enterprise Server Core Edition', '15':'Enterprise Server Edition for Itanium-Based Systems', '16':'Business N Edition', '17':'Web Server Edition', '18':'Cluster Server Edition', '19':'Home Server Edition', '20':'Storage Express Server Edition', '21':'Storage Standard Server Edition', '22':'Storage Workgroup Server Edition', '23':'Storage Enterprise Server Edition', '24':'Server For Small Business Edition', '25':'Small Business Server Premium Edition', '29':'Web Server, Server Core', '39':'Datacenter Edition without Hyper-V, Server Core', '40':'Standard Edition without Hyper-V, Server Core', '41':'Enterprise Edition without Hyper-V, Server Core', '42':'Hyper-V Server'}
    try:
      if arrayTypes.has_key(code):
        retValue = arrayTypes[code]
      else:
        retValue = "%s (OS Code)" % (code) if code.strip() != "" else ""

    except:
      retValue = "%s (OS Code)" % (code) if code.strip() != "" else ""

    return retValue


def getSIDType(code):

    arrayTypes = [ '', 'SidTypeUser', 'SidTypeGroup', 'SidTypeDomain', 'SidTypeAlias', 'SidTypeWellKnownGroup', 'SidTypeDeletedAccount', 'SidTypeInvalid', 'SidTypeUnknown', 'SidTypeComputer']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (SIDType)" % (code) if code.strip() != "" else ""

    return retValue 


def getAccountType(code):

    arrayTypes = {'256':'UF_TEMP_DUPLICATE_ACCOUNT ', '512':'UF_NORMAL_ACCOUNT', '2048':'UF_INTERDOMAIN_TRUST_ACCOUNT', '4096':'UF_WORKSTATION_TRUST_ACCOUNT', '8192':'UF_SERVER_TRUST_ACCOUNT'}
    try:
      if arrayTypes.has_key(code):
        retValue = arrayTypes[code]
      else:
        retValue = "%s (AccountType)" % (code) if code.strip() != "" else ""

    except:
      retValue = "%s (AccountType)" % (code) if code.strip() != "" else ""

    return retValue


def getSoftwareElementState(code):

    arrayStates = [ 'Deployable', 'Installable', 'Executable', 'Running']
    try:
      retValue = arrayStates[int(code)]
    except:
      retValue = "%s (State Code)" % (code) if code.strip() != "" else ""

    return retValue

def getChar(code):

    arrayChars = [ 'Reserved', 'Reserved', 'Unknown', 'BIOS Characteristics Not Supported', 'ISA is supported', 'MCA is supported', 'EISA is supported', 'PCI is supported', 'PC Card (PCMCIA) is supported', 'Plug and Play is supported', 'APM is supported', 'BIOS is Upgradable (Flash)', 'BIOS shadowing is allowed', 'VL-VESA is supported', 'ESCD support is available', 'Boot from CD is supported', 'Selectable Boot is supported', 'BIOS ROM is socketed', 'Boot From PC Card (PCMCIA) is supported', 'EDD (Enhanced Disk Drive) Specification is supported', 'Int 13h - Japanese Floppy for NEC 9800 1.2mb (3.5, 1k Bytes/Sector, 360 RPM) is supported', 'Int 13h - Japanese Floppy for Toshiba 1.2mb (3.5, 360 RPM) is supported', 'Int 13h - 5.25 / 360 KB Floppy Services are supported', 'Int 13h - 5.25 /1.2MB Floppy Services are supported', 'Int 13h - 3.5 / 720 KB Floppy Services are supported', 'Int 13h - 3.5 / 2.88 MB Floppy Services are supported', 'Int 5h, Print Screen Service is supported', 'Int 9h, 8042 Keyboard services are supported', 'Int 14h, Serial Services are supported', 'Int 17h, printer services are supported', 'Int 10h, CGA/Mono Video Services are supported', 'NEC PC-98', 'ACPI is supported', 'USB Legacy is supported', 'AGP is supported', 'I2O boot is supported', 'LS-120 boot is supported', 'ATAPI ZIP Drive boot is supported', '1394 boot is supported', 'Smart Battery is supported', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for BIOS vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor', 'Reserved for system vendor']

    try:
      retValue = arrayChars[int(code)]
    except:
      retValue = "%s (Char Code)" % (code) if code.strip() != "" else ""

    return retValue


def getConfigManagerErrorCode(code):

    arrayErrors = [ 'Device is working properly', 'Device is not configured correctly', 'Windows cannot load the driver for this device', 'Driver for this device might be corrupted or the system may be low on memory or other resources', 'Device is not working properly. One of its drivers or the registry might be corrupted', 'Driver for the device requires a resource that Windows cannot manage', 'Boot configuration for the device conflicts with other devices', 'Cannot filter', 'Driver loader for the device is missing', 'Device is not working properly. The controlling firmware is incorrectly reporting the resources for the device', 'Device cannot start', 'Device failed', 'Device cannot find enough free resources to use', 'Windows cannot verify the devices resources', 'Device cannot work properly until the computer is restarted', 'Device is not working properly due to a possible re-enumeration problem', 'Windows cannot identify all of the resources that the device uses', 'Device is requesting an unknown resource type', 'Device drivers must be reinstalled', 'Failure using the VxD loader', 'Registry might be corrupted', 'System failure. If changing the device driver is ineffective, see the hardware documentation. Windows is removing the device', 'Device is disabled', 'System failure. If changing the device driver is ineffective, see the hardware documentation', 'Device is not present, not working properly, or does not have all of its drivers installed', 'Windows is still setting up the device', 'Windows is still setting up the device', 'Device does not have valid log configuration', 'Device drivers are not installed', 'Device is disabled. The device firmware did not provide the required resources', 'Device is using an IRQ resource that another device is using', 'Device is not working properly. Windows cannot load the required device drivers']

    try:
      retValue = arrayErrors[int(code)]
    except:
      retValue = "%s (Error Code)" % (code) if code.strip() != "" else ""

    return retValue


def getCPUStatus(code):

    arrayTypes = [ 'Unknown', 'CPU Enabled', 'CPU Disabled by User via BIOS Setup', 'CPU Disabled by BIOS (POST Error)', 'CPU Is Idle', 'Reserved', 'Reserved', 'Other']

    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Status Code)" % (code) if code.strip() != "" else ""

    return retValue


def getFamily(code):

    arrayFamilies = { '1':'Other', '2':'Unknown', '3':'8086', '4':'80286', '5':'Intel386 Processor', '6':'Intel486 Processor', '7':'8087', '8':'80287', '9':'80387', '10':'80487', '11':'Pentium Brand', '12':'Pentium Pro', '13':'Pentium II', '14':'Pentium Processor with MMX Technology', '15':'Celeron', '16':'Pentium II Xeon', '17':'Pentium III', '18':'M1 Family', '19':'M2 Family', '24':'AMD Duron Processor Family', '25':'K5 Family', '26':'K6 Family', '27':'K6-2', '28':'K6-3', '29':'AMD Athlon Processor Family', '30':'AMD2900 Family', '31':'K6-2+', '32':'Power PC Family', '33':'Power PC 601', '34':'Power PC 603', '35':'Power PC 603+', '36':'Power PC 604', '37':'Power PC 620', '38':'Power PC X704', '39':'Power PC 750', '48':'Alpha Family', '49':'Alpha 21064', '50':'Alpha 21066', '51':'Alpha 21164', '52':'Alpha 21164PC', '53':'Alpha 21164a', '54':'Alpha 21264', '55':'Alpha 21364', '64':'MIPS Family', '65':'MIPS R4000', '66':'MIPS R4200', '67':'MIPS R4400', '68':'MIPS R4600', '69':'MIPS R10000', '80':'SPARC Family', '81':'SuperSPARC', '82':'microSPARC II', '83':'microSPARC IIep', '84':'UltraSPARC', '85':'UltraSPARC II', '86':'UltraSPARC IIi', '87':'UltraSPARC III', '88':'UltraSPARC IIIi', '96':'68040', '97':'68xxx Family', '98':'68000', '99':'68010', '100':'68020', '101':'68030', '112':'Hobbit Family', '120':'Crusoe TM5000 Family', '121':'Crusoe TM3000 Family', '122':'Efficeon TM8000 Family', '128':'Weitek', '130':'Itanium Processor', '131':'AMD Athlon 64 Processor Family', '132':'AMD Opteron Processor Family', '144':'PA-RISC Family', '145':'PA-RISC 8500', '146':'PA-RISC 8000', '147':'PA-RISC 7300LC', '148':'PA-RISC 7200', '149':'PA-RISC 7100LC', '150':'PA-RISC 7100', '160':'V30 Family', '176':'Pentium III Xeon Processor', '177':'Pentium III Processor with Intel SpeedStep Technology', '178':'Pentium 4', '179':'Intel Xeon', '180':'AS400 Family', '181':'Intel Xeon Processor MP', '182':'AMD Athlon XP Family', '183':'AMD Athlon MP Family', '184':'Intel Itanium 2', '185':'Intel Pentium M Processor', '190':'K7', '198':'Intel Core i7-2760QM', '200':'IBM390 Family', '201':'G4', '202':'G5', '203':'G6', '204':'z/Architecture Base', '250':'i860', '251':'i960', '260':'SH-3', '261':'SH-4', '280':'ARM', '281':'StrongARM', '300':'6x86', '301':'MediaGX', '302':'MII', '320':'WinChip', '350':'DSP', '500':'Video Processor'}
    try:
      if arrayFamilies.has_key(code):
        retValue = arrayFamilies[code]
      else:
        retValue = "%s (Family Code)" % (code) if code.strip() != "" else ""

    except:
      retValue = "%s (Family Code)" % (code) if code.strip() != "" else ""

    return retValue


def getProcessorType(code):

    arrayTypes = [ '', 'Other', 'Unknown', 'Central Processor', 'Math Processor', 'DSP Processor', 'Video Processor']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getAvailability(code):

    arrayTypes = [ '', 'Other', 'Unknown', 'Running or Full Power', 'Warning', 'In test', 'Not Applicable', 'Power Off', 'Off Line', 'Off Duty', 'Degraded', 'Not Installed', 'Install Error', 'Power Save - Unknown', 'Power Save - Low Power Mode', 'Power Save- Standby', 'Power Cycle', 'Power Save - Warning']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getNetConnectionStatus(code):

    arrayStates = [ 'Disconnected', 'Connecting', 'Connected', 'Disconnecting', 'Hardware not present', 'Hardware disabled', 'Hardware malfunction', 'Media disconnected', 'Authenticating', 'Authentication succeeded', 'Authentication failed', 'Invalid address', 'Credentials required']

    try:
      retValue = arrayStates[int(code)]
    except:
      retValue = "%s (State Code)" % (code) if code.strip() != "" else ""

    return retValue


def getIGMPLevel(code):

    arrayTypes = [ 'No Multicast', 'IP Multicast', 'IP and IGMP Multicast']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (IGMP Code)" % (code) if code.strip() != "" else ""

    return retValue


def getLocation(code):

    arrayLocations = [ 'Reserved', 'Other', 'Unknown', 'System board or motherboard', 'ISA add-on card', 'EISA add-on card', 'PCI add-on card', 'MCA add-on card', 'PCMCIA add-on card', 'Proprietary add-on card', 'NuBus', 'PC-98/C20 add-on card', 'PC-98/C24 add-on card', 'PC-98/E add-on card', 'PC-98/Local bus add-on card']
    try:
      retValue = arrayLocations[int(code)]
    except:
      retValue = "%s (Location Code)" % (code) if code.strip() != "" else ""

    return retValue


def getMemoryErrorCorrection(code):

    arrayTypes = [ 'Reserved', 'Other', 'Unknown', 'None', 'Parity', 'Single-bit ECC', 'Multi-bit ECC', 'CRC']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Error Code)" % (code) if code.strip() != "" else ""

    return retValue


def getUse(code):

    arrayUses = [ 'Reserved', 'Other', 'Unknown', 'System Memory', 'Video Memory', 'Flash Memory', 'Nonvolatile RAM', 'Cache Memory']
    try:
      retValue = arrayUses[int(code)]
    except:
      retValue = "%s (Error Code)" % (code) if code.strip() != "" else ""

    return retValue


def getFormFactor(code):

    arrayTypes = [ 'Unknown', 'Other', 'SIP', 'DIP', 'ZIP', 'SOJ', 'Proprietary', 'SIMM', 'DIMM', 'TSOP', 'PGA', 'RIMM', 'SODIMM', 'SRIMM', 'SMD', 'SSMP', 'QFP', 'TQFP', 'SOIC', 'LCC', 'PLCC', 'BGA', 'FPBGA', 'LGA']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getMemoryType(code):

    arrayTypes = [ 'Unknown', 'Other', 'DRAM', 'Synchronous DRAM', 'Cache DRAM', 'EDO', 'EDRAM', 'VRAM', 'SRAM', 'RAM', 'ROM', 'Flash', 'EEPROM', 'FEPROM', 'EPROM', 'CDRAM', '3DRAM', 'SDRAM', 'SGRAM', 'RDRAM', 'DDR', 'DDR2', 'DDR2 FB-DIMM', 'DDR3', 'FBD2']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getCap(code):

    arrayCaps = [ 'Unknown', 'Other', 'Sequential Access', 'Random Access', 'Supports Writing', 'Encryption', 'Compression', 'Supports Removable Media', 'Manual Cleaning', 'Automatic Cleaning', 'SMART Notification', 'Supports Dual-Sided Media', 'Ejection Prior to Drive Dismount Not Required']
    try:
      retValue = arrayCaps[int(code)]
    except:
      retValue = "%s (Capability Code)" % (code) if code.strip() != "" else ""

    return retValue


def getAccess(code):

    arrayAccess = [ 'Unknown', 'Readable', 'Writable', 'Read/write Supported', 'Write Once']
    try:
      retValue = arrayAccess[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getDriveType(code):

    arrayTypes = [ 'Unknown', 'No Root Directory', 'Removable Disk', 'Local Disk', 'Network Drive', 'Compact Disc', 'RAM Disk']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getDeviceType(code):

    arrayTypes = [ '', 'Other', 'Unknown', 'Video', 'SCSI Controller', 'Ethernet', 'Token Ring', 'Sound']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Undefined)" % (code) if code.strip() != "" else ""

    return retValue


def getBusType(code):

    arrayTypes = [ 'Internal', 'ISA', 'EISA', 'MicroChannel', 'TurboChannel', 'PCI Bus', 'VME Bus', 'NuBus', 'PCMCIA Bus', 'C Bus', 'MPI Bus', 'MPSA Bus', 'Internal Processor', 'Internal Power Bus', 'PNP ISA Bus', 'PNP Bus', 'Maximum Interface Type']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Undefined)" % (code) if code.strip() != "" else ""

    return retValue


def getConnectorType(code):

    arrayTypes = [ 'Unknown', 'Other', 'Male', 'Female', 'Shielded', 'Unshielded', 'SCSI (A) High-Density (50 pins)', 'SCSI (A) Low-Density (50 pins)', 'SCSI (P) High-Density (68 pins)', 'SCSI SCA-I (80 pins)', 'SCSI SCA-II (80 pins)', 'SCSI Fibre Channel (DB-9, Copper)', 'SCSI Fibre Channel (Fibre)', 'SCSI Fibre Channel SCA-II (40 pins)', 'SCSI Fibre Channel SCA-II (20 pins)', 'SCSI Fibre Channel BNC', 'ATA 3-1/2 Inch (40 pins)', 'ATA 2-1/2 Inch (44 pins)', 'ATA-2', 'ATA-3', 'ATA/66', 'DB-9', 'DB-15', 'DB-25', 'DB-36', 'RS-232C', 'RS-422', 'RS-423', 'RS-485', 'RS-449', 'V.35', 'X.21', 'IEEE-488', 'AUI', 'UTP Category 3', 'UTP Category 4', 'UTP Category 5', 'BNC', 'RJ11', 'RJ45', 'Fiber MIC', 'AppleAUI', 'Apple GeoPort', 'PCI', 'ISA', 'EISA', 'VESA', 'PCMCIA', 'PCMCIA Type I', 'PCMCIA Type II', 'PCMCIA Type III', 'ZV Port', 'CardBus', 'USB', 'IEEE 1394', 'HIPPI', 'HSSDC (6 pins)', 'GBIC', 'DIN', 'Mini-DIN', 'Micro-DIN', 'PS/2', 'Infrared', 'HP-HIL', 'Access.bus', 'NuBus', 'Centronics', 'Mini-Centronics', 'Mini-Centronics Type-14', 'Mini-Centronics Type-20', 'Mini-Centronics Type-26', 'Bus Mouse', 'ADB', 'AGP', 'VME Bus', 'VME64', 'Propietary', 'Proprietary Processor Card Slot', 'Proprietary Memory Card Slot', 'Proprietary I/O Riser Slot', 'PCI-66MHZ', 'AGP2X', 'AGP4X', 'PC-98', 'PC-98-Hireso', 'PC-H98', 'PC-98Note', 'PC-98Full', 'SSA SCSI', 'Circular', 'On Board IDE Connector', 'On Board Floppy Connector', '9 Pin Dual Inline', '25 Pin Dual Inline', '50 Pin Dual Inline', '68 Pin Dual Inline', 'On Board Sound Connector', 'Mini-Jack', 'PCI-X', 'Sbus IEEE 1396-1993 32 Bit', 'Sbus IEEE 1396-1993 64 Bit', 'MCA', 'GIO', 'XIO', 'HIO', 'NGIO', 'PMC', 'MTRJ', 'VF-45', 'Future I/O', 'SC', 'SG', 'Electrical', 'Optical', 'Ribbon', 'GLM', '1x9', 'Mini SG', 'LC', 'HSSC', 'VHDCI Shielded (68 pins)', 'InfiniBand']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Undefined)" % (code) if code.strip() != "" else ""

    return retValue


def getPortType(code):

    arrayTypes = [ 'None', 'Parallel Port XT/AT Compatible', 'Parallel Port PS/2', 'Parallel Port ECP', 'Parallel Port EPP', 'Parallel Port ECP/EPP', 'Serial Port XT/AT Compatible', 'Serial Port 16450 Compatible', 'Serial Port 16550 Compatible', 'Serial Port 16550A Compatible', 'SCSI Port', 'MIDI Port', 'Joy Stick Port', 'Keyboard Port' , 'Mouse Port', 'SSA SCSI', 'USB', 'FireWire (IEEE P1394)', 'PCMCIA Type I', 'PCMCIA Type II', 'PCMCIA Type III', 'CardBus', 'Access Bus Port', 'SCSI II', 'SCSI Wide', 'PC-98', 'PC-98-Hireso', 'PC-H98', 'Video Port', 'Audio Port', 'Modem Port', 'Network Port', '8251 Compatible', '8251 FIFO Compatible']
    try:
      retValue = arrayTypes[int(code)]
    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def getType(code):

    arrayTypes = {'0':'Disk Drive', '1':'Print Queue',  '2':'Device', '3':'IPC', '2147483648':'Disk Drive Admin', '2147483649':'Print Queue Admin', '2147483650':'Device Admin', '2147483651':'IPC Admin'}
    try:
      if arrayTypes.has_key(code):
        retValue = arrayTypes[code]
      else:
        retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    except:
      retValue = "%s (Type Code)" % (code) if code.strip() != "" else ""

    return retValue


def show_ComputerSystem():

    print "    \"ComputerSystem\": {"

    ### Name ###
    retName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"name\": \"%s\"," % (formatCad(retName))    

    ### Domain ###
    retDomain = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"domain\": \"%s\"," % (formatCad(retDomain))

    ### Part Of Domain ###
    retPartOfDomain = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PartOfDomain from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PartOfDomain$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"partOfDomain\": \"%s\"," % (formatCad(retPartOfDomain))

    ### Workgroup ###
    retWorkgroup = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,Workgroup from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|Workgroup$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"workgroup\": \"%s\"," % (formatCad(retWorkgroup))

    ### Caption ###
    retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"caption\": \"%s\"," % (formatCad(retCaption)) 

    ### Description ###
    retDescription = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Description,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Description|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"description\": \"%s\"," % (formatCad(retDescription))

    ### Domain Role ###
    retDomainRole = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DomainRole,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DomainRole|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"domainRole\": \"%s\"," % (formatCad(getDomainRole(retDomainRole)))

    ### Roles ###
    retRoles = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,Roles from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|Roles$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"roles\": ["
    if retRoles.startswith('(') and retRoles.endswith(')'):
      listRoles = retRoles[1:len(retRoles)-1].split(',')
    else:
      listRoles = retRoles.split(',') 

    countRoles = 1 
    for role in listRoles:
      print "        \"%s\"%s" % (formatCad(role), ("",",") [ countRoles < len(listRoles) ])
      countRoles += 1
    print "      ],"

    ### Current Time Zone ###
    retCurrentTimeZone = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CurrentTimeZone,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CurrentTimeZone|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"currentTimeZone\": \"%s\"," % (formatCad(retCurrentTimeZone))

    ### Manufacturer ###
    retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Manufacturer,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Manufacturer|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

    ### Model ###
    retModel = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Model,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Model|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"model\": \"%s\"," % (formatCad(retModel))

    ### Primary Owner Name ###
    retPrimaryOwnerName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PrimaryOwnerName from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PrimaryOwnerName$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"primaryOwnerName\": \"%s\"," % (formatCad(retPrimaryOwnerName))

    ### PC System Type ###
    retPCSystemType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PCSystemType from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PCSystemType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"PCSystemType\": \"%s\"," % (formatCad(getPCSystemType(retPCSystemType)))

    ### System Type ###
    retSystemType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SystemType from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SystemType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"systemType\": \"%s\"," % (formatCad(retSystemType))

    ### Wake Up Type ###
    retWakeUpType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,WakeUpType from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|WakeUpType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"wakeUpType\": \"%s\"," % (formatCad(getWakeUpType(retWakeUpType)))

    ### Infrared Supported ###
    retInfraredSupported = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select InfraredSupported,Name from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^InfraredSupported|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"infraredSupported\": \"%s\"," % (formatCad(retInfraredSupported))

    ### Number Of Processors ###
    retNumberOfProcessors = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,NumberOfProcessors from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|NumberOfProcessors$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"numberOfProcessors\": \"%s\"," % (formatCad(retNumberOfProcessors))

    ### Number Of Logical Processors ###
    retNumberOfLogicalProcessors = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,NumberOfLogicalProcessors from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|NumberOfLogicalProcessors$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"numberOfLogicalProcessors\": \"%s\"," % (formatCad(retNumberOfLogicalProcessors))

    ### Total Physical Memory ###
    retTotalPhysicalMemory = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,TotalPhysicalMemory from Win32_ComputerSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|TotalPhysicalMemory$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"totalPhysicalMemory\": \"%s\"" % (formatCad(retTotalPhysicalMemory))

    print "    },"


def show_OperatingSystem():

    print "    \"OperatingSystem\": {"

    ### Name ###
    retName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"name\": \"%s\"," % (formatCad(retName))

    ### Boot Device ###
    retBootDevice = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BootDevice,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BootDevice|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"bootDevice\": \"%s\"," % (formatCad(retBootDevice))

    ### Caption ###
    retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"caption\": \"%s\"," % (formatCad(retCaption))

    ### Description ###
    retDescription = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Description,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Description|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"description\": \"%s\"," % (formatCad(retDescription))

    ### CSD Version ###
    retCSDVersion = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CSDVersion,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CSDVersion|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"CSDVersion\": \"%s\"," % (formatCad(retCSDVersion))

    ### Service Pack Major-Minor Version ###
    retServicePackMajorMinorVersion = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,ServicePackMajorVersion,ServicePackMinorVersion from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|ServicePackMajorVersion|ServicePackMinorVersion$'|rev|cut -d'|' -f1,2|rev|tr '|' '.') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"servicePackMajorMinorVersion\": \"%s\"," % (formatCad(retServicePackMajorMinorVersion))

    ### OS Arquitecture ###
    retOSArchitecture = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,OSArchitecture from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|OSArchitecture$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"OSArchitecture\": \"%s\"," % (formatCad(retOSArchitecture))

    ### OS Product Suite ###
    retOSProductSuite = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,OSProductSuite from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|OSProductSuite$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    arraySuites = {16384:'Windows Server 2003, Compute Cluster Edition', 8192:'Windows Storage Server 2003 R2', 1024:'Windows Server 2003, Web Edition', 512:'Windows Home Edition', 256:'Terminal Services, but only one interactive session is supported', 128:'Windows Server 2008 Datacenter or Windows Server 2003, Datacenter Edition', 64:'Windows Embedded', 32:'Microsoft Small Business Server with the restrictive client license', 16:'Terminal Services', 8:'Communication Server', 4:'Windows BackOffice components', 2:'Windows Server 2008 Enterprise or Windows Server 2003, Enterprise Edition', 1:'Microsoft Small Business Server, but may upgraded to another version of Windows'}
    print "      \"OSProductSuite\": ["
    try:
      countSuites = int(retOSProductSuite)

      for key in sorted(arraySuites.iterkeys(),reverse=True):
        if countSuites >= key:
	  countSuites = countSuites-key
	  print "        \"%s\"%s" % (formatCad(arraySuites[key]), ("",",") [ countSuites <> 0 ]) 

    except:
     countSuites = 0 

    print "      ],"

    ### OS Type ###
    retOSType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,OSType from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|OSType$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"OSType\": \"%s\"," % (formatCad(getOSType(retOSType)))

    ### Product Type ###
    retProductType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,ProductType from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|ProductType$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"productType\": \"%s\"," % (formatCad(getProductType(retProductType)))

    ### Version ###
    retVersion = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,Version from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|Version$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"version\": \"%s\"," % (formatCad(retVersion))

    ### Serial Number ###
    retSerialNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SerialNumber from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SerialNumber$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"serialNumber\": \"%s\"," % (formatCad(retSerialNumber))

    ### Country Code ###
    retCountryCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CountryCode,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CountryCode|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"countryCode\": \"%s\"," % (formatCad(getCountryCode(retCountryCode)))

    ### OS Language ###
    retOSLanguage = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,OSLanguage from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|OSLanguage$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"OSLanguage\": \"%s\"," % (formatCad(getOSLanguage(retOSLanguage)))

    ### PAE Enabled ###
    retPAEEnabled = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PAEEnabled from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PAEEnabled$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"PAEEnabled\": \"%s\"," % (formatCad(retPAEEnabled))

    ### Manufacturer ###
    retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Manufacturer,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Manufacturer|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

    ### Current Time Zone ###
    retCurrentTimeZone = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CurrentTimeZone,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CurrentTimeZone|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"currentTimeZone\": \"%s\"," % (formatCad(retCurrentTimeZone))

    ### Encryption Level ###
    retEncryptionLevel = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select EncryptionLevel,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^EncryptionLevel|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"encryptionLevel\": \"%s\"," % (formatCad(retEncryptionLevel))

    ### Number Of Licensed Users ###
    retNumberOfLicensedUsers = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,NumberOfLicensedUsers from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|NumberOfLicensedUsers$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"numberOfLicensedUsers\": \"%s\"," % (formatCad(retNumberOfLicensedUsers))

    ### Operating System SKU ###
    retOperatingSystemSKU = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,OperatingSystemSKU from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|OperatingSystemSKU$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"operatingSystemSKU\": \"%s\"," % (formatCad(getOperatingSystemSKU(retOperatingSystemSKU)))

    ### Organization ###
    retOrganization = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,Organization from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|Organization$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"organization\": \"%s\"," % (formatCad(retOrganization))

    ### Registered User ###
    retRegisteredUser = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,RegisteredUser from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|RegisteredUser$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"registeredUser\": \"%s\"," % (formatCad(retRegisteredUser))

    ### Max Number Of Processes ###
    retMaxNumberOfProcesses = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select MaxNumberOfProcesses,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^MaxNumberOfProcesses|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"maxNumberOfProcesses\": \"%s\"," % (formatCad(retMaxNumberOfProcesses))

    ### Max Process Memory Size ###
    retMaxProcessMemorySize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select MaxProcessMemorySize,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^MaxProcessMemorySize|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"maxProcessMemorySize\": \"%s\"," % (formatCad(retMaxProcessMemorySize))

    ### System Device ###
    retSystemDevice = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SystemDevice from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SystemDevice$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"systemDevice\": \"%s\"," % (formatCad(retSystemDevice))

    ### System Drive ###
    retSystemDrive = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SystemDrive from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SystemDrive$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"systemDrive\": \"%s\"," % (formatCad(retSystemDrive))

    ### Windows Directory ###
    retWindowsDirectory = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,WindowsDirectory from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|WindowsDirectory$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"windowsDirectory\": \"%s\"," % (formatCad(retWindowsDirectory))

    ### System Directory ###
    retSystemDirectory = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SystemDirectory from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SystemDirectory$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"systemDirectory\": \"%s\"," % (formatCad(retSystemDirectory))

    ### Total Visible Memory Size ###
    retTotalVisibleMemorySize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,TotalVisibleMemorySize from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|TotalVisibleMemorySize$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"totalVisibleMemorySize\": \"%s\"," % (formatCad(retTotalVisibleMemorySize))

    ### Total Swap Space Size ###
    retTotalSwapSpaceSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,TotalSwapSpaceSize from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|TotalSwapSpaceSize$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"totalSwapSpaceSize\": \"%s\"," % (formatCad(retTotalSwapSpaceSize))

    ### SizeStoredInPagingFiles ###
    retSizeStoredInPagingFiles = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SizeStoredInPagingFiles from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SizeStoredInPagingFiles$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"sizeStoredInPagingFiles\": \"%s\"," % (formatCad(retSizeStoredInPagingFiles))

    ### Total Virtual Memory Size ###
    retTotalVirtualMemorySize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,TotalVirtualMemorySize from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|TotalVirtualMemorySize$'|rev|cut -d'|' -f1|rev) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"totalVirtualMemorySize\": \"%s\"," % (formatCad(retTotalVirtualMemorySize))

    ### Distributed ###
    retDistributed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Distributed,Name from Win32_OperatingSystem') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Distributed|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"distributed\": \"%s\"" % (formatCad(retDistributed))

    print "    },"


def show_SystemDriver():

    # Getting Total System Drivers 
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from win32_SystemDriver') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"SystemDriver\": ["
      # Getting System Drivers
      count = 1
      
      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,ErrorControl,Name,PathName,ServiceType,StartMode,State,TagId from win32_SystemDriver') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|ErrorControl|Name|PathName|ServiceType|StartMode|State|TagId$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

      	data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,ErrorControl,Name,PathName,ServiceType,StartMode,State,TagId from win32_SystemDriver') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|ErrorControl|Name|PathName|ServiceType|StartMode|State|TagId$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
      	data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from win32_SystemDriver') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

	if directLoop == "true":
	  retCaption = line.split('|')[0].strip()
	  retErrorControl = line.split('|')[1].strip()
	  retName = line.split('|')[2].strip()
	  retPathName = line.split('|')[3].strip()
	  retServiceType = line.split('|')[4].strip()
	  retStartMode = line.split('|')[5].strip()
	  retState = line.split('|')[6].strip()
	  retTagId = line.split('|')[7].strip()
	else:
	  Name = line.strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retErrorControl = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ErrorControl,Name from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ErrorControl|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retName = Name
          retPathName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PathName from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PathName$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retServiceType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,ServiceType from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|ServiceType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retStartMode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,StartMode from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|StartMode$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retState = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,State from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|State$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTagId = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,TagId from Win32_SystemDriver where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|TagId$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Name ###
        print "        \"name\": \"%s\"," % (formatCad(retName))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Error Control ###
        print "        \"errorControl\": \"%s\"," % (formatCad(retErrorControl))

        ### Path Name ###
        print "        \"pathName\": \"%s\"," % (formatCad(retPathName))

        ### Service Type ###
        print "        \"serviceType\": \"%s\"," % (formatCad(retServiceType))

        ### Start Mode ###
        print "        \"startMode\": \"%s\"," % (formatCad(retStartMode))

        ### State ###
        print "        \"state\": \"%s\"," % (formatCad(retState))

        ### TagId ###
        print "        \"tagId\": \"%s\"" % (formatCad(retTagId))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_Service():

    # Getting Total Services
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from win32_Service') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"Service\": ["
      # Getting Services
      count = 1
     
      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,ErrorControl,Name,PathName,ProcessId,StartMode,State,TagId from win32_Service') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^$Caption|ErrorControl|Name|PathName|ProcessId|StartMode|State|TagId$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,ErrorControl,Name,PathName,ProcessId,StartMode,State,TagId from win32_Service') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|ErrorControl|Name|PathName|ProcessId|StartMode|State|TagId$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
      	data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from win32_Service') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retErrorControl = line.split('|')[1].strip()
          retName = line.split('|')[2].strip()
          retPathName = line.split('|')[3].strip()
	  retProcessId = line.split('|')[4].strip()
          retStartMode = line.split('|')[5].strip()
          retState = line.split('|')[6].strip()
          retTagId = line.split('|')[7].strip()
        else:
	  Name = line.strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retErrorControl = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ErrorControl,Name from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ErrorControl|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retName = Name
          retPathName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PathName from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PathName$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retProcessId = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,ProcessId from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|ProcessId$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retStartMode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,StartMode from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|StartMode$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retState = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,State from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|State$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTagId = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,TagId from Win32_Service where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|TagId$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Name ###
        print "        \"name\": \"%s\"," % (formatCad(retName))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Error Control ###
        print "        \"errorControl\": \"%s\"," % (formatCad(retErrorControl))

        ### Path Name ###
        print "        \"pathName\": \"%s\"," % (formatCad(retPathName))

        ### ProcessId ###
        print "        \"processId\": \"%s\"," % (formatCad(retProcessId))

        ### Start Mode ###
        print "        \"startMode\": \"%s\"," % (formatCad(retStartMode))

        ### State ###
        print "        \"state\": \"%s\"," % (formatCad(retState))

        ### TagId ###
        print "        \"tagId\": \"%s\"" % (formatCad(retTagId))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_SystemAccount():

    # Getting Total System Accounts 
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from win32_SystemAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"SystemAccount\": ["
      # Getting System Accounts
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,LocalAccount,Name,SID,SIDType,Status from win32_SystemAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|LocalAccount|Name|SID|SIDType|Status$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,LocalAccount,Name,SID,SIDType,Status from win32_SystemAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|LocalAccount|Name|SID|SIDType|Status$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from win32_SystemAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retDomain = line.split('|')[1].strip()
          retLocalAccount = line.split('|')[2].strip()
          retName = line.split('|')[3].strip()
          retSID = line.split('|')[4].strip()
          retSIDType = line.split('|')[5].strip()
          retStatus = line.split('|')[6].strip()
        else:
      	  Domain = line.split('|',1)[0].strip()
       	  Name = line.split('|',1)[1].strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,Name from Win32_SystemAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retDomain = Domain
          retLocalAccount = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,LocalAccount,Name from Win32_SystemAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|LocalAccount|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retName = Name
          retSID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,SID from Win32_SystemAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|SID$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSIDType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,SIDType from Win32_SystemAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|SIDType$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retStatus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,Status from Win32_SystemAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|Status$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

	### Domain ###
	print "        \"domain\": \"%s\"," % (formatCad(retDomain))

        ### Name ###
	print "        \"name\": \"%s\"," % (formatCad(retName))

	### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Local Account ###
        print "        \"localAccount\": \"%s\"," % (formatCad(retLocalAccount))

        ### SID ###
	print "        \"SID\": \"%s\"," % (formatCad(retSID))

        ### SID Type ###
	print "        \"SIDType\": \"%s\"," % (formatCad(getSIDType(retSIDType)))

        ### Status ###
	print "        \"status\": \"%s\"" % (formatCad(retStatus))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_UserAccount():

    # Getting Total User Accounts
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from win32_UserAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"UserAccount\": ["
      # Getting User Accounts
      count = 1
      
      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select AccountType,Caption,Disabled,Domain,FullName,LocalAccount,Lockout,Name,PasswordChangeable,PasswordExpires,PasswordRequired,SID,SIDType,Status from win32_UserAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^AccountType|Caption|Disabled|Domain|FullName|LocalAccount|Lockout|Name|PasswordChangeable|PasswordExpires|PasswordRequired|SID|SIDType|Status$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select AccountType,Caption,Disabled,Domain,FullName,LocalAccount,Lockout,Name,PasswordChangeable,PasswordExpires,PasswordRequired,SID,SIDType,Status from win32_UserAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^AccountType|Caption|Disabled|Domain|FullName|LocalAccount|Lockout|Name|PasswordChangeable|PasswordExpires|PasswordRequired|SID|SIDType|Status$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from win32_UserAccount') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines(): 

        if directLoop == "true":
	  retAccountType = line.split('|')[0].strip()
          retCaption = line.split('|')[1].strip()
	  retDisabled = line.split('|')[2].strip()
          retDomain = line.split('|')[3].strip()
	  retFullName = line.split('|')[4].strip()
          retLocalAccount = line.split('|')[5].strip()
	  retLockout = line.split('|')[6].strip()
          retName = line.split('|')[7].strip()
	  retPasswordChangeable = line.split('|')[8].strip()
          retPasswordExpires = line.split('|')[9].strip()
          retPasswordRequired = line.split('|')[10].strip()
          retSID = line.split('|')[11].strip()
          retSIDType = line.split('|')[12].strip()
          retStatus = line.split('|')[13].strip()
        else:
          Domain = line.split('|',1)[0].strip()
          Name = line.split('|',1)[1].strip()
          retAccountType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select AccountType,Domain,Name from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^AccountType|Domain|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,Name from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDisabled = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Disabled,Domain,Name from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Disabled|Domain|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retDomain = Domain
          retFullName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,FullName,Name from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|FullName|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retLocalAccount = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,LocalAccount,Name from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|LocalAccount|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retLockout = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Lockout,Name from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Lockout|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retName = Name
          retPasswordChangeable = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,PasswordChangeable from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|PasswordChangeable$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retPasswordExpires = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,PasswordExpires from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|PasswordExpires$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retPasswordRequired = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,PasswordRequired from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|PasswordRequired$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,SID from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|SID$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSIDType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,SIDType from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|SIDType$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retStatus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,Status from Win32_UserAccount where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|Status$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Domain ###
        print "        \"domain\": \"%s\"," % (formatCad(retDomain))

        ### Name ###
        print "        \"name\": \"%s\"," % (formatCad(retName))

        ### Account Type ###
        print "        \"accountType\": \"%s\"," % (formatCad(getAccountType(retAccountType)))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Disabled ###
        print "        \"disabled\": \"%s\"," % (formatCad(retDisabled))

        ### Full Name ###
        print "        \"fullName\": \"%s\"," % (formatCad(retFullName))

        ### Local Account ###
        print "        \"localAccount\": \"%s\"," % (formatCad(retLocalAccount))

        ### Lockout ###
        print "        \"lockout\": \"%s\"," % (formatCad(retLockout))

        ### Password Changeable ###
        print "        \"passwordChangeable\": \"%s\"," % (formatCad(retPasswordChangeable))

        ### Password Expires ###
        print "        \"passwordExpires\": \"%s\"," % (formatCad(retPasswordExpires))

        ### Password Required ###
        print "        \"passwordRequired\": \"%s\"," % (formatCad(retPasswordRequired))

        ### SID ###
	print "        \"SID\": \"%s\"," % (formatCad(retSID))

        ### SID Type ###
        print "        \"SIDType\": \"%s\"," % (formatCad(getSIDType(retSIDType)))

        ### Status ###
        print "        \"status\": \"%s\"" % (formatCad(retStatus))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_Group():

    # Getting Total Groups
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from win32_Group') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"Group\": ["
      # Getting Groups
      count = 1
      
      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,LocalAccount,Name,SID,SIDType,Status from win32_Group') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|LocalAccount|Name|SID|SIDType|Status$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,LocalAccount,Name,SID,SIDType,Status from win32_Group') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|LocalAccount|Name|SID|SIDType|Status$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name from win32_Group') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retDomain = line.split('|')[1].strip()
          retLocalAccount = line.split('|')[2].strip()
          retName = line.split('|')[3].strip()
          retSID = line.split('|')[4].strip()
          retSIDType = line.split('|')[5].strip()
          retStatus = line.split('|')[6].strip()
        else:
          Domain = line.split('|',1)[0].strip()
          Name = line.split('|',1)[1].strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Domain,Name from Win32_Group where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Domain|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retDomain = Domain
          retLocalAccount = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,LocalAccount,Name from Win32_Group where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|LocalAccount|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retName = Name
          retSID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,SID from Win32_Group where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|SID$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSIDType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,SIDType from Win32_Group where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|SIDType$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retStatus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Domain,Name,Status from Win32_Group where Domain=\"%s\" and  Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Domain|Name|Status$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Domain, Name, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Domain ###
        print "        \"domain\": \"%s\"," % (formatCad(retDomain))

        ### Name ###
        print "        \"name\": \"%s\"," % (formatCad(retName))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Local Account ###
        print "        \"localAccount\": \"%s\"," % (formatCad(retLocalAccount))

        ### SID ###
        print "        \"SID\": \"%s\"," % (formatCad(retSID))

        ### SID Type ###
        print "        \"SIDType\": \"%s\"," % (formatCad(getSIDType(retSIDType)))

        ### Status ###
        print "        \"status\": \"%s\"" % (formatCad(retStatus))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_GroupUser():

    # Getting Total Groups-Users
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select GroupComponent,PartComponent from win32_GroupUser') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^GroupComponent|PartComponent$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"GroupUser\": ["
      # Getting Groups-Users
      count = 1
      data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select GroupComponent,PartComponent from win32_GroupUser') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^GroupComponent|PartComponent$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for line in data.stdout.readlines():
        print "      {"

        groupComponent = line.split('|',1)[0].strip().split('.',1)[1].strip()
        partComponent = line.split('|',1)[1].strip().split('.',1)[1].strip()

	groupDomain = groupComponent.split(',',1)[0].strip().split('=',1)[1].strip().replace('"','')
	groupName = groupComponent.split(',',1)[1].strip().split('=',1)[1].strip().replace('"','')
        userDomain = partComponent.split(',',1)[0].strip().split('=',1)[1].strip().replace('"','')
        userName = partComponent.split(',',1)[1].strip().split('=',1)[1].strip().replace('"','')

        print "        \"groupDomain\": \"%s\"," % (formatCad(groupDomain))
        print "        \"groupName\": \"%s\"," % (formatCad(groupName))
        print "        \"userDomain\": \"%s\"," % (formatCad(userDomain))
        print "        \"userName\": \"%s\"" % (formatCad(userName))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_BIOS():

    print "    \"BIOS\": {"

    ### Name ###
    retName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"name\": \"%s\"," % (formatCad(retName))

    ### Caption ###
    retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"caption\": \"%s\"," % (formatCad(retCaption))

    ### Software Element ID ###
    retSoftwareElementID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"softwareElementID\": \"%s\"," % (formatCad(retSoftwareElementID))

    ### Software Element State ###
    retSoftwareElementState = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f3) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"softwareElementState\": \"%s\"," % (formatCad(getSoftwareElementState(retSoftwareElementState)))

    ### Target Operating System ###
    retTargetOperatingSystem = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f4) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    arrayTypes = [ 'Unknown', 'Other', 'MACROS', 'ATTUNIX', 'DGUX', 'DECNT', 'Digital Unix', 'OpenVMS', 'HPUX', 'AIX', 'MVS', 'OS400', 'OS/2', 'JavaVM', 'MSDOS', 'WIN3X', 'WIN95', 'WIN98', 'WINNT', 'WINCE', 'NCR3000', 'NetWare', 'OSF', 'DC/OS', 'Reliant UNIX', 'SCO UnixWare', 'SCO OpenServer', 'Sequent', 'IRIX', 'Solaris', 'SunOS', 'U6000', 'ASERIES', 'TandemNSK', 'TandemNT', 'BS2000', 'LINUX', 'Lynx', 'XENIX', 'VM/ESA', 'Interactive UNIX', 'BSDUNIX', 'FreeBSD', 'NetBSD', 'GNU Hurd', 'OS9', 'MACH Kernel', 'Inferno', 'QNX', 'EPOC', 'IxWorks', 'VxWorks', 'MiNT', 'BeOS', 'HP MPE', 'NextStep', 'PalmPilot', 'Rhapsody']
    try:
      retValue = arrayTypes[int(retTargetOperatingSystem)]
    except:
      retValue = "%s (Type Code)" % (retTargetOperatingSystem) if retTargetOperatingSystem.strip() != "" else ""

    print "      \"targetOperatingSystem\": \"%s\"," % (formatCad(retValue))

    ### Version ###
    retVersion = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f5) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"version\": \"%s\"," % (formatCad(retVersion))

    ### Build Number ###
    retBuildNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BuildNumber,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BuildNumber|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"buildNumber\": \"%s\"," % (formatCad(retBuildNumber))


    ### Code Set ###
    retCodeSet = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CodeSet,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CodeSet|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"codeSet\": \"%s\"," % (formatCad(retCodeSet))

    ### Current Language ###
    retCurrentLanguage = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CurrentLanguage,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CurrentLanguage|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"currentLanguage\": \"%s\"," % (formatCad(retCurrentLanguage))

    ### Identification Code ###
    retIdentificationCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select IdentificationCode,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^IdentificationCode|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"identificationCode\": \"%s\"," % (formatCad(retIdentificationCode))

    ### Language Edition ###
    retLanguageEdition = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select LanguageEdition,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^LanguageEdition|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"languageEdition\": \"%s\"," % (formatCad(retLanguageEdition))

    ### Manufacturer ###
    retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Manufacturer,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Manufacturer|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

    ### Primary BIOS ###
    retPrimaryBIOS = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,PrimaryBIOS,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|PrimaryBIOS|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"primaryBIOS\": \"%s\"," % (formatCad(retPrimaryBIOS))

    ### Release Date ###
    retReleaseDate = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,ReleaseDate,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|ReleaseDate|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"releaseDate\": \"%s\"," % (formatCad("%s/%s/%s" % (retReleaseDate[:4],retReleaseDate[4:6],retReleaseDate[6:8])))

    ### Serial Number ###
    retSerialNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SerialNumber,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SerialNumber|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"serialNumber\": \"%s\"," % (formatCad(retSerialNumber))

    ### Status ###
    retStatus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,SoftwareElementID,SoftwareElementState,Status,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|SoftwareElementID|SoftwareElementState|Status|TargetOperatingSystem|Version$'|cut -d'|' -f4) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
    print "      \"status\": \"%s\"," % (formatCad(retStatus))

    ### Bios Characteristics ###
    retBiosCharacteristics = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BiosCharacteristics,Name,SoftwareElementID,SoftwareElementState,TargetOperatingSystem,Version from Win32_BIOS') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BiosCharacteristics|Name|SoftwareElementID|SoftwareElementState|TargetOperatingSystem|Version$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

    listChar = retBiosCharacteristics.replace("(","").replace(")","").split(",") 
    print "      \"biosCharacteristics\": ["
    countChar = 1
    for char in listChar:
      print "        {"
      print "          \"charCode\": \"%s\"," % (formatCad(char))
      print "          \"description\": \"%s\"" % (formatCad(getChar(char)))
      print "        }%s" % (("",",") [ countChar < len(listChar) ])
      countChar += 1

    print "      ]"

    print "    },"


def show_Processor():

    # Getting Total Processors
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_Processor') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"Processor\": ["
      # Getting Processors
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,ConfigManagerErrorCode,CPUStatus,CurrentClockSpeed,DataWidth,DeviceID,Family,L2CacheSize,L2CacheSpeed,L3CacheSize,L3CacheSpeed,Manufacturer,MaxClockSpeed,Name,NumberOfCores,NumberOfLogicalProcessors,ProcessorID,ProcessorType from win32_Processor') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|ConfigManagerErrorCode|CPUStatus|CurrentClockSpeed|DataWidth|DeviceID|Family|L2CacheSize|L2CacheSpeed|L3CacheSize|L3CacheSpeed|Manufacturer|MaxClockSpeed|Name|NumberOfCores|NumberOfLogicalProcessors|ProcessorID|ProcessorType$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,ConfigManagerErrorCode,CPUStatus,CurrentClockSpeed,DataWidth,DeviceID,Family,L2CacheSize,L2CacheSpeed,L3CacheSize,L3CacheSpeed,Manufacturer,MaxClockSpeed,Name,NumberOfCores,NumberOfLogicalProcessors,ProcessorID,ProcessorType from win32_Processor') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|ConfigManagerErrorCode|CPUStatus|CurrentClockSpeed|DataWidth|DeviceID|Family|L2CacheSize|L2CacheSpeed|L3CacheSize|L3CacheSpeed|Manufacturer|MaxClockSpeed|Name|NumberOfCores|NumberOfLogicalProcessors|ProcessorID|ProcessorType$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
        directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_Processor') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retConfigManagerErrorCode = line.split('|')[1].strip()
          retCPUStatus = line.split('|')[2].strip()
          retCurrentClockSpeed = line.split('|')[3].strip()
          retDataWidth = line.split('|')[4].strip()
          retDeviceID = line.split('|')[5].strip()
          retFamily = line.split('|')[6].strip()
          retL2CacheSize = line.split('|')[7].strip()
          retL2CacheSpeed = line.split('|')[8].strip()
          retL3CacheSize = line.split('|')[9].strip()
          retL3CacheSpeed = line.split('|')[10].strip()
          retManufacturer = line.split('|')[11].strip()
          retMaxClockSpeed = line.split('|')[12].strip()
          retName = line.split('|')[13].strip()
          retNumberOfCores = line.split('|')[14].strip()
          retNumberOfLogicalProcessors = line.split('|')[15].strip()
          retProcessorID = line.split('|')[16].strip()
          retProcessorType = line.split('|')[17].strip()
        else:
	  DeviceID = line.strip()
          retName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID, Name from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,DeviceID from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retConfigManagerErrorCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConfigManagerErrorCode,DeviceID from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConfigManagerErrorCode|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCPUStatus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CPUStatus,DeviceID from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CPUStatus|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCurrentClockSpeed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select CurrentClockSpeed,DeviceID from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^CurrentClockSpeed|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDataWidth = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DataWidth,DeviceID from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DataWidth|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retDeviceID = DeviceID
          retFamily = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Family from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Family$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retL2CacheSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,L2CacheSize from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|L2CacheSize$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retL2CacheSpeed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,L2CacheSpeed from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|L2CacheSpeed$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retL3CacheSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,L3CacheSize from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|L3CacheSize$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retL3CacheSpeed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,L3CacheSpeed from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|L3CacheSpeed$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Manufacturer from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Manufacturer$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMaxClockSpeed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,MaxClockSpeed from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|MaxClockSpeed$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retNumberOfCores = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,NumberOfCores from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|NumberOfCores$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retNumberOfLogicalProcessors = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,NumberOfLogicalProcessors from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|NumberOfLogicalProcessors$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retProcessorID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,ProcessorID from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|ProcessorID$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retProcessorType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,ProcessorType from Win32_Processor where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|ProcessorType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

	print "      {"

	### Device ID ###
	print "        \"deviceID\": \"%s\"," % (formatCad(retDeviceID))

	### Name ###
	print "        \"name\": \"%s\"," % (formatCad(retName))

	### Caption ###
	print "        \"caption\": \"%s\"," % (formatCad(retCaption))

	### Config Manager Error Code ###
	print "        \"configManagerErrorCode\": \"%s\"," % (formatCad(getConfigManagerErrorCode(retConfigManagerErrorCode)))

        ### CPU Status ###
        print "        \"CPUStatus\": \"%s\"," % (formatCad(getCPUStatus(retCPUStatus)))

        ### Current Clock Speed ###
	print "        \"currentClockSpeed\": \"%s\"," % (formatCad(retCurrentClockSpeed))

        ### Data Width ###
        print "        \"dataWidth\": \"%s\"," % (formatCad(retDataWidth))

        ### Family ###
        print "        \"family\": \"%s\"," % (formatCad(getFamily(retFamily)))

        ### L2 Cache Size ###
        print "        \"L2CacheSize\": \"%s\"," % (formatCad(retL2CacheSize))

        ### L2 Cache Speed ###
        print "        \"L2CacheSpeed\": \"%s\"," % (formatCad(retL2CacheSpeed))

        ### L3 Cache Size ###
        print "        \"L3CacheSize\": \"%s\"," % (formatCad(retL2CacheSize))

        ### L3 Cache Speed ###
        print "        \"L3CacheSpeed\": \"%s\"," % (formatCad(retL3CacheSpeed))

        ### Manufacturer ###
        print "        \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

        ### Max Clock Speed ###
        print "        \"maxClockSpeed\": \"%s\"," % (formatCad(retMaxClockSpeed))

        ### Number Of Cores ###
        print "        \"numberOfCores\": \"%s\"," % (formatCad(retNumberOfCores))

        ### Number Of Logical Processors ###
        print "        \"numberOfLogicalProcessors\": \"%s\"," % (formatCad(retNumberOfLogicalProcessors))

        ### Processor ID ###
        print "        \"processorID\": \"%s\"," % (formatCad(retProcessorID))

        ### Processor Type ###
	print "        \"processorType\": \"%s\"" % (formatCad(getProcessorType(retProcessorType)))

	print "      }%s" % (("",",") [ count < total ])

	count += 1

      print "    ],"


def show_NetworkAdapter():

    # Getting Total Network Adapters
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_NetworkAdapter') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"NetworkAdapter\": ["
      # Getting Network Adapters 
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select AdapterType,Availability,ConfigManagerErrorCode,DeviceID,Index,MACAddress,Manufacturer,Name,NetConnectionID,NetConnectionStatus,ServiceName from win32_NetworkAdapter') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^AdapterType|Availability|ConfigManagerErrorCode|DeviceID|Index|MACAddress|Manufacturer|Name|NetConnectionID|NetConnectionStatus|ServiceName$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select AdapterType,Availability,ConfigManagerErrorCode,DeviceID,Index,MACAddress,Manufacturer,Name,NetConnectionID,NetConnectionStatus,ServiceName from win32_NetworkAdapter') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^AdapterType|Availability|ConfigManagerErrorCode|DeviceID|Index|MACAddress|Manufacturer|Name|NetConnectionID|NetConnectionStatus|ServiceName$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_NetworkAdapter') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retAdapterType = line.split('|')[0].strip()
          retAvailability = line.split('|')[1].strip()
          retConfigManagerErrorCode = line.split('|')[2].strip()
          retDeviceID = line.split('|')[3].strip()
          retIndex = line.split('|')[4].strip()
          retMACAddress = line.split('|')[5].strip()
          retManufacturer = line.split('|')[6].strip()
          retName = line.split('|')[7].strip()
          retNetConnectionID = line.split('|')[8].strip()
          retNetConnectionStatus = line.split('|')[9].strip()
          retServiceName = line.split('|')[10].strip()
        else:
          DeviceID = line.strip()
	  retDeviceID = DeviceID
          retName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Name from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Name$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAdapterType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select AdapterType,DeviceID from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^AdapterType|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Manufacturer from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Manufacturer$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMACAddress = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,MACAddress from Win32_NetworkAdapter where DeviceID=\"%s\"')|grep -iv '^CLASS:'|grep -iv '^DeviceID|MACAddress$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAvailability = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,DeviceID from Win32_NetworkAdapter where DeviceID=\"%s\"')|grep -iv '^CLASS:'|grep -iv '^Availability|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retConfigManagerErrorCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConfigManagerErrorCode,DeviceID from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConfigManagerErrorCode|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retIndex = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Index from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Index$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retNetConnectionID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,NetConnectionID from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|NetConnectionID$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retNetConnectionStatus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,NetConnectionStatus from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|NetConnectionStatus$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retServiceName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,ServiceName from Win32_NetworkAdapter where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|ServiceName$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Device ID ###
        print "        \"deviceID\": \"%s\"," % (formatCad(retDeviceID))

        ### Name ###
	print "        \"name\": \"%s\"," % (formatCad(retName))

        ### Adapter Type ###
        print "        \"adapterType\": \"%s\"," % (formatCad(retAdapterType))

        ### Manufacturer ###
        print "        \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

        ### MACAddress ###
        print "        \"MACAddress\": \"%s\"," % (formatCad(retMACAddress))

        ### Availability ###
        print "        \"availability\": \"%s\"," % (formatCad(getAvailability(retAvailability)))

        ### Config Manager Error Code ###
        print "        \"configManagerErrorCode\": \"%s\"," % (formatCad(getConfigManagerErrorCode(retConfigManagerErrorCode)))

        ### Index ###
        print "        \"index\": \"%s\"," % (formatCad(retIndex))

        ### Net Connection ID ###
        print "        \"netConnectionID\": \"%s\"," % (formatCad(retNetConnectionID))

        ### Net Connection Status ###
        print "        \"netConnectionStatus\": \"%s\"," % (formatCad(getNetConnectionStatus(retNetConnectionStatus)))

        ### Service Name ###
        print "        \"serviceName\": \"%s\"" % (formatCad(retServiceName))

        print "      }%s" % (("",",") [ count < total ])

        count += 1

      print "    ],"


def show_NetworkAdapterConfiguration():

    # Getting Total Network Adapter Configurations
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index from win32_NetworkAdapterConfiguration') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"NetworkAdapterConfiguration\": ["
      # Getting Network Adapter Configurations
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DefaultIPGateway,DefaultTOS,DefaultTTL,Description,DHCPEnabled,DHCPServer,DNSDomain,DNSDomainSuffixSearchOrder,DNSEnabledForWINSResolution,DNSServerSearchOrder,IGMPLevel,Index,IPAddress,IPSubnet,MACAddress,WINSEnableLMHostsLookup,WINSPrimaryServer,WINSSecondaryServer from win32_NetworkAdapterConfiguration') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DefaultIPGateway|DefaultTOS|DefaultTTL|Description|DHCPEnabled|DHCPServer|DNSDomain|DNSDomainSuffixSearchOrder|DNSEnabledForWINSResolution|DNSServerSearchOrder|IGMPLevel|Index|IPAddress|IPSubnet|MACAddress|WINSEnableLMHostsLookup|WINSPrimaryServer|WINSSecondaryServer$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DefaultIPGateway,DefaultTOS,DefaultTTL,Description,DHCPEnabled,DHCPServer,DNSDomain,DNSDomainSuffixSearchOrder,DNSEnabledForWINSResolution,DNSServerSearchOrder,IGMPLevel,Index,IPAddress,IPSubnet,MACAddress,WINSEnableLMHostsLookup,WINSPrimaryServer,WINSSecondaryServer from win32_NetworkAdapterConfiguration') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DefaultIPGateway|DefaultTOS|DefaultTTL|Description|DHCPEnabled|DHCPServer|DNSDomain|DNSDomainSuffixSearchOrder|DNSEnabledForWINSResolution|DNSServerSearchOrder|IGMPLevel|Index|IPAddress|IPSubnet|MACAddress|WINSEnableLMHostsLookup|WINSPrimaryServer|WINSSecondaryServer$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
      	data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index from win32_NetworkAdapterConfiguration') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index$'|grep -v '^$') || echo'') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
   	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retDefaultIPGateway = line.split('|')[0].strip()
          retDefaultTOS = line.split('|')[1].strip()
          retDefaultTTL = line.split('|')[2].strip()
          retDescription = line.split('|')[3].strip()
          retDHCPEnabled = line.split('|')[4].strip()
          retDHCPServer = line.split('|')[5].strip()
          retDNSDomain = line.split('|')[6].strip()
          retDNSDomainSuffixSearchOrder = line.split('|')[7].strip()
          retDNSEnabledForWINSResolution = line.split('|')[8].strip()
          retDNSServerSearchOrder = line.split('|')[9].strip()
          retIGMPLevel = line.split('|')[10].strip()
          retIndex = line.split('|')[11].strip()
          retIPAddress = line.split('|')[12].strip()
          retIPSubnet = line.split('|')[13].strip()
          retMACAddress = line.split('|')[14].strip()
	  retWINSEnableLMHostsLookup = line.split('|')[15].strip()
          retWINSPrimaryServer = line.split('|')[16].strip()
          retWINSSecondaryServer = line.split('|')[17].strip()
        else:
          Index = line.strip()
	  retIndex = Index
          retDescription = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Description,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Description|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retIPAddress = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index,IPAddress from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index|IPAddress$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retIPSubnet = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index,IPSubnet from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index|IPSubnet$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDefaultIPGateway = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DefaultIPGateway,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DefaultIPGateway|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDefaultTOS = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DefaultTOS,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DefaultTOS|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDefaultTTL = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DefaultTTL,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DefaultTTL|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDHCPEnabled = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DHCPEnabled,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"')|grep -iv '^CLASS:'|grep -iv '^DHCPEnabled|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDHCPServer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DHCPServer,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DHCPServer|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDNSDomain = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DNSDomain,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DNSDomain|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDNSDomainSuffixSearchOrder = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DNSDomainSuffixSearchOrder,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DNSDomainSuffixSearchOrder|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDNSEnabledForWINSResolution = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DNSEnabledForWINSResolution,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DNSEnabledForWINSResolution|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDNSServerSearchOrder = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DNSServerSearchOrder,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DNSServerSearchOrder|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retIGMPLevel = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select IGMPLevel,Index from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^IGMPLevel|Index$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMACAddress = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index,MACAddress from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index|MACAddress$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
	  retWINSEnableLMHostsLookup = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index,WINSEnableLMHostsLookup from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index|WINSEnableLMHostsLookup$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retWINSPrimaryServer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index,WINSPrimaryServer from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index|WINSPrimaryServer$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retWINSSecondaryServer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Index,WINSSecondaryServer from Win32_NetworkAdapterConfiguration where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Index|WINSSecondaryServer$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Index ###
        print "        \"index\": \"%s\"," % (formatCad(retIndex))

        ### Description ###
        print "        \"description\": \"%s\"," % (formatCad(retDescription))

        ### IP Address ###
	if retIPAddress.startswith('(') and retIPAddress.endswith(')'):
	  retIPAddress = retIPAddress[1:len(retIPAddress)-1]

        print "        \"IPAddress\": \"%s\"," % (formatCad(retIPAddress))

        ### IP Subnet ###
        if retIPSubnet.startswith('(') and retIPSubnet.endswith(')'):
          retIPSubnet = retIPSubnet[1:len(retIPSubnet)-1]

        print "        \"IPSubnet\": \"%s\"," % (formatCad(retIPSubnet))

        ### Default IP Gateway ###
        if retDefaultIPGateway.startswith('(') and retDefaultIPGateway.endswith(')'):
          retDefaultIPGateway = retDefaultIPGateway[1:len(retDefaultIPGateway)-1]

        print "        \"defaultIPGateway\": \"%s\"," % (formatCad(retDefaultIPGateway))

        ### Default TOS ###
	print "        \"defaultTOS\": \"%s\"," % (formatCad(retDefaultTOS))

        ### Default TTL ###
        print "        \"defaultTTL\": \"%s\"," % (formatCad(retDefaultTTL))

        ### DHCP Enabled ###
        print "        \"DHCPEnabled\": \"%s\"," % (formatCad(retDHCPEnabled))

	### DHCP Server ###
        if retDHCPServer.startswith('(') and retDHCPServer.endswith(')'):
          retDHCPServer = retDHCPServer[1:len(retDHCPServer)-1]

        print "        \"DHCPServer\": \"%s\"," % (formatCad(retDHCPServer))

        ### DNS Domain ###
        if retDNSDomain.startswith('(') and retDNSDomain.endswith(')'):
          retDNSDomain = retDNSDomain[1:len(retDNSDomain)-1]

        print "        \"DNSDomain\": \"%s\"," % (formatCad(retDNSDomain))

        ### DNS Domain Suffix Search Order ###
        if retDNSDomainSuffixSearchOrder.startswith('(') and retDNSDomainSuffixSearchOrder.endswith(')'):
          retDNSDomainSuffixSearchOrder = retDNSDomainSuffixSearchOrder[1:len(retDNSDomainSuffixSearchOrder)-1]

        print "        \"DNSDomainSuffixSearchOrder\": \"%s\"," % (formatCad(retDNSDomainSuffixSearchOrder))

        ### DNS Enabled For WINS Resolution ###
        print "        \"DNSEnabledForWINSResolution\": \"%s\"," % (formatCad(retDNSEnabledForWINSResolution))

        ### DNS Server Search Order ###
        if retDNSServerSearchOrder.startswith('(') and retDNSServerSearchOrder.endswith(')'):
          retDNSServerSearchOrder = retDNSServerSearchOrder[1:len(retDNSServerSearchOrder)-1]

        print "        \"DNSDomainSearchOrder\": \"%s\"," % (formatCad(retDNSServerSearchOrder.replace(',',' ')))

        ### IGMP Level ###
        print "        \"IGMPLevel\": \"%s\"," % (formatCad(getIGMPLevel(retIGMPLevel)))

        ### MAC Address ###
        print "        \"MACAddress\": \"%s\"," % (formatCad(retMACAddress))

        ### WINS Enable LMHosts Lookup ###
        print "        \"WINSEnableLMHostsLookup\": \"%s\"," % (formatCad(retWINSEnableLMHostsLookup))

        ### WINS Primary Server ###
        if retWINSPrimaryServer.startswith('(') and retWINSPrimaryServer.endswith(')'):
          retWINSPrimaryServer = retWINSPrimaryServer[1:len(retWINSPrimaryServer)-1]

        print "        \"WINSPrimaryServer\": \"%s\"," % (formatCad(retWINSPrimaryServer))

        ### WINS Secondary Server ###
        if retWINSSecondaryServer.startswith('(') and retWINSSecondaryServer.endswith(')'):
          retWINSSecondaryServer = retWINSSecondaryServer[1:len(retWINSSecondaryServer)-1]

        print "        \"WINSSecondaryServer\": \"%s\"" % (formatCad(retWINSSecondaryServer))

        print "      }%s" % (("",",") [ count < total ])

        count += 1

      print "    ],"


def show_NetworkAdapterSetting():

    # Getting Total Network Adapter Settings
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Element,Setting from win32_NetworkAdapterSetting') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Element|Setting$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"NetworkAdapterSetting\": ["
      # Getting Network Adapter Settings 
      count = 1
      data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Element,Setting from win32_NetworkAdapterSetting') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Element|Setting$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for line in data.stdout.readlines():
        print "      {"

        element = line.split('|',1)[0].strip().split('.',1)[1].strip()
        setting = line.split('|',1)[1].strip().split('.',1)[1].strip()

        elementDeviceID = element.strip().split('=',1)[1].strip().replace('"','')
        settingIndex = setting.strip().split('=',1)[1].strip().replace('"','')

        print "        \"deviceID\": \"%s\"," % (formatCad(elementDeviceID))
        print "        \"index\": \"%s\"" % (formatCad(settingIndex))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_PhysicalMemoryArray():

    # Getting Total Physical Memory Arrays 
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_PhysicalMemoryArray') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"PhysicalMemoryArray\": ["
      # Getting Physical Memory Arrays
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,HotSwappable,Location,MaxCapacity,MemoryDevices,MemoryErrorCorrection,Tag,Use from win32_PhysicalMemoryArray') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|HotSwappable|Location|MaxCapacity|MemoryDevices|MemoryErrorCorrection|Tag|Use$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,HotSwappable,Location,MaxCapacity,MemoryDevices,MemoryErrorCorrection,Tag,Use from win32_PhysicalMemoryArray') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|HotSwappable|Location|MaxCapacity|MemoryDevices|MemoryErrorCorrection|Tag|Use$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
      	data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_PhysicalMemoryArray') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retHotSwappable = line.split('|')[1].strip()
          retLocation = line.split('|')[2].strip()
          retMaxCapacity = line.split('|')[3].strip()
          retMemoryDevices = line.split('|')[4].strip()
          retMemoryErrorCorrection = line.split('|')[5].strip()
          retTag = line.split('|')[6].strip()
          retUse = line.split('|')[7].strip()
        else:
          Tag = line.strip()
	  retTag = Tag
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Tag from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retHotSwappable = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select HotSwappable,Tag from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^HotSwappable|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retLocation = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Location,Tag from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Location|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMaxCapacity = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select MaxCapacity,Tag from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^MaxCapacity|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMemoryDevices = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select MemoryDevices,Tag from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^MemoryDevices|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMemoryErrorCorrection = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select MemoryErrorCorrection,Tag from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^MemoryErrorCorrection|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retUse = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag,Use from Win32_PhysicalMemoryArray where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag|Use$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Tag ###
        print "        \"tag\": \"%s\"," % (formatCad(retTag))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Hot Swappable ###
        print "        \"hotSwappable\": \"%s\"," % (formatCad(retHotSwappable))

        ### Location ###
        print "        \"location\": \"%s\"," % (formatCad(getLocation(retLocation)))

        ### Max Capacity ###
        print "        \"maxCapacity\": \"%s\"," % (formatCad(retMaxCapacity))

        ### Memory Devices ###
        print "        \"memoryDevices\": \"%s\"," % (formatCad(retMemoryDevices))

        ### Memory Error Correction ###
        print "        \"memoryErrorCorrection\": \"%s\"," % (formatCad(getMemoryErrorCorrection(retMemoryErrorCorrection)))

        ### Use ###
        print "        \"use\": \"%s\"" % (formatCad(getUse(retUse)))


        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_PhysicalMemory():

    # Getting Total Physical Memories
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_PhysicalMemory') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"PhysicalMemory\": ["
      # Getting Physical Memories
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Capacity,Caption,DataWidth,DeviceLocator,FormFactor,HotSwappable,Manufacturer,MemoryType,PositionInRow,Speed,Tag,TotalWidth from win32_PhysicalMemory') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Capacity|Caption|DataWidth|DeviceLocator|FormFactor|HotSwappable|Manufacturer|MemoryType|PositionInRow|Speed|Tag|TotalWidth$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Capacity,Caption,DataWidth,DeviceLocator,FormFactor,HotSwappable,Manufacturer,MemoryType,PositionInRow,Speed,Tag,TotalWidth from win32_PhysicalMemory') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Capacity|Caption|DataWidth|DeviceLocator|FormFactor|HotSwappable|Manufacturer|MemoryType|PositionInRow|Speed|Tag|TotalWidth$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_PhysicalMemory') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCapacity = line.split('|')[0].strip()
          retCaption = line.split('|')[1].strip()
          retDataWidth = line.split('|')[2].strip()
          retDeviceLocator = line.split('|')[3].strip()
          retFormFactor = line.split('|')[4].strip()
          retHotSwappable = line.split('|')[5].strip()
          retManufacturer = line.split('|')[6].strip()
          retMemoryType = line.split('|')[7].strip()
          retPositionInRow = line.split('|')[8].strip()
          retSpeed = line.split('|')[9].strip()
          retTag = line.split('|')[10].strip()
          retTotalWidth = line.split('|')[11].strip()
        else:
          Tag = line.strip()
	  retTag = Tag
          retCapacity = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Capacity,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Capacity|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDataWidth = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DataWidth,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DataWidth|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTotalWidth = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag,TotalWidth from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag|TotalWidth$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDeviceLocator = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceLocator,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceLocator|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retFormFactor = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select FormFactor,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^FormFactor|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retHotSwappable = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select HotSwappable,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^HotSwappable|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Manufacturer,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Manufacturer|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMemoryType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select MemoryType,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^MemoryType|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retPositionInRow = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select PositionInRow,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^PositionInRow|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSpeed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Speed,Tag from Win32_PhysicalMemory where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Speed|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Tag ###
        print "        \"tag\": \"%s\"," % (formatCad(retTag))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Capacity ###
        print "        \"capacity\": \"%s\"," % (formatCad(retCapacity))

        ### Data Width ###
        print "        \"dataWidth\": \"%s\"," % (formatCad(retDataWidth))

        ### Total Width ###
        print "        \"totalWidth\": \"%s\"," % (formatCad(retTotalWidth))

        ### Device Locator ###
        print "        \"deviceLocator\": \"%s\"," % (formatCad(retDeviceLocator))

        ### Form Factor ###
        print "        \"formFactor\": \"%s\"," % (formatCad(getFormFactor(retFormFactor)))

        ### Hot Swappable ###
        print "        \"hotSwappable\": \"%s\"," % (formatCad(retHotSwappable))

        ### Manufacturer ###
        print "        \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

        ### Memory Type ###
        print "        \"memoryType\": \"%s\"," % (formatCad(getMemoryType(retMemoryType)))

        ### Position In Row ###
        print "        \"positionInRow\": \"%s\"," % (formatCad(retPositionInRow))

        ### Speed ###
        print "        \"speed\": \"%s\"" % (formatCad(retSpeed))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_PhysicalMemoryLocation():

    # Getting Total Physical Memory Locations 
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select GroupComponent,PartComponent from win32_PhysicalMemoryLocation') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^GroupComponent|PartComponent$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"PhysicalMemoryLocation\": ["
      # Getting Network Adapter Settings
      count = 1
      data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select GroupComponent,PartComponent from win32_PhysicalMemoryLocation') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^GroupComponent|PartComponent$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for line in data.stdout.readlines():
        print "      {"

        group = line.split('|',1)[0].strip().split('.',1)[1].strip()
        part = line.split('|',1)[1].strip().split('.',1)[1].strip()

        groupTag = group.strip().split('=',1)[1].strip().replace('"','')
        partTag = part.strip().split('=',1)[1].strip().replace('"','')

        print "        \"groupTag\": \"%s\"," % (formatCad(groupTag))
        print "        \"partTag\": \"%s\"" % (formatCad(partTag))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_DiskDrive():

    # Getting Total Disk Drives
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Index from win32_DiskDrive') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Index$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"DiskDrive\": ["
      # Getting Disk Drives 
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,BytesPerSector,Capabilities,Caption,ConfigManagerErrorCode,DefaultBlockSize,DeviceID,Index,InterfaceType,MediaType,Model,Partitions,SCSIBus,SCSILogicalUnit,SCSIPort,SCSITargetID,SectorsPerTrack,SerialNumber,Size,TotalCylinders,TotalHeads,TotalSectors,TotalTracks,TracksPerCylinder from win32_DiskDrive') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|BytesPerSector|Capabilities|Caption|ConfigManagerErrorCode|DefaultBlockSize|DeviceID|Index|InterfaceType|MediaType|Model|Partitions|SCSIBus|SCSILogicalUnit|SCSIPort|SCSITargetID|SectorsPerTrack|SerialNumber|Size|TotalCylinders|TotalHeads|TotalSectors|TotalTracks|TracksPerCylinder$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,BytesPerSector,Capabilities,Caption,ConfigManagerErrorCode,DefaultBlockSize,DeviceID,Index,InterfaceType,MediaType,Model,Partitions,SCSIBus,SCSILogicalUnit,SCSIPort,SCSITargetID,SectorsPerTrack,SerialNumber,Size,TotalCylinders,TotalHeads,TotalSectors,TotalTracks,TracksPerCylinder from win32_DiskDrive') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|BytesPerSector|Capabilities|Caption|ConfigManagerErrorCode|DefaultBlockSize|DeviceID|Index|InterfaceType|MediaType|Model|Partitions|SCSIBus|SCSILogicalUnit|SCSIPort|SCSITargetID|SectorsPerTrack|SerialNumber|Size|TotalCylinders|TotalHeads|TotalSectors|TotalTracks|TracksPerCylinder$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Index from win32_DiskDrive') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Index$'|grep -v '^$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retAvailability = line.split('|')[0].strip()
          retBytesPerSector = line.split('|')[1].strip()
          retCapabilities = line.split('|')[2].strip()
          retConfigManagerErrorCode = line.split('|')[3].strip()
          retCaption = line.split('|')[4].strip()
          retDefaultBlockSize = line.split('|')[5].strip()
          retDeviceID = line.split('|')[6].strip()
          retIndex = line.split('|')[7].strip()
          retInterfaceType = line.split('|')[8].strip()
          retMediaType = line.split('|')[9].strip()
          retModel = line.split('|')[10].strip()
          retPartitions = line.split('|')[11].strip()
          retSCSIBus = line.split('|')[12].strip()
          retSCSILogicalUnit = line.split('|')[13].strip()
          retSCSIPort = line.split('|')[14].strip()
          retSCSITargetID = line.split('|')[15].strip()
          retSectorsPerTrack = line.split('|')[16].strip()
          retSerialNumber = line.split('|')[17].strip()
          retSize = line.split('|')[18].strip()
          retTotalCylinders = line.split('|')[19].strip()
          retTotalHeads = line.split('|')[20].strip()
          retTotalSectors = line.split('|')[21].strip()
          retTotalTracks = line.split('|')[22].strip()
          retTracksPerCylinder = line.split('|')[23].strip()
        else:
          Index = line.strip()
	  retIndex = Index
          retDeviceID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,DeviceID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retInterfaceType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,InterfaceType from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|InterfaceType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retModel = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Model from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Model$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Size from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Size$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAvailability = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,DeviceID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTotalHeads = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,TotalHeads from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|TotalHeads$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTotalCylinders = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,TotalCylinders from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|TotalCylinders$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTracksPerCylinder = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,TracksPerCylinder from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|TracksPerCylinder$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTotalTracks = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,TotalTracks from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|TotalTracks$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSectorsPerTrack = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SectorsPerTrack from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SectorsPerTrack$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTotalSectors = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,TotalSectors from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|TotalSectors$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retBytesPerSector = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BytesPerSector,DeviceID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BytesPerSector|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDefaultBlockSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DefaultBlockSize,DeviceID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DefaultBlockSize|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retMediaType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,MediaType from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|MediaType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retPartitions = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Partitions from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Partitions$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retConfigManagerErrorCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConfigManagerErrorCode,DeviceID from Win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConfigManagerErrorCode|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSerialNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SerialNumber from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SerialNumber$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSCSIBus = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SCSIBus from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SCSIBus$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSCSIPort = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SCSIPort from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SCSIPort$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSCSITargetID = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SCSITargetID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SCSITargetID$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSCSILogicalUnit = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SCSILogicalUnit from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SCSILogicalUnit$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCapabilities = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Capabilities,DeviceID from win32_DiskDrive where Index=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Capabilities|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Index, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Device ID ###
	retDeviceIDSub = re.sub("\\\\+\.\\\\+","",retDeviceID)
        print "        \"deviceID\": \"%s\"," % (formatCad(retDeviceIDSub))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Index ###
        print "        \"index\": \"%s\"," % (formatCad(retIndex))

        ### Interface Type ###
        print "        \"interfaceType\": \"%s\"," % (formatCad(retInterfaceType))

        ### Model ###
        print "        \"model\": \"%s\"," % (formatCad(retModel))

        ### Size ###
        print "        \"size\": \"%s\"," % (formatCad(retSize))

        ### Availability ###
        print "        \"availability\": \"%s\"," % (formatCad(getAvailability(retAvailability)))

        ### Total Heads ###
        print "        \"totalHeads\": \"%s\"," % (formatCad(retTotalHeads))

        ### Total Cylinders ###
        print "        \"totalCylinders\": \"%s\"," % (formatCad(retTotalCylinders))

        ### Tracks Per Cylinder ###
        print "        \"tracksPerCylinder\": \"%s\"," % (formatCad(retTracksPerCylinder))

        ### Total Tracks ###
        print "        \"totalTracks\": \"%s\"," % (formatCad(retTotalTracks))

        ### Sectors Per Track ###
        print "        \"sectorsPerTrack\": \"%s\"," % (formatCad(retSectorsPerTrack))

        ### Total Sectors ###
        print "        \"totalSectors\": \"%s\"," % (formatCad(retTotalSectors))

        ### Bytes Per Sector ###
        print "        \"bytesPerSector\": \"%s\"," % (formatCad(retBytesPerSector))

        ### Default Block Size ###
        print "        \"defaultBlockSize\": \"%s\"," % (formatCad(retDefaultBlockSize))

        ### Media Type ###
        print "        \"mediaType\": \"%s\"," % (formatCad(retMediaType))

        ### Partitions ###
        print "        \"partitions\": \"%s\"," % (formatCad(retPartitions))

        ### Config Manager Error Code ###
        print "        \"configManagerErrorCode\": \"%s\"," % (formatCad(getConfigManagerErrorCode(retConfigManagerErrorCode)))

        ### Serial Number ###
        print "        \"serialNumber\": \"%s\"," % (formatCad(retSerialNumber))

        ### SCSI Bus ###
        print "        \"SCSIBus\": \"%s\"," % (formatCad(retSCSIBus))

        ### SCSI Port ###
        print "        \"SCSIPort\": \"%s\"," % (formatCad(retSCSIPort))

        ### SCSI TargetID ###
        print "        \"SCSITargetID\": \"%s\"," % (formatCad(retSCSITargetID))

        ### SCSI Logical Unit ###
        print "        \"SCSILogicalUnit\": \"%s\"," % (formatCad(retSCSILogicalUnit))

        ### Capabilities ###
	listCap = retCapabilities.replace("(","").replace(")","").split(",")
	print "        \"capabilities\": ["
	countCap = 1
	for cap in listCap:
	  print "          \"%s\"%s" % (formatCad(getCap(cap)), ("",",") [ countCap < len(listCap) ])
	  countCap += 1

	print "        ]"

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_DiskPartition():

    # Getting Total Disk Partitions
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_DiskPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$'|wc -l)  || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"DiskPartition\": ["
      # Getting Disk Partitions 
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Access,Availability,BlockSize,Bootable,BootPartition,Caption,DeviceID,DiskIndex,Index,NumberOfBlocks,PrimaryPartition,Size,Type from win32_DiskPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Access|Availability|BlockSize|Bootable|BootPartition|Caption|DeviceID|DiskIndex|Index|NumberOfBlocks|PrimaryPartition|Size|Type$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Access,Availability,BlockSize,Bootable,BootPartition,Caption,DeviceID,DiskIndex,Index,NumberOfBlocks,PrimaryPartition,Size,Type from win32_DiskPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Access|Availability|BlockSize|Bootable|BootPartition|Caption|DeviceID|DiskIndex|Index|NumberOfBlocks|PrimaryPartition|Size|Type$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_DiskPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():


        if directLoop == "true":
          retAccess = line.split('|')[0].strip()
          retAvailability = line.split('|')[1].strip()
          retBlockSize = line.split('|')[2].strip()
          retBootable = line.split('|')[3].strip()
          retBootPartition = line.split('|')[4].strip()
          retCaption = line.split('|')[5].strip()
          retDeviceID = line.split('|')[6].strip()
          retDiskIndex = line.split('|')[7].strip()
          retIndex = line.split('|')[8].strip()
          retNumberOfBlocks = line.split('|')[9].strip()
          retPrimaryPartition = line.split('|')[10].strip()
          retSize = line.split('|')[11].strip()
          retType = line.split('|')[12].strip()
        else:
	  DeviceID = line.strip()
	  retDeviceID = DeviceID
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,DeviceID from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDiskIndex = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,DiskIndex from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|DiskIndex$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retIndex = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Index from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Index$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Type from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Type$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Size from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Size$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retBlockSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BlockSize,DeviceID from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BlockSize|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retNumberOfBlocks = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,NumberOfBlocks from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|NumberOfBlocks$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAccess = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Access,DeviceID from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Access|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAvailability = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,DeviceID from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retBootable = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Bootable,DeviceID from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Bootable|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retBootPartition = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BootPartition,DeviceID from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BootPartition|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retPrimaryPartition = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,PrimaryPartition from Win32_DiskPartition where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|PrimaryPartition$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Device ID ###
        print "        \"deviceID\": \"%s\"," % (formatCad(retDeviceID))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Disk Index ###
        print "        \"diskIndex\": \"%s\"," % (formatCad(retDiskIndex))

        ### Index ###
        print "        \"index\": \"%s\"," % (formatCad(retIndex))

        ### Type ###
        print "        \"type\": \"%s\"," % (formatCad(retType))

        ### Size ###
        print "        \"size\": \"%s\"," % (formatCad(retSize))

        ### Block Size ###
        print "        \"blockSize\": \"%s\"," % (formatCad(retBlockSize))

        ### Number Of Blocks ###
        print "        \"numberOfBlocks\": \"%s\"," % (formatCad(retNumberOfBlocks))

        ### Access ###
        print "        \"access\": \"%s\"," % (formatCad(getAccess(retAccess)))

        ### Availability ###
        print "        \"availability\": \"%s\"," % (formatCad(getAvailability(retAvailability)))

        ### Bootable ###
        print "        \"bootable\": \"%s\"," % (formatCad(retBootable))

        ### Boot Partition ###
        print "        \"bootPartition\": \"%s\"," % (formatCad(retBootPartition))

        ### Primary Partition ###
        print "        \"primaryPartition\": \"%s\"" % (formatCad(retPrimaryPartition))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_DiskDriveToDiskPartition():

    # Getting Total Disk Drive To Disk Partitions
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Antecedent,Dependent from win32_DiskDriveToDiskPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Antecedent|Dependent$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"DiskDriveToDiskPartition\": ["
      # Getting Disk Drive To Disk Partitions
      count = 1
      data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Antecedent,Dependent from win32_DiskDriveToDiskPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Antecedent|Dependent$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for line in data.stdout.readlines():
        print "      {"

        antecedent = line.split('|',1)[0].strip().split('.',1)[1].strip()
        dependent = line.split('|',1)[1].strip().split('.',1)[1].strip()

        antecedentDeviceID = antecedent.strip().split('=',1)[1].strip().replace('"','')
 	antecedentDeviceID = re.sub("\\\\+\.\\\\+","",antecedentDeviceID)
        dependentDeviceID = dependent.strip().split('=',1)[1].strip().replace('"','')

        print "        \"diskDeviceID\": \"%s\"," % (formatCad(antecedentDeviceID))
        print "        \"partitionDeviceID\": \"%s\"" % (formatCad(dependentDeviceID))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_LogicalDisk():

    # Getting Total Logical Disks
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_LogicalDisk') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"LogicalDisk\": ["
      # Getting Logical Disks
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Access,Availability,Caption,Compressed,ConfigManagerErrorCode,DeviceID,DriveType,FileSystem,QuotasDisabled,Size,SupportsDiskQuotas,SupportsFileBasedCompression,VolumeName,VolumeSerialNumber from win32_LogicalDisk') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Access|Availability|Caption|Compressed|ConfigManagerErrorCode|DeviceID|DriveType|FileSystem|QuotasDisabled|Size|SupportsDiskQuotas|SupportsFileBasedCompression|VolumeName|VolumeSerialNumber$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Access,Availability,Caption,Compressed,ConfigManagerErrorCode,DeviceID,DriveType,FileSystem,QuotasDisabled,Size,SupportsDiskQuotas,SupportsFileBasedCompression,VolumeName,VolumeSerialNumber from win32_LogicalDisk') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Access|Availability|Caption|Compressed|ConfigManagerErrorCode|DeviceID|DriveType|FileSystem|QuotasDisabled|Size|SupportsDiskQuotas|SupportsFileBasedCompression|VolumeName|VolumeSerialNumber$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
      	data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_LogicalDisk') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
  	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retAccess = line.split('|')[0].strip()
          retAvailability = line.split('|')[1].strip()
          retCaption = line.split('|')[2].strip()
          retCompressed = line.split('|')[3].strip()
          retConfigManagerErrorCode = line.split('|')[4].strip()
          retDeviceID = line.split('|')[5].strip()
          retDriveType = line.split('|')[6].strip()
          retFileSystem = line.split('|')[7].strip()
          retQuotasDisabled = line.split('|')[8].strip()
          retSize = line.split('|')[9].strip()
          retSupportsDiskQuotas = line.split('|')[10].strip()
          retSupportsFileBasedCompression = line.split('|')[11].strip()
          retVolumeName = line.split('|')[12].strip()
	  retVolumeSerialNumber = line.split('|')[13].strip()
        else:
          DeviceID = line.strip()
	  retDeviceID = DeviceID
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,DeviceID from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDriveType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,DriveType from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|DriveType$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retFileSystem = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,FileSystem from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|FileSystem$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSize = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,Size from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|Size$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAccess = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Access,DeviceID from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Access|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAvailability = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,DeviceID from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retCompressed = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Compressed,DeviceID from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Compressed|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retConfigManagerErrorCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConfigManagerErrorCode,DeviceID from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConfigManagerErrorCode|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSupportsDiskQuotas = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SupportsDiskQuotas from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SupportsDiskQuotas$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retQuotasDisabled = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,QuotasDisabled from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|QuotasDisabled$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSupportsFileBasedCompression = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,SupportsFileBasedCompression from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|SupportsFileBasedCompression$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retVolumeName = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,VolumeName from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|VolumeName$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retVolumeSerialNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID,VolumeSerialNumber from Win32_LogicalDisk where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID|VolumeSerialNumber$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Device ID ###
        print "        \"deviceID\": \"%s\"," % (formatCad(retDeviceID))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Drive Type ###
        print "        \"driveType\": \"%s\"," % (formatCad(getDriveType(retDriveType)))

        ### File System ###
        print "        \"fileSystem\": \"%s\"," % (formatCad(retFileSystem))

        ### Size ###
        print "        \"size\": \"%s\"," % (formatCad(retSize))

        ### Access ###
        print "        \"access\": \"%s\"," % (formatCad(getAccess(retAccess)))

        ### Availability ###
        print "        \"availability\": \"%s\"," % (formatCad(getAvailability(retAvailability)))

        ### Compressed ###
        print "        \"compressed\": \"%s\"," % (formatCad(retCompressed))

        ### Config Manager Error Code ###
        print "        \"configManagerErrorCode\": \"%s\"," % (formatCad(getConfigManagerErrorCode(retConfigManagerErrorCode)))

        ### Supports Disk Quotas ###
        print "        \"supportsDiskQuotas\": \"%s\"," % (formatCad(retSupportsDiskQuotas))

        ### Quotas Disabled ###
        print "        \"quotasDisabled\": \"%s\"," % (formatCad(retQuotasDisabled))

        ### Supports File Based Compression ###
        print "        \"supportsFileBasedCompression\": \"%s\"," % (formatCad(retSupportsFileBasedCompression))

        ### Volume Name ###
        print "        \"volumeName\": \"%s\"," % (formatCad(retVolumeName))

        ### Volume Serial Number ###
        print "        \"volumeSerialNumber\": \"%s\"" % (formatCad(retVolumeSerialNumber))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_LogicalDiskToPartition():

    # Getting Total Logical Disk To Partitions
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Antecedent,Dependent from win32_LogicalDiskToPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Antecedent|Dependent$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"LogicalDiskToPartition\": ["
      # Getting Logical Disk To Partitions
      count = 1
      data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Antecedent,Dependent from win32_LogicalDiskToPartition') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Antecedent|Dependent$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for line in data.stdout.readlines():
        print "      {"

        antecedent = line.split('|',1)[0].strip().split('.',1)[1].strip()
        dependent = line.split('|',1)[1].strip().split('.',1)[1].strip()

        antecedentDeviceID = antecedent.strip().split('=',1)[1].strip().replace('"','')
        dependentDeviceID = dependent.strip().split('=',1)[1].strip().replace('"','')

        print "        \"partitionDeviceID\": \"%s\"," % (formatCad(antecedentDeviceID))
        print "        \"logicalDiskDeviceID\": \"%s\"" % (formatCad(dependentDeviceID))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_BaseBoard():

    # Getting Total Base Boards
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_BaseBoard') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"BaseBoard\": ["
      # Getting Base Boards
      count = 1
      data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_BaseBoard') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
      for line in data.stdout.readlines():
        Tag = line.strip()
        print "      {"

        ### Tag ###
        print "        \"tag\": \"%s\"," % (formatCad(Tag))

        ### Caption ###
        retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Manufacturer ###
        retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Manufacturer,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Manufacturer|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

        ### Product ###
        retProduct = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Product,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Product|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"product\": \"%s\"," % (formatCad(retProduct))

        ### Model ###
        retModel = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Model,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Model|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"model\": \"%s\"," % (formatCad(retModel))

        ### Version ###
        retVersion = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag,Version from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag|Version$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"version\": \"%s\"," % (formatCad(retVersion))

        ### Serial Number ###
        retSerialNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select SerialNumber,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^SerialNumber|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"serialNumber\": \"%s\"," % (formatCad(retSerialNumber))

        ### Hosting Board ###
        retHostingBoard = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select HostingBoard,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^HostingBoard|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"hostingBoard\": \"%s\"," % (formatCad(retHostingBoard))

        ### Hot Swappable ###
        retHotSwappable = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select HotSwappable,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^HotSwappable|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"hotSwappable\": \"%s\"," % (formatCad(retHotSwappable))

        ### Powered On ###
        retPoweredOn = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select PoweredOn,Tag from Win32_BaseBoard where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^PoweredOn|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
        print "        \"poweredOn\": \"%s\"" % (formatCad(retPoweredOn))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_OnBoardDevice():

    # Getting Total On Board Devices
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_OnBoardDevice') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"OnBoardDevice\": ["
      # Getting On Board Devices
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Description,DeviceType,Enabled,HotSwappable,Manufacturer,Model,PoweredOn,SerialNumber,Tag,Version from win32_OnBoardDevice') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Description|DeviceType|Enabled|HotSwappable|Manufacturer|Model|PoweredOn|SerialNumber|Tag|Version$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Description,DeviceType,Enabled,HotSwappable,Manufacturer,Model,PoweredOn,SerialNumber,Tag,Version from win32_OnBoardDevice') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Description|DeviceType|Enabled|HotSwappable|Manufacturer|Model|PoweredOn|SerialNumber|Tag|Version$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_OnBoardDevice') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retDescription = line.split('|')[1].strip()
          retDeviceType = line.split('|')[2].strip()
          retEnabled = line.split('|')[3].strip()
          retHotSwappable = line.split('|')[4].strip()
          retManufacturer = line.split('|')[5].strip()
          retModel = line.split('|')[6].strip()
          retPoweredOn = line.split('|')[7].strip()
          retSerialNumber = line.split('|')[8].strip()
          retTag = line.split('|')[9].strip()
          retVersion = line.split('|')[10].strip()
        else:
	  Tag = line.strip()
	  retTag = Tag
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDescription = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Description,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Description|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retDeviceType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceType,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceType|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retManufacturer = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Manufacturer,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Manufacturer|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retModel = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Model,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Model|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retVersion = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag,Version from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag|Version$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retSerialNumber = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select SerialNumber,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^SerialNumber|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retEnabled = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Enabled,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Enabled|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retHotSwappable = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select HotSwappable,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^HotSwappable|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retPoweredOn = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select PoweredOn,Tag from Win32_OnBoardDevice where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^PoweredOn|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Tag ###
        print "        \"tag\": \"%s\"," % (formatCad(retTag))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Description ###
        print "        \"description\": \"%s\"," % (formatCad(retDescription))

        ### Device Type ###
        print "        \"deviceType\": \"%s\"," % (formatCad(getDeviceType(retDeviceType)))

        ### Manufacturer ###
        print "        \"manufacturer\": \"%s\"," % (formatCad(retManufacturer))

        ### Model ###
        print "        \"model\": \"%s\"," % (formatCad(retModel))

        ### Version ###
        print "        \"version\": \"%s\"," % (formatCad(retVersion))

        ### Serial Number ###
        print "        \"serialNumber\": \"%s\"," % (formatCad(retSerialNumber))

        ### Enabled ###
        print "        \"enabled\": \"%s\"," % (formatCad(retEnabled))

        ### Hot Swappable ###
        print "        \"hotSwappable\": \"%s\"," % (formatCad(retHotSwappable))

        ### Powered On ###
        print "        \"poweredOn\": \"%s\"" % (formatCad(retPoweredOn))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_Bus():

    # Getting Total Buses 
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_Bus') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"Bus\": ["
      # Getting Buses 
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,BusNum,BusType,Caption,ConfigManagerErrorCode,DeviceID from win32_Bus') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|BusNum|BusType|Caption|ConfigManagerErrorCode|DeviceID$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,BusNum,BusType,Caption,ConfigManagerErrorCode,DeviceID from win32_Bus') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|BusNum|BusType|Caption|ConfigManagerErrorCode|DeviceID$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select DeviceID from win32_Bus') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^DeviceID$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
	directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retAvailability = line.split('|')[0].strip()
          retBusNum = line.split('|')[1].strip()
          retBusType = line.split('|')[2].strip()
          retCaption = line.split('|')[3].strip()
          retConfigManagerErrorCode = line.split('|')[4].strip()
          retDeviceID = line.split('|')[5].strip()
        else:
          DeviceID = line.strip()
	  retDeviceID = DeviceID
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,DeviceID from Win32_Bus where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retBusType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BusType,DeviceID from Win32_Bus where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BusType|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retBusNum = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select BusNum,DeviceID from Win32_Bus where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^BusNum|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retAvailability = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Availability,DeviceID from Win32_Bus where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Availability|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retConfigManagerErrorCode = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConfigManagerErrorCode,DeviceID from Win32_Bus where DeviceID=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConfigManagerErrorCode|DeviceID$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, DeviceID, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Device ID ###
        print "        \"deviceID\": \"%s\"," % (formatCad(retDeviceID))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Bus Type ###
        print "        \"busType\": \"%s\"," % (formatCad(getBusType(retBusType)))

        ### Bus Num ###
        print "        \"busNum\": \"%s\"," % (formatCad(retBusNum))

        ### Availability ###
        print "        \"availability\": \"%s\"," % (formatCad(getAvailability(retAvailability)))

        ### Config Manager Error Code ###
        print "        \"configManagerErrorCode\": \"%s\"" % (formatCad(getConfigManagerErrorCode(retConfigManagerErrorCode)))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_PortConnector():

    # Getting Total Port Connectors 
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_PortConnector') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"PortConnector\": ["
      # Getting Port Connectors
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConnectorType,ExternalReferenceDesignator,InternalReferenceDesignator,PortType,Tag from win32_PortConnector') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConnectorType|ExternalReferenceDesignator|InternalReferenceDesignator|PortType|Tag$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConnectorType,ExternalReferenceDesignator,InternalReferenceDesignator,PortType,Tag from win32_PortConnector') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConnectorType|ExternalReferenceDesignator|InternalReferenceDesignator|PortType|Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
        directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Tag from win32_PortConnector') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
        directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retConnectorType = line.split('|')[0].strip()
          retExternalReferenceDesignator = line.split('|')[1].strip()
          retInternalReferenceDesignator = line.split('|')[2].strip()
          retPortType = line.split('|')[3].strip()
          retTag = line.split('|')[4].strip()
        else:
          Tag = line.strip()
          retTag = Tag
          retConnectorType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ConnectorType,Tag from Win32_PortConnector where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ConnectorType,Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retExternalReferenceDesignator = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select ExternalReferenceDesignator,Tag from Win32_PortConnector where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^ExternalReferenceDesignator|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retInternalReferenceDesignator = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select InternalReferenceDesignator,Tag from Win32_PortConnector where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^InternalReferenceDesignator|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retPortType = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select PortType,Tag from Win32_PortConnector where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^PortType|Tag$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Tag ###
        print "        \"tag\": \"%s\"," % (formatCad(retTag))

        ### Connector Type ###
	retConnectorType = retConnectorType.replace("(","").replace(")","")
        print "        \"connectorType\": \"%s\"," % (formatCad(getConnectorType(retConnectorType)))

        ### External Reference Designator ###
        print "        \"externalReferenceDesignator\": \"%s\"," % (formatCad(retExternalReferenceDesignator))

        ### Internal Reference Designator ###
        print "        \"internalReferenceDesignator\": \"%s\"," % (formatCad(retInternalReferenceDesignator))

        ### Port Type ###
        print "        \"portType\": \"%s\"" % (formatCad(getPortType(retPortType)))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


def show_Share():

    # Getting Total Shares
    total = int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from win32_Share') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read())
    if total > 0:
      print "    \"Share\": ["
      # Getting Shares
      count = 1

      if int(subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name,Path,Type from win32_Share') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name|Path|Type$'|grep -v '^$'|wc -l) || echo '0') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read()) > 0:

        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name,Path,Type from win32_Share') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name|Path|Type$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
        directLoop = "true"

      else:
        data = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name from win32_Share') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Tag$'|grep -v '^$') || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE)
        directLoop = "false"

      for line in data.stdout.readlines():

        if directLoop == "true":
          retCaption = line.split('|')[0].strip()
          retName = line.split('|')[1].strip()
          retPathShare = line.split('|')[2].strip()
          retTypeShare = line.split('|')[3].strip()
        else:
          Name = line.strip()
	  retName = Name
          retCaption = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Caption,Name from Win32_Share where Name=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Caption|Name$'|cut -d'|' -f1) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retPathShare = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,Path from Win32_Share where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|Path$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()
          retTypeShare = subprocess.Popen("((ret=$(%s -U %s%%%s //%s 'Select Name,Type from Win32_Share where Tag=\"%s\"') && echo \"${ret}\"|grep -iv 'failed NT status'|grep -iv '^CLASS:'|grep -iv '^Name|Type$'|cut -d'|' -f2) || echo '') 2>%s" % (path('wmic'), user, passwd, winNode, Tag, errorLog), shell=True, executable='%s' % (bash), stdout=subprocess.PIPE).stdout.read().strip()

        print "      {"

        ### Name ###
        print "        \"name\": \"%s\"," % (formatCad(retName))

        ### Caption ###
        print "        \"caption\": \"%s\"," % (formatCad(retCaption))

        ### Path ###
        print "        \"pathShare\": \"%s\"," % (formatCad(retPathShare))

	### Type ###
    	print "        \"typeShare\": \"%s\"" % (formatCad(getType(retTypeShare)))

        print "      }%s" % (("",",") [ count < total ])
        count += 1

      print "    ],"


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

    global winNode, user, passwd


    if len(sys.argv) > 1:

      args_file = sys.argv[1]
      args_data = file(args_file).read()

      arguments = shlex.split(args_data)

      for arg in arguments:

        if "=" in arg:

	  (key, value) = arg.split("=", 1)

          if key == "host":
            winNode = value

      if winNode:

        show_cabecera()

        if winCheck() == "y":
          user = winUser()
          passwd = winPasswd()

          print "    \"name\": \"%s\"," % (winNode)
          print "    \"shortName\": \"%s\"," % (winNode.split('.',1)[0])
          print "    \"user\": \"%s\"," % (user)
          print "    \"domain\": \"%s\"," % (winNode.split('.',1)[1] if len(winNode.split('.',1)) > 1 else "")


          show_ComputerSystem()
          show_OperatingSystem()
          show_SystemDriver()
          show_Service()
          show_SystemAccount()
          show_UserAccount()
          show_Group()
          show_GroupUser()
          show_BIOS()
          show_Processor()
          show_NetworkAdapter()
          show_NetworkAdapterConfiguration()
          show_NetworkAdapterSetting()
          show_PhysicalMemoryArray()
          show_PhysicalMemory()
          show_PhysicalMemoryLocation()
          show_DiskDrive()
          show_DiskPartition()
          show_DiskDriveToDiskPartition()
          show_LogicalDisk()
          show_LogicalDiskToPartition()
          show_BaseBoard()
          show_OnBoardDevice()
          show_Bus()
          show_PortConnector()
          show_Share()


        show_pie()


    else:
      print json.dumps({
        "failed" : True,
        "msg"    : "failed: no arguments"
      })
      sys.exit(1)




if __name__ == '__main__':
    main()

