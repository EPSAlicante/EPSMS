# EPS INVENTORY SYSTEM
System is able to get information about software, hardware, (even about security) from selected hosts (in some selected networks). This information will be saved in some servers in different formats (including a mysql database, a dokuwiki server and a PHP application), to be accesed by administrators (with user/password security) from some selected IPs.
Furthermore, it will install and configure a monitorization system (Nagios) and a performance system (Munin).

This infrastructure will be deployed after a simple configuration (some variables to define) and will be updated forever with no human interaction. Administrator just have to install software (really simple), and configure it to deploy infrastructure. Configuration consists on a number of questions to define parameters needed for deployment, security, maintenance and non interaction updating.

After configuration, system will scan working networks (defined at configuration) to detect hosts. For every host, system will try to access inside and clasify them as 'nodes', 'winNodes' or 'outsiders'. Linux/Unix accesible hosts will be clasified as 'nodes', Windows accesible hosts will be clasified as 'winNodes', and not accesible hosts will be 'outsiders'.


There are four stages before using System:


## (1) Configuration

Execute menu '/etc/ansible/menu.py' and select option 1 'Configure System'. We have to answer series of questions about system. These answers are basic to deployment. At the end, deployment starts.

See Configuration doc for details.


## (2) Deployment

When System has been configured, system automatically will start installation and configuration of infrastructure, required servers and tools to start data collection, monitorization and results checking.

Servers and tools installed and configured at deployment are:

* Control server with Ansible and all required tools to deply the rest of infrastructure, scanning working subnets and system management.

* Mysql server configured with inventory database to save information collected from hosts.

* Nagios server to check hosts: nodes (monitoring load, disk free space and TCP and UDP open ports) and outsiders (monitoring TCP open ports).

* Munin server with performance graphics about main hosts' features

* Wiki server with data inventory collected from hosts (nodes and outsiders).

* Openvas server to check vulnerabilities of hosts and generate reports (html, pdf, txt and xml formats) in Wiki server. It also has a Web server in port 9392 to manage task and watch reports.

* Web server with a PHP Application for customize querys and management from data collected, and PHPMyAdmin to query data and manage database.

All these tasks are repeated frequently (defined at configuration time) to verify that all servers are installed and configured correctly. If something has changed, Control server will reinstall and reconfigured again.


## (3) Data collection

When infrastructure is deployed (all server and nodes have their software installed and configured), system is ready to start data collection stage.

This stage consists of some tasks that Control server will repeat frequently (defined at configuration time too):

