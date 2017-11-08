#!/bin/bash
#
# A Nagios Plugin that checks if there is any program listening on specified
# TCP/UDP port.  
#
# Copyright (C) 2007 by Cedric Defortis <cedric@aiur.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

version=0.1
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4


progname=$(basename $0)

print_help()
{
    cat <<'EOF'
Usage: check_listen_tcp_udp.sh [-v] [-l <LISTENING_ADDRESS>] -p <PORT>
        [-P <tcp|udp|any|>=tcp]

A Nagios Plugin that checks if there is any program listening on specified
TCP/UDP port.  

Options:
      --help                print this help message
      --version             print program version
  -l, --listen=<ip_address> Specify the listening address. If unspecified no
                            verification is done on the listening address.
  -p, --port=<port>         The port number the service should listen to.
  -P, --protocol=<tcp|udp|any>  The protocol the service should used (By default,
                            the TCP protocol is used)
  -v, --verbose             verbose output

Examples:

To check that some daemon is listening on the port 80, with TCP protocol:
  $ ./check_listen_tcp_udp -p 80

To check that the server is able to answer to TCP _or_ UDP DNS requests:
  $ ./check_listen_tcp_udp -p 53 -P 

Report bugs to <cedric@aiur.fr>
EOF
} #

print_version()
{
    cat <<EOF
$progname $version
Copyright (C) 2009 Free Software Foundation, Inc.
This is free software.  You may redistribute copies of it under the terms of
the GNU General Public License <http://www.gnu.org/licenses/gpl.html>.
There is NO WARRANTY, to the extent permitted by law.

Written by Cedric Defortis
EOF
} #

SHORTOPTS="p:P:l:vVh"
LONGOPTS="port,protocol,listen,help,version,verbose"

if $(getopt -T >/dev/null 2>&1) ; [ $? = 4 ] ; then # New longopts getopt.
    OPTS=$(getopt -o $SHORTOPTS --long $LONGOPTS -n "$progname" -- "$@")
else # Old classic getopt.
    # Special handling for --help and --version on old getopt.
    case $1 in --help) print_help ; exit 0 ;; esac
    case $1 in --version) print_version ; exit 0 ;; esac
    OPTS=$(getopt $SHORTOPTS "$@")
fi

if [ $? -ne 0 ]; then
    print_help;
    exit 1
fi

eval set -- "$OPTS"

# Ensure that $lipo is an integer
declare -i lipo
lipo=0
listening_address="0.0.0.0"
proto="tcp"
verbose=false
while [ $# -gt 0 ]; do
    case $1 in
        -h|--help)
            print_help
            exit 0
            ;;
        -V|--version)
            print_version
            exit 0
            ;;
        -l|--listen)
            listening_address=$2
            shift 2
            ;;
        -p|--port)
            lipo=$2
            shift 2
            ;;
        -P|--protocol)
            proto=$2
            shift 2
            ;;
        -v|--verbose)
            verbose=true
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Internal Error: option processing error: $1" 1>&2
            exit 1
            ;;
    esac
done

MAX_PORT_NUM=65535
if test ! $lipo -eq $lipo 2> /dev/null
then
    echo "Invalid port number";
    exit 1;
fi;
if test $lipo -ge $MAX_PORT_NUM -o $lipo -le 0
then
    echo "You MUST specify a valid listening port with option: '--port=PORT'"
    exit 1;
fi;

if [ "`uname -s`" == "SunOS" ]
then
    NETSTAT_OPTS="-an -f inet -f inet6"
else
    NETSTAT_OPTS="-ln"
fi;

case $proto in
    "udp")
    proto_code="udp"
    if [ "`uname -s`" == "SunOS" ]
    then
        NETSTAT_OPTS="${NETSTAT_OPTS} -P udp|grep -i 'Idle'"
    else
        NETSTAT_OPTS="${NETSTAT_OPTS}u"
    fi;
    ;;
    "any")
    proto_code="(tcp|udp)"
    if [ "`uname -s`" == "SunOS" ]
    then
        NETSTAT_OPTS="${NETSTAT_OPTS}tu"
    else
        NETSTAT_OPTS="${NETSTAT_OPTS}tu"
    fi;
    ;;
    *)
    proto_code="tcp"
    if [ "`uname -s`" == "SunOS" ]
    then
        NETSTAT_OPTS="${NETSTAT_OPTS} -P tcp|grep -i 'LISTEN'"
    else
        NETSTAT_OPTS="${NETSTAT_OPTS}t"
    fi;
    ;;
esac;



NETSTAT="netstat"
#NET_SED='sed -nr -e "s/^([a-zA-Z0-9]+) [0-9 ]+ ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+|[:0-9]+) +.*/\1,\2/p"'
if [ "`uname -s`" == "SunOS" ]
then
    NET_SED="tr '\t' ' '|tr -s ' '|gsed \"s/^ */$proto_code,/\"|gsed 's/\*\./0\.0\.0\.0:/'|gsed 's/\./:/4'|cut -d' ' -f1"
else
    NET_SED='sed -nr -e "s/^([a-zA-Z0-9]+) [0-9 ]+ ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+|[:0-9]+|.*:[0-9]+) +.*/\1,\2/p"'
fi;
#NET_GREP="grep \":$lipo$\" | grep -E \"$proto_code\""
NET_GREP="grep \":$lipo$\""

if [[ $listening_address != "0.0.0.0" ]]
then
    NET_GREP="${NET_GREP} | grep \"$listening_address\""
fi;

cmd="$NETSTAT ${NETSTAT_OPTS} | $NET_SED | $NET_GREP"

if $verbose
then
    echo $cmd
    eval $cmd
else
    eval $cmd 2>&1 > /dev/null
fi;


# On a eu un resultat:
if [[ $? -eq 0 ]]
then
    res=`eval $cmd`
    res_proto=${res%,*}
    res_listen=${res#*,}
    #echo "OK -  Listening on ${res_listen} (protocol: $res_proto)"
    if [[ $listening_address == "0.0.0.0" ]]
    then
        echo "OK -  Listening on :${lipo} (protocol: $proto)"
    else
	echo "OK -  Listening on ${listening_address}:${lipo} (protocol: $proto)"
    fi;
    exit $STATE_OK;
else
    if [[ $listening_address == "0.0.0.0" ]]
    then
    	echo "CRITICAL - No service listening on :${lipo} (protocol: $proto) "
    else
	echo "CRITICAL - No service listening on ${listening_address}:${lipo} (protocol: $proto) "
    fi;
    exit $STATE_CRITICAL;
fi;

