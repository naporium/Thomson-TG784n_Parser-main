# Thomson_TG784n_PARSER
  - __Description:__
  __Extract data from  Network Device "Thomson TG784n" (ALTICE MEO)__
  
  - __We can get:__
    - [x] __Device environment variables.__
    - [ ] __Thompson interfaces configuration: MacADDR, IPADDR, etc..__
    - [x] __DHCP Leases__
    - [x] __Connections.__
    - [x] __Information about Devices that have been connect, like IPADDRs, MACADDRs, hostnames..__
    - [x] __Thompson Logs.__
    - [ ] None
   
  - __Requirements:__
    - Python 3.6.8
    - Python Modules: 
       - pexpect==4.8.0
  
  - __License__: MIT
### How to Use:
    A or B:
    A) We can use the functions in file get_thomson.py and use them in conjuction with other tools like nslookup, etc.. 
    
    B) From the command line, run: python3 thomsonTG784.py -t dhcp-list 
    """  OUTPUT E.G.:
      OUTPUT - Connecting to Device ip:192.168.1.254 ... 
    OUTPUT - Sending command: 'dhcp server lease list' to device:192.168.1.254. 
    (venv) [User@NO MeoScrap]$ python get_thomson.py -t dhcp-list -o
    OUTPUT - Connecting to Device ip:192.168.1.254 ... 
    OUTPUT - Sending command: 'dhcp server lease list' to device:192.168.1.254. 
    ### 
    DHCP LIST 
    {'Lease': '0', 'Ip': '192.168.1.253', 'Pool': 'LAN_private', 'TTL': 'infinite', 'State': 'USED', 'Mac_addr': '56a:12:40:2d:f2:a3'}
    {'Lease': '1', 'Ip': '192.168.1.64', 'Pool': 'LAN_private', 'TTL': 'infinite', 'State': 'USED', 'Mac_addr': '4d:93:59:d1:91:f9'}
    ...
    {'Lease': '37', 'Ip': '192.168.1.120', 'Pool': 'LAN_private', 'TTL': 'infinite', 'State': 'USED', 'Mac_addr': '22:8c:9f:c1:12:ee'}
   
    # FOR HELP, flag -h
    python3 thomsonTG784.py -h
    
    # For flag -t, the list of possibilities
    # python3 thonsonTG784.py -t ["dhcp-list", "connections-list", "logs","arp-list", "env-variables", "host", "all"]
           
   
---
# Thomson TG784n MANUAL
####  Thomson TG784n (ALTICE MEO) - CLI available commands:
######(List is not exausted)


  __Usefull commands:__

 - ```help```             : Displays this help information
 - ```menu```             : Displays menu
 - ```?```                : Displays this help information
 - ```exit```             : Exits this shell.
 - ```..```               : Exits group selection.
 - ```saveall```          : Saves current configuration.
 -  ```ping```             : Send ICMP ECHO_REQUEST packets.
 - ```traceroute```       : Send ICMP/UDP packets to trace the ip path.

 [?] __Following command groups are available :__

 - [X] __contentsharing__
 - [X] __firewall__        
 - [X] __printersharing__  
 - [X] __pwr__             
 - [X] __service__         
 - [X] __connection__      
 - [X] __dhcp__           
 - [X] __dns__             
 - [X] __dyndns__          
 - [X] __eth__             
 - [X] __env__             
 - [X] __expr__            
 - [X] __hostmgr__         
 - [X] __interface__       
 - [X] __ip__              
 - [X] __ipqos__           
 - [X] __language__        
 - [X] __mobile__          
 - [X] __nat__             
 - [X] __pptp__            
 - [X] __sntp__            
 - [X] __software__        
 - [X] __ssh__             
 - [X] __syslog__          
 - [X] __system__          
 - [X] __upnp__            
 - [X] __vfs__             
 - [X] __wansensing__     
 - [X] __wireless__ 


__[GROUP ip] Following commands are available :__
 - ```ip iflist  ```         : Display all IP interfaces.
 - ```ip iplist ```          : Display all configured IP addresses.
 - ```ip rtlist  ```         : Display the routing table.
 - ```ip arplist ```         : Display the ARP cache.
 - ```ip nblist ```          : List the neighbours
 - ```ip nbset ```           : Add/modify a neighbour
 - ```ip nbdelete```         : Delete a neighbour
 - ```ip clearifstats```     : Flush IP interface statistics.
---

 __[GROUP nat] Following commands are available :__

  - ```nat iflist ```          : Display all interfaces.
  - ```natmaplist```          : Display address mappings.
  - ```nattmpllist```         : Display address mapping templates.
  - ```natconfig```           : Modify global NAT configuration.

---

 __[GROUP connection] Following commands are available :__
 
  - ```connection config```           : Modify global connection configuration.
  - ```connection timerconfig```      : Modify connection timeout handling.
  - ```connection info```             : Display all modules with some info.
  - ```connection list```             : Display the currently known connections. [USEFULL X]
  - ```connection describe```         : Describe the streams of a connection.
  - ```connection stats```            : Display connection and stream statistics.
  - ```connection reserve```          : Reserve connections.
  - ```connection release```          : Release connections.
  - ```connection applist```          : Display the available CONN/NAT application helpers.
  - ```connection appconfig```        : Modify a CONN/NAT application helper configuration
  - ```connection appinfo```          : Display CONN/NAT application specific info
  - ```connection bindlist```         : Display the CONN/NAT application helper/port bindings.
  - ```connection bind```             : Create a CONN/NAT application helper/port binding.
  - ```connection unbind```           : Delete a CONN/NAT application helper/port binding.

---

 __[GROUP syslog] Following commands are available :__

 - ```syslog config```           : Set/Display configuration
 - ```syslog ruleadd```          : Add a new rule to the syslog configuration.
 - ```syslog ruledelete```       : Delete a rule in the syslog configuration
 - ```syslog flush```            : Flushes syslog rules.
 - ```syslog list```             : List the current syslog configuration
    
    __[syslog msgbuf] Following commands are available :__

     - ```syslog msgbug show```             : Show messages in the syslog message buffer.
     - ```syslog msgbug send```             : Send messages to remote syslog server.
     - ```syslog msgbug flush```            : Flush all messages in syslog message buffer.

---

 __[GROUP env] Following commands are available :__

 - ```env get```              : Gets an environment variable.
 - ```env list```             : List all environment variables.

---
 __[GROUP dhcp] Following commands are available :__                                          

  - [X] __relay__  
  - [X] __relayv6__
  - [X] __rule__
  - [X] __server__
  - [X] __spoofing__ 
  - [X] __serverv6__ 
  
     __[dhcp server] Following commands are available :__
     
      - [X] __debug__  
      - [X] __lease__
      - [X] __option__
      - [X] __pool__ 
     
        __[dhcp server lease] Following commands are available :__
    
        - ```dhcp server lease add```              : Add a DHCP server lease
        - ```dhcp server lease delete```           : Delete a DHCP server lease
        - ```dhcp server lease flush```            : Flush all DHCP server leases
        - ```dhcp server lease list```             : List all DHCP server leases
    
        __[dhcp server pool] Following commands are available :__
        
        - ```dhcp server pool add```              : Add a DHCP server pool
        - ```dhcp server pool config```           : Configure a DHCP server pool
        - ```dhcp server pool delete```           : Delete a DHCP server pool
        - ```dhcp server pool rtadd```            : Add a route to the DHCP server pool
        - ```dhcp server pool rtdelete```         : Delete a route from the DHCP server pool
        - ```dhcp server pool optadd```           : Add an option instance to the DHCP server pool
        - ```dhcp server pool optdelete```        : Delete an option instance from the DHCP server pool
        - ```dhcp server pool ruleadd```          : Add a selection rule to the DHCP server pool
        - ```dhcp server pool ruledelete```       : Delete a selection rule from the DHCP server pool
        - ```dhcp server pool flush```            : Flush all DHCP server pools
        - ```dhcp server pool list```             : List all DHCP server pools
    
        __[dhcp server debug] Following commands are available :__
    
        - ```dhcp server debug traceconfig```      : Modify DHCP server trace configuration
        - ```dhcp server debug stats```            : Print DHCP server statistics
        - ```dhcp server debug clear```            : Clear DHCP server statistics
        
        __[dhcp server option] Following commands are available :__
    
        - ```dhcp server option tmpladd ```         : Add a DHCP server option template
        - ```dhcp server option tmpldelete```       : Delete a DHCP server option template
        - ```dhcp server option tmpllist```         : List all DHCP server option templates
        - ```dhcp server option instadd```          : Add a DHCP server option instance
        - ```dhcp server option instdelete```       : Delete a DHCP server option instance
        - ```dhcp server option instlist```         : List all DHCP server option instances
        - ```dhcp server option ruleadd```          : Add a selection rule to a DHCP server option instance
        - ```dhcp server option ruledelete```       : Delete a selection rule from a DHCP server option instance
        - ```dhcp server option flush```            : Flush all DHCP server option templates and instances
  
  __[GROUP software] Following commands are available :__ 
   - ```software version```          : Display the software version.
   - ```software upgrade```          : Force the gateway into LAN upgrade mode (Ctrl-BOOTP).
   - ```software deletepassive```    : Delete passive image.
   - ```software duplicate```        : Duplicate the active firmware (passive = active).
   
   __[GROUP system] Following commands are available :__
   - ```system settime```          : Set/Get date, time, timezone, daylight savings time, uptime.
   - ```system dst```              : Set daylight saving values
   - ```system reboot```           : Reboot the modem.
   - ```system reset```            : Reset to (factory or ISP) defaults: user specific settings will be cleared !
   - ```system config```           : Set or change system config parameters.
   - ```system timedreboot```      : Set or change editing mode timed reboot

 
 ```
 Trying 192.168.1.254...
 Connected to 192.168.1.254.
 Escape character is '^]'.
 Username : meo
 Password : ***
 
 ------------------------------------------------------------------------

                             ______  Thomson TG784n
                         ___/_____/\ 
                        /         /\\  10.2.1.L
                  _____/__       /  \\ 
                _/       /\_____/___ \  Copyright (c) 1999-2014, THOMSON
               //       /  \       /\ \
       _______//_______/    \     / _\/______ 
      /      / \       \    /    / /        /\
   __/      /   \       \  /    / /        / _\__ 
  / /      /     \_______\/    / /        / /   /\
 /_/______/___________________/ /________/ /___/  \ 
 \ \      \    ___________    \ \        \ \   \  /
  \_\      \  /          /\    \ \        \ \___\/
     \      \/          /  \    \ \        \  /
      \_____/          /    \    \ \________\/
           /__________/      \    \  /
           \   _____  \      /_____\/
            \ /    /\  \    /___\/
             /____/  \  \  /
             \    \  /___\/
              \____\/
 -------------------------------------------------------------------------
 {meo}=>
``` 
__Legend:__ 'THOMSON TG784n' CLI output, via Telnet Connection.

---

__Tools and Support:__
 - [Pycharm Community Edition](https://www.jetbrains.com/pycharm/) 
 - [CentOS](https://www.centos.org/)
 - Networking and Python Communities

__Sources:__
  - [whos-on-my-network](https://github.com/brentvollebregt/whos-on-my-network)
  - [geektuga.ddns.net](https://geektuga.ddns.net/gct/index.php/2017/07/17/comandos-technicolor-meo-vodafone/)