* It starts a scanning of working subnets (defined at configuration time) to detect hosts and classify them as nodes (if control server can access host with defined user) or outsiders (if control server can't access).

* When scanning is done Control server will prepare an inventory of nodes with open TCP open ports of every host (scanning will give us a list of TCP open ports for every node). An inventory of outsiders with TCP open ports will be made too.

* Control server will save this information (nodes, outsiders and their TCP ports) is saved on 'inventory' database.

* Control server will generate the main wiki page 'servers' with information about nodes and outsiders detected, a page for every host with their TCP ports, and reports of vulnerabilities checked.

* Control server will configure Nagios server with nodes and outsider as hosts, checking TCP open ports.

* Control server will connect to nodes to install and configure required software to monitor (Nagios NRPE), get graphics performance (Munin node) and some other tools to recover hardware and software information.

* Collection of hardware and software information from nodes.

* Control server will save all data collected on 'inventory' database.

* Control server will generate wiki pages with collected information and data from 'inventory' database (pages with historic information).

* Control server will configure Nagios server with internal checks (with Nagios NRPE) as load, disk free space and TCP & UDP open ports.

* Control server will configure Munin server with nodes.

* Control server will check vulnerabilities of all hosts (outsiders, nodes and winNodes) with Openvas software. It generates a report (in different format: html, pdf, txt and xml) for every host (this information will be available in wiki pages and stored on 'inventory' database).


## (4) Monitorization & results checking

When system has configured all server and nodes, and has collected all information about nodes and outsiders, administrators are ready to use it. Obviosly, deployment and data collection stages will repeat forever to maintain infrastructure ready and data updated.

Administrators will use these tools connecting to servers (Nagios server for monitorizarion of hosts, Munin server to get graphical performance of nodes, Wiki server to get information about hosts and Web server to manage database and doing simple queries with PHP application) just from a list of selected IPs (defined at configuration time). They will connect using user 'admin' with password defined at configuration time.

### Nagios server

Connecting to Nagios server permit monitoring hosts, open TCP & UDP ports (just TCP for outsiders), check load and space free of root disk for nodes, and check system errors. We can see availability of hosts and services, receiving alerts about any problems. It's an essential tool for Administrators to be alerted immediately about problems and repairing them as soon as possible. Obvously, Administrator can increase availability of hosts and services reducing time discovering and resolving problems.

Of course, administrator can modify Nagios to add new checks for nodes, increasing capacities for monitorization (see FAQ document)

Administrator have to connect to URL: http://NagiosServer/nagios

### Munin server

Connecting to Munin server permit watch graphical performance of nodes main features as: performance I/O of disks, free space (%) of disks, network interfaces bandwith, number of processes, CPU, load system, users logged, memory, Swap, etc. It's very useful tool to monitor performance of hosts after an error, trying to discover the origin of problem.

Munin server will save information about performance for a year, and user can select range time even zooming in and out to increase or decrease parformance graphical range.

Of course, administrator can modify Munin to add new graphs for nodes, increasing capacities to monitor performance (see FAQ document)

Administrator have to connect to URL: http://MuninServer/munin

### Openvas server (web server in port 9392)

Connecting to Openvas server permit manage Openvas: targets, tasks, updates... generate and watch reports of scanned hosts.

Vulnerabilities checks and are made by Control server automatically, and reports are created and copied to Wiki server. But with Openvas server manually checks can be created.

### Wiki server (inventory)

Connecting to Wiki server permit get hardware & software information about hosts (just availability, TCP open ports and vulnerabilities for outsiders).

Main page show a list of hosts: nodes, winNodes (windows nodes) and outsiders. We can ordering columns clicking on top of them. We can filter type of hosts (nodes, winNodes and outsiders) clicking in selected host type. We have possibility to see changes on availability of hosts (discovering down time of them) clicking on 'Last 100 changes' column. Clicking on hostname column we'll see all information about it (host's page). We can also watch vulnerabilities scanning of hosts, and a link to Nagios and Munin servers page.

In host's page we'll see hardware, software and security information (for nodes and winNodes). Information about nodes and winNodes is similar but not exactly the same.

We'll have this information about nodes (linux/Unix nodes):

##### Hardware

+ System -> Arquitecture, Manufacturer, Product Name, Version, Serial Number, UUID and Wake-Up Type

+ Processor -> Processor Type, Count, Cores per Processor, Threads per Core, Total Virtual CPU's, and list of sockets with information about them: Type, Family, Vendor, Signature, ID, Version, Voltage, External Clock, Max Speed, Current Speed, Status, Upgrade, L1 Cache Handle, L2 Cache Handle, L3 Cache Handle and Serial Number.

+ Memory -> Total Memory, Maximum Memory Module Size, Number Of Arrays, Number Of Slots, list of Memory Arrays with information about them: Handle, Location, Use, Error Correction Type, Maximum Capacity and Number of Devices, and list of Memory Slots with information about them: Handle, Locator, Array, Bank Locator, Size, Speed and Type.

+ Bios -> Vendor, Release Date, Version, ROM Size, Runtime Size and list of Characteristics supported.

+ Baseboard -> Handle, Manufacturer, Product Name, Versionm, Serial Number and a list of Devices with information about them: Handle, Type, Description and Enabled.

+ Chassis -> Manufacturer, Type, Version and Serial Number.

+ Devices -> List of devices with information about them: Model, Host, Scheduler, Size and Vendor.

+ Interfaces -> List of Network Interfaces with information about them: Name, Adress, DNS Name, Network, Netmask, MAC Address, Type, Module and Active.

+ Cache Memory -> List of Cache Memories with information about them: Name, Handle, Level, Enabled, Operational Mode, Location, Installed Size and Maximum Size.

