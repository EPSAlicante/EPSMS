#!/usr/bin/python

import MySQLdb
import sys
import shlex
try:
  import json
except ImportError:
  import simplejson as json




def runQuery(query, connData):
    datos = connData
    listData = {}
    listCols = {}
    listTable = {}
    try:
      if query.upper().startswith('SELECT'):
        conn = MySQLdb.connect(*datos)    # Connect 
        cursor = conn.cursor()            # Create a cursor 
        cursor.execute(query)             # Execute the query 
        listData = cursor.fetchall()     # If SELECT, get rows 
        listCols = [col[0] for col in cursor.description] 
        cursor.close()                    
        conn.close()                      
        listTable = (listCols,) + listData

    except MySQLdb.Error, e:
      #print >> sys.stderr, "ERROR %d: %s. Query: %s" % (e.args[0],e.args[1],query)
      print json.dumps({
        "failed" : True,
        "msg"    : "ERROR %d: %s. Query: %s" % (e.args[0],e.args[1],query)
        })
      sys.exit(1)

    return listTable 


def show_data(connectData,label,query):
    data = runQuery("%s" % (query), connectData)

    print "    \"%s\": [" % (label) 

    # Check for data
    if len(data):
      cont = 1
      for row in data:
        if cont == 1:
          # Get columns names
          colNames = row
        else:
          print "      {"
          colIndex = 0
          for col in row:
            if colIndex+1 < len(row):
              print "        \"%s\": \"%s\"," % (colNames[colIndex],col)
            else:
              print "        \"%s\": \"%s\"" % (colNames[colIndex],col)
            colIndex += 1

          if cont < len(data):
            print "      },"
          else:
            print "      }"

        cont += 1

      retCode = 0

    else:
      retCode = 1

    print "    ],"

    return retCode


def show_cabecera():
    print "{"
    print "  \"ansible_facts\": {"


def show_pie():
    print "    \"changed\": false"
    print "  }"
    print "}" 


def main():

    # DB Configuration Files
    database = "inventory"
    user = "inventory"
    passwd = ""
    hostMysql = ""
    labelStr = ""
    queryStr = ""

    # read the argument string from the arguments file
    if len(sys.argv) > 1:
      args_file = sys.argv[1]
      args_data = file(args_file).read()

      arguments = shlex.split(args_data)

      for arg in arguments:

        if "=" in arg:

          (key, value) = arg.split("=", 1)

          if key == "hostMysql":
            hostMysql = value

          if key == "passwd":
            passwd = value

          if key == "label":
            labelStr = value

          if key == "query":
            queryStr = value
	    queryStr = queryStr.replace("'\"","'").replace("\"'","'")
	    if queryStr.startswith("'"):
	      queryStr = queryStr[1:]
	      if queryStr.endswith("'"):
		queryStr = queryStr[:-1]

      if passwd and hostMysql and labelStr and queryStr:

        # Connect Data
        connectData = [hostMysql, user, passwd, database]

        show_cabecera()
        ret = show_data(connectData,labelStr,queryStr)
        show_pie()

        sys.exit(ret)

      else:
        print json.dumps({
          "failed" : True,
          "msg"    : "failed getting arguments 'hostMysql', 'passwd', 'label' and 'query'"
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

