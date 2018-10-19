# EPS Monitoring System

## Table of contents
- [Introduction](#introduction)
- [Infrastructure provided](#infrastructure-provided)
- [Installation & configuration](#installation-and-configuration)
- [Internal Working](#internal-working)
- [Information collected](#information-collected)
- [Copyright & License](#copyright-and-license)


## Introduction

Every System Administrator wants to have a 'monitoring system' to know exactly the state of his system, getting alerts of any server's problem (software or hardware), knowing server's performance, and collecting the most detailed inventory as possible (hardware and software).

Some of them (sysadmins) have all these requirements done, so they don't need this software (EPS MS), but  maybe 'EPS MS' let them a better tool to monitor their systems.

Most of them have got just one of these requirements (as problem's alerts or performance) because they have no time to invest in monitoring. In this case, 'EPS MS' will complete their 'monitoring system'.

For the other (who don't have any monitoring system) 'EPS MS' will be perfect because they just have to invest a very short time to install and configure a complete, automatic and free monitoring system.

Live Demo available at [**https://epsms.eps.ua.es**](https://epsms.eps.ua.es) (user: 'epsms', password: 'epsms'). Read only user 'epsms' to watch hardware/software/security information collected from a real network in real-time.


## Infrastructure provided

Basically, 'EPS MS' **provide us**:

 - An events & alerts monitoring system as [**Nagios**](https://www.nagios.org) to analize host's and service's status.
 - A performance monitoring system as [**Munin**](http://munin-monitoring.org) to analize host's performance graphically.
 - An **own monitoring system** (made with [**Ansible**](https://www.ansible.com)) to collect host's hardware, software and security information, and install & configure the other monitoring systems: Nagios, Munin, Openvas...
 - A [**Mysql**](http://www.mysql.com) database to store collected information (current and historical).
 - A [**Dokuwiki**](https://www.dokuwiki.org) server to show collected information.
 - A [**PhpMyAdmin**](https://www.phpmyadmin.net) server to manage graphically data stored in Mysql database.
 - Some **Web applications** (made with [**PHP**](https://php.net) and [**angularjs**](https://angularjs.org)) to analize information in a customized way.
 - A [**Rest**](https://en.wikipedia.org/wiki/Representational_state_transfer) API to access data (used by angularjs application)
 - An [**InfluxDB**](https://www.influxdata.com) database to store time-series data from munin and nagios.
 -  A full-featured interactive dashboard ([**Grafana**](http://grafana.org)) to analyze influxdb information. 
 - A security monitoring system as [**Openvas**](http://www.openvas.org) to scan host's vulnerabilites.

 
## Installation and configuration

OK, I want to try this software. But, how much time do I have to spend? Just a few minutes. These are the steps to **install and configure**:

1. Download ***'epsms.tgz'*** file of **install** directory and decompress it on a CentOS 6 host (this will be our 'Control Server'). 

2. Execute **'install.py'** script to install 'EPS MS'.

3. Execute **'/etc/ansible/menu.py'** showing the 'Control Menu'.

4. Select **option '1'** in 'Control Menu' to deploy 'EPS MS' infrastructure. This option will ask some questions about configuration as:

	- User to connect to Linux/Unix hosts (connection by SSH without password, using public keys and sudo)
	- User/password to connect to Windows hosts (connection by WMI 'Windows Management Instrumentation')
	- IP addresses of Nagios, Munin, Mysql, Web (Dokuwiki, PhpMyAdmin and web Apps), Grafana and Openvas servers to install software (they have to be CentOS 6)
	- Networks to monitor, collecting information of hosts inside them
	- Admin password of Servers: Nagios, Munin, Mysql, Web (Dokuwiki, PhpMyAdmin and web Apps), Grafana and Openvas
	- IP addresses of administrators hosts (access permission to servers)
	- Frequencies to check servers (server's software installation and a correct configuration) and hosts (client's software installation, correct configuration and data collecting of hardware, software and security information from them)

5. After infrastructure's deployment , 'EPS MS' starts **collecting information** from hosts indefinitely. Results can be analyzed from 'https://hostnameWebServer' with links to Nagios, Munin, Wiki, Mysql (phpMyAdmin), web (PHP & AngularJS) Apps, InfluxDB, Grafana, Openvas and Help.


## Internal working

But, **how does it work** inside? These are the steps 'EPS MS' does after configuration:

(A.1) Infrastructure deployment: **Installation and configuration of servers software**

(A.2) Infrastructure deployment: **Network scanning** to discover 'nodes' (hosts accessed by 'EPS MS') and 'outsiders' (hosts not accessed)

(A.3) Nodes deployment: **Installation and configuration of nodes software**

(B.1) Data collection: **Getting information from nodes**

(B.2) Data collection: **Updating servers with nodes information**

(C.1) Security Assessment: **Vulnerabilities scanning** of nodes and outsiders (with Openvas)

(C.2) Security assesment: **Updating servers with scanning results**

(D) **Analyzing results** stored in servers


## Information collected

What kind of **information** do we'll get?

| Type | Information |
|:--------:|---------------------------------|
| **Hardware (Linux/Unix)** | **System**: Architecture, Manufacturer, Product Name, Version, Serial Number, UUID, Wake-Up Type. **Processor**: Processor Type, Processor Count, Cores per Processor, Threads per Core, Total Virtual CPUs, Sockets. For Every Socket: Designation, Type, Family, Vendor, Signature, ID, Version, Voltage, External Clock, Maximum Speed, Current Speed, Status, L1 Cache Handle, L3 Cache Handle, L3 Cache Handle, Serial Number.	**Memory**: Total Memory, Maximum Memory Module Size, Number of Arrays, Number of Slots, Arrays.	**For Every Array**: Handle, Location, Use, Error Correction Type, Maximum Capacity, Number of Devices, Slots.	**For Every Slot**: Handle, Locator, Array, Bank Locator, Size, Speed, Type.	**BIOS**: Vendor, Release Date, Version, ROM Size, Runtime Size, Characteristics.	**For Every Characteristic**: Characteristic, Value.	**Baseboard**: Handle, Manufacturer, Product Name, Version, Serial Number, Devices.	**For Every Device**: Handle, Type, Description, Enabled.	**Chassis**: Manufacturer, Type, Version, Serial Number.	**Devices**: Name, Model, Scheduler, Size, Vendor, Partitions.	**For Every Partition**: Name, Size.	**Network Interfaces**: Name, Address, DNS Name, Network, NetMask, MAC, Type, Module, Active.	**Cache Memory**: Handle, Socket Designation, Level, Enabled, Mode, Location, Installed Size, Maximum Size.	**Connectors**: Handle, Internal Reference Designator, Internal Connector Type, External Reference Designator, External Connector Type, Port Type. |
| **Hardware (Windows)** | **System**: Description, System Type, PC System Type, Manufacturer, Model, Infrared Supported, Wake-Up Type.	**Processor**: Number of Processors, Number of Logical Processors, Sockets.	**For Every Socket**: Device ID, Name, Caption, Config Manager Error Code, CPU Status, Current Clock Speed, Data Width, Family, L2 Cache Size, L2 Cache Speed, L3 Cache Size, L3 Cache Speed, Manufacturer, Maximum Clock Speed, Number of Cores, Number of Logical Processors, Processor ID, Processor Type.	**Memory**: Total Physical Memory, Arrays.	**For Every Array**: Tag, Caption, Hot Swappable, Location, Maximum Capacity, Memory of Devices, Memory Error Correction, Memory Use, Slots.	**For Every Slot**: Tag, Caption, Capacity, Data Width, Total Width, Device Locator, Form Factor, Hot Swappable, Manufacturer, Memory Type, Position in Row, Speed.	**BIOS**: Name, Caption, Software Element ID, Software Element State, Target Operating System, Version, Buid Number, Code Set, Current Language, Identification Code, Language Edition, Manufacturer, Primary BIOS, Characteristics.	**For Every Characteristic**: Char Code, Description.	**Baseboard**: Tag, Caption, Manufacturer,  Product, Model, Version, Serial Number, Hosting Board, Hot Swappable, Powered On, Devices.	**For Every Device**: Tag, Caption, Description, Device Type, Manufacturer, Model, Version, Serial Number, Enabled, Hot Swappable, Powered On.	**Devices**: Device ID, Caption, Disk Index, Interface Type, Model ,Size, Availability, Total Heads, Total Cylinders, Tracks per Cylinder, Total Tracks, Sectors per Track, Total Sectors, Bytes per Sector, Default Block Size, Media Type, Partition ID, Config Manager Error Code, Serial Number, SCSI Bus, SCSI Port, SCSI Target ID, SCSI Logical Unit, Partitions.	**For Every Partition**: Device ID, Caption, Disk Index, Partition Index, Partition Type, Size, Block Size, Number of Blocks, Access, Availability, Bootable, Boot Partition, Primary Partition.	**Network Interfaces**: Device ID, Name, Adapter Type, Manufacturer, MAC Address, Availability, Config Manager Error Code, Adapter Index, Net Connection ID, Net Connection Status, Service Name, Settings.	**For Every Setting**: Net Index, Description, IP Address, IP Subnet, Default IP Gateway, Default TOS, Default TTL, DHCP Enabled, DHCP Server, DNS Domain, DNS Domain Suffix Search Order, DNS Enabled for WINS Resolution, DNS Domain Search Order, IGMP Level, MAC Address, WINS Enable LMHosts Lookup, WINS Primary Server, WINS Secondary Server.	**Connectors**: Tag, Connector Type, External Reference Designator, Internal Reference Designator, Port Type.	**Buses**: Device ID, Caption, Bus Type, Bus Num, Availability, Config Manager Error Code. |
| **Software (Linux/Unix)** | **IP**: Name, IP.	**Distribution**: Distribution, Version.	**Kernel**: Kernel.	**Modules**: Name, File Name, Author, Description, License, Version, Version Magic, Source Version.	**Domain**: Domain.	**DNS Resolver**: Domain, NameServer 1, NameServer 2, NameServer 3, Options.	**For Every Option**: Option.	**'/etc/hosts' File**: Rules.	**Routes**: Destination, Gateway, Mask, Flags, Interfaces.	**Swap Memory**: Swap.	**Virtualization**: Virtualization Role, Virtualization Type.	**FileSystems**: Name, Type, Mount, Options, Size |
| **Software (Windows)** | **IP**: Name, IP.	**Domain**: Domain.	**Operating System**: OS Name, OS Description, Boot Device, Service Pack Version, OS Architecture, OS Type, Product Type, Version, Serial Number, Country, Language, PAE Enabled, Manufacturer, Current Time Zone, Encryption Level, Number of Licensed Users, Operating System SKU, Organization, Registered User, Maximum Number of Processes, System Device, System Drive, Windows Directory, System Directory, Total Visible Memory Size, Total Swap Space Size, Total Virtual Memory Size, Distributed.	**Logical Devices**: Device ID, Caption, Drive Type, File System, Size, Access, Availability, Compressed, Config Manager Error Code, Supports Disk Quotas, Quotas Disabled, Supports File Based Compression, Volume Name, Volume Serial Number, Partitions.	**For Every Partition**: Partition Device ID. |
| **Security (Linux/Unix)** | **Servers**: Name, IP, Node.	**TCP/UDP Ports (inside Scan)**: Protocol, Port, IP4, Bind IP4, IP6, Bind IP6, Process.	**TCP Ports (outside scan)**: Protocol, Port.	**Packages**: Name, Version, Size.	**Executables**: Name, Package, File Size, File User, File Group, File Permissions, Signature.	**Executables (with no package)**: Name, File Size, File User, File Group, File Permissions.	**Executables (setUID)**: Name, Package, File Size, File User, File Group, File Permissions.	**Executables (setGID)**: Name, Package, File Size, File User, File Group, File Permissions.	**Users**: Name, UID, GID, Password Type, Last Change, Description, Home, Shell.	**Groups**: Name, GID, Users.	**For Every User*: User.	**Sudo**: Defaults, User Alias, Cmnd Alias, Runas Alias, Rules Alias.	**For Every Default**: Rule.	**For Every User Alias**: Rule.	**For Every Cmnd Alias**: Rule.	**For Every Runas Alias**: Rule.	**For Every Rules Alias**: Rule.	**Crontab**: User, Minute, Hour, Day, Month, DayWeek, Command.	**IPTables**: IPTable, Chain, Policy, Rules.	**For Every Rule**: Rule.	**TCP Wrappers**: Type, Service, Hosts.	**For Every Host**: Host.	**PAM Access**: Modules, Rules.	**For Every Module**: Module.	**For Every Rule**: Rule.	**Openvas**: IP, Start Scan, CVSS, Total High, Total Medium, Total Low, Total Log, Total False Positive. |
| **Security (Windows)** | **Servers**: Name, IP, Node.	**TCP/UDP Ports (inside Scan)**: Protocol, Port, IP4, Bind IP4, IP6, Bind IP6, Process.	**TCP Ports (outside scan)**: Protocol, Port.	**Users**: Domain, Name, System Account, Caption, Account Type, Disabled, Full Name, Local Account, Lockout, Password Changeable, Password Expires, Password RequiredSID, SID Type.	**Groups**: Name, GID, Users.	**For Every User**: User.	**Drivers**: Name, Caption, Error Control, Path Name, Service Type, Start Mode, State, Tag ID.	**Services**: Name, Caption, Error Control, Path Name, Process ID, Start Mode, State, Tag ID.	**Shares**: Name, Caption, Path Share, Type Share.	**Openvas**: IP, Start Scan, CVSS, Total High, Total Medium, Total Low, Total Log, Total False Positive. |


## Copyright and License

The source code packaged with this file is Free Software, Copyright (C) 2016 by Unidad de Laboratorios, Escuela Politecnica Superior, Universidad de Alicante :: `<`epsms at eps.ua.es`>`.
It's licensed under the AFFERO GENERAL PUBLIC LICENSE unless stated otherwise. You can get copies of the licenses here: http://www.affero.org/oagpl.html AFFERO GENERAL PUBLIC LICENSE is also included in the file called "LICENSE".

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