+ Connectors -> List of Connectors with information about them: Handle, Internal Reference Designator, Internal Connector Type, External Reference Designator, External Connector Type and Port Type.

+ Slots -> List of Slots with information about them: Handle, Designation, Type SlotType, Type SlotBusWidth, Current Usage and Slot ID.

##### Software

+ Distribution

+ Version

+ Kernel

+ Modules -> List of modules with information about them: Name, Filename, Author, Description, License, Version, Version Magic, Source Version and Dependencies.
Se
+ Domain

+ Resolver (configuration of '/etc/resolv.conf' file) -> Domain, Search and Nameservers.

+ Hosts (configuration of '/etc/hosts' file) -> List of alias declared.

+ Network Routes -> List of network routes configured with information about them: Destination, Gateway, Mask, Flags and Interface.

+ Swap

+ Virtualization -> Kind of virtualization and type (host or guest).

+ Filesystems -> List of filesystems with information about them: Name, Type, Mount Point, Options and Size.

##### Security

+ TCP & UDP Ports

+ TCP & UDP Listennig Ports -> List of TCP & UDP Ports (internal scan) with information about them: Protocol, Port, IP4, IP6 and Process.

+ Last Found (100) -> Historical list of last 100 Ports found with information about them: Protocol, Port, IP4, IP6, Process, Since (when appeared) and Until (when disapeared).

+ TCP Listennig Ports -> List of TCP Port (external scan).

+ Packages

+ Package Manager

+ List of packages installed with information about them: Name, Version and Size

+ Last packages installed (100) -> Historcal list of last 100 packages installed with information about them: Name, Version, Size, Since (when was installed) and Until (when was removed).

+ Executables

+ Exes with no package -> List of executables without package and information about them: Name, Size, User, Group, Permission and Since (when appeared).

+ Exes with SetUID -> List of executables with setUID attribute and information about them: Name, Size, User, Group, Permission and Since (when appeared).

+ Exes with SetGID -> List of executables with setGID attribute and information about them: Name, Size, User, Group, Permission and Since (when appeared).

+ Exes modified -> List of executables with signature modified (every executable is signed every time system get information about it) with information about them: Name, Package and Versions (number of different changes).

+ Exes with attributed modified -> List of executables with any attribute modified (Size, User, Group or Permission) with information about them: Name, Package, Size and Versions (number of different changes).

+ Last Found (100) -> Historical list of last 100 executables found with information about them: Name, Size, User, Group, Permission, Since (when appeared) and Until (when disappeared).

+ User & Groups -> List of users with information about them: Name, UID, GID, Password Type (blocked, crypted, etc.), Last Change, Description, Home and Shell, and List of Groups with information about them: Name, GID and list of users.

+ Sudo (configuration of '/etc/sudoers' file) -> List of Defaults options, userAlias, runasAlias, hostAlias, cmndAlias and User Specifications.

+ Crontab -> List of jobs on crontab with information about them: User, Minute, Hour, Day, Month, Day Week and Command.

+ IPTables -> List of different Tables and Chains.

+ TCP Wrappers (configuration of '/etc/hosts.deny' and '/etc/hosts.allow' files) -> List of deny and allow rules with information about them: Service and List of Hosts.

+ PAM Access (configuration of '/etc/security/access.conf' file) -> List of PAM modules and List of Rules of every module.

#### We'll have this information about winNodes (windows nodes):

##### Hardware

+ System -> Description, System Type, PC System Type, Manufacturer, Model, Infrared Supported and Wake-Up Type.

+ Processor -> List of processors with information about them: Name, Caption, Family, Manufacturer, Processor Type, Current Clock Speed, Max Clock Speed, Number of Cores, Number of Logical Processors, Data Width, L2 Cache Size, L2 Cache Speed, L3 Cache Size, L3 Cache Speed and Processor ID.

+ Memory -> Total Memory, List of Arrays with information about them: Capion, Location, Use, Error Correction Type, Maximum Capacity, Number of Devices and Hot Swappable, and List of Slots with information about them: Caption, Device Locator, Position in Row, Form Factor, Capacity, Data Width, Total Witdh, Speed, Type, Manufacturer and Hot Swappable.

+ Bios -> Name, Caption, Version, Manufacturer, Release Date, Serial Number, Build Number, Identification Code, Current Language, Language Edition, Primary Bios and a list of Characteristics supported.

+ Baseboard -> Caption, Manufacturer, Product, Model, Version, Serial Number, Hosting Board, Hot Swappable, Powered On and a list of Devices on Board with information about them: Description, Type, Manufacturer, Model, Version, Serial Number, Enabled, HotSwappable, Powered On.

+ Devices -> List of Devices with information about them: Caption, Media Type, Interface Type, SCSI Bus, SCSI Port, SCSI Target ID, SCSI Logical Unit, Model, Size, Total Heads, Total Cylinders, Tracks per Cylinder, Total Tracks, Sectors per Track, Total Sectors, Bytes per Sector, Default Block Size, Serial Number, Availability, Config Manager Error, Partitions and a list of Partitions with information about them: Partition Disk, Partition ID, Type, Caption, Block Size, Number of Blocks, Size, Access, Availability, Primary Partition, Bootable and Boot Partition.

+ Network Adapters -> List of Network Adapters with information about them: Name, Type, MAC Address, Manufacturer, Connection Status and Config Manager Error.

+ Port Connectors -> List of Port Connectors with information about them: Connector ID, Connector Type, Port Type, External Reference Designator and Internal Reference Designator.

+ Buses -> List of Buses with information about them: Bus ID, Caption, Bus Num, Bus Type, Availability and Config Manager Error.

##### Software

+ Operating System -> Name, Description, Boot Device, CSD Version, Service Pack Version, OS Architecture, OS Type, Product Type, Version, Serial Number, Country Code, OS Language, PAE Enabled, Manufacturer, Current Time Zone, Encryption Level, Number of Licensed Users, Operating System SKU, Organization, Registered User, Max Number of Processes, System Device, System Drive, Windows Directory, System Directory, Total Visible Memory Size, Total Swap Space Size, Total Virtual Memory Size and Distributed.

+ Version

+ Logical Devices -> List of Logical Devices with information about them: Caption, Drive Type, File System, Volume Name, Size, Access, Support File Based Compression, Compressed, Supports Disk Quotas, Quotas Disabled, Volume Serial Number, Availability and Config Manager Error.

+ Logical Network Adapters -> List of Logical Network Adapters with information about them: Adapter ID, Description, MAC Address, IP Address, IP Subnet, Default IP Gateway, Default TOS, Default TTL, DHCP Enabled, DHCP Server, DNS Domain, DNS Domain Suffix Search Order, DNS Domain Search Order, IGMP Level, WINS Enable LMHosts Lookup, WINS Primary Server and WINS Secondary Server.

+ System Drive

+ Windows Directory

+ OS Domain -> Domain, Part of Domain, Workgroup and Domain Role.

+ Domain Role

+ OS Language

##### Security

+ TCP Listennig Ports -> List of TCP Port (external scan).

+ User & Groups -> List of System Accounts with information about them: Name, Local Account, SID Type and SID, list of User Accounts with information about them: Name, Local Account, SID Type, SID, Account Type, Disabled, Lockout, Full Name, Password Changeable, Password Expires and Password Required, and list of Groups with information about them: Name, Local Group, SID Type and SID.

+ Drivers -> List of Drivers with information about them: Name, Caption, Path Name, Service Type, Start Mode, State and Error Control.

+ Services -> List of Services with information about them: Name, Caption, Path Name, Process ID, Start Mode, State and Error Control.

+ Shares -> List of Network Shares with information about them: Name, Caption, Path and Type.


Of course, administrator can modify system to add new pages or modify them, even collect new information and create pages to show it (see FAQ document)

Administrator have to connect to URL: http://wikiServer/wiki

### Web server

Connecting to Web server permit manage database with PhpMyAdmin software. We'll need mysql user ('admin' or 'inventory') and password (defined at configuration time).

Administrator have to connect to URL: http://webServer/phpmyadmin

We can watch a few examples of PHP application and take it as template to made a customized PHP appplication.

Administrator have to connect to URL: http://webServer/web

