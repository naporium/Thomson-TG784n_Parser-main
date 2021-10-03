#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from json import dumps, dump
from datetime import datetime
import sys

import argparse
import re
from validate_ip import validate_ipv4, prepare_ips_for_validation
from time import sleep
try:
    import pexpect
except ImportError as error:
    sys.exit("Error while importing Expect Package. Check requirements.txt. Error: {}".format(error))

"""
Extract and Parse data from Thomson TG784n Network Device. (ALTICE MEO)
"""

__author__ = "Nuno Moura"
__copyright__ = "Copyright 2020, Thomson_parser_TG784n"
__license__ = "MIT"
__version__ = "1"
__mantainer__ = "Nuno Moura"
__email__ = "a21250606@alunos.isec.pt"
__status__ = "Prototype"


##### CONFIGURATION
host = "192.168.1.254"
CREDENTIALS = {
    'username': "meo",
    'password': "meo"
}
commands_list = {"logs": "syslog msgbuf show",
                 "hosts": "hostmgr list",
                 "dhcp-list": "dhcp server lease list",
                 "env-variables": "env list",
                 "connections-list": "connection list",
                 "arp-list": "ip arplist"
                 }


def parse_meo_hostmgr_line(l):
    """
    Auxiliary function that cleans the line data (create a list from a line ... )
    :param l: <string>
    Something like this :
    '\n10:7b:44:0e:42:1f 192.168.1.80    CDL     Generic          IP.Intf.LocalNetwork ETH.Phys.ethif1 Unknown-2a-88-77-b1-67-f6'
    :return: <list> list with (strings)
    like this:
    ['\n2c:95:69:c1:80:f9 192.168.1.67', 'CDL', 'Generic', 'IP.Intf.LocalNetwork', 'ETH.Phys.ethif1', 'Unknown-1l-67-80-9f-17-73']
    """
    #data = l[1:-2]
    new_data_list = l.split(" ")
    tmp_data = []
    for line in new_data_list:
        if line != "":
            tmp_data.append(line)
    return tmp_data


def parse_meo_hostmgr(data):
    """
    This function get a list of devices present in MEO THOMSON ROUTER (Connected or not Connected).
    :param data:<List> is a output list obtained after the interaction with MEO THOMSON. command : "hostmgr"
            E.G data
            data = ['list',
            '\nMAC-address       IP-address      Flags   Type             Intf                 Hw Intf    Hostname            ',
            '\n-----------       ----------      -----   ----             ----                 -------    --------            ',
            '\n10:78:40:f7:f1:a3 192.168.1.254   CT      Generic          IP.Intf.LocalNetwork -          localhost           ',
            '\n2c:95:69:c1:80:f9 192.168.1.67    CDL     Generic          IP.Intf.LocalNetwork ETH.Phys.ethif1 Unknown-2a-88-77-b1-67-f6',
            '\n10:7b:44:0e:42:1f 192.168.1.73    DL      Generic          IP.Intf.LocalNetwork ETH.Phys.ethif4 NODE             ',
            '\n88:9e:33:00:b8:06 192.168.1.96    CDL     Generic          IP.Intf.LocalNetwork ETH.Phys.wlif1 android-600bf70b90cf709b',
            '\n1c:67:37:9f:61:73 192.168.1.101    CDL     Generic          IP.Intf.LocalNetwork ETH.Phys.wlif1 Unknown-1l-67-80-9f-17-73',
            '\n']
    :return:<List> A list with dictionaries. Each one, is a device.
    """
    data = data[1:-2]
    data_parsed = []
    for line in data:
        #print(line)
        data_parsed.append(parse_meo_hostmgr_line(line))
    #for line_parsed in data_parsed:

    final_list = []
    for count, ele in enumerate(data_parsed, 0):
        if count < 3: # line 2 is meo local host, line 1 is "---" and line 0 is headers ... We dont need this
            continue
        structured_data = {
            "MAC-address": ele[0].split("\n")[1],
            "IP-address": ele[1],
            "Flags": ele[2],
            "Type": ele[3],
            "Intf": ele[4],
            "Hw Intf": ele[5],
            "Hostname": ele[6]}
        final_list.append(structured_data)
        structured_data = {
            "MAC-address": "",
            "IP-address": "",
            "Flags": "",
            "Type": "",
            "Intf": "",
            "Hw Intf": "",
            "Hostname": ""}
    return final_list


def parse_DHCP_leases(data):
    # A list with this type of structure:
    # Lease                Pool            TTL           State     Clientid
    # 0  192.168.1.253     LAN_private     infinite      USED      [01] 2c-88-77-b1-67-f6
    # 1  192.168.1.70      LAN_private     infinite      USED      [01] 35:36:39:b1:29:f7
    # 2  192.168.1.66      LAN_private     infinite      USED      [01] 10:7b:44:0e:42:1f

    data = data[2:-2]
    #for l in data:
    #    print(repr(l))
    tmp_data_1 =[]
    for line in data:
        line = line.split(" ")
        #print(line)
        tmp_data = []
        for ele in line:
            if ele != "":
                tmp_data.append(ele)
        tmp_data_1.append(tmp_data)
    #print(tmp_data_1)
    #for line in tmp_data_1:
    #    print(line)
    final_list = []
    for line in tmp_data_1:
        structured_data = {
            "Lease": line[0].split("\n")[1],
            "Ip": line[1],
            "Pool": line[2],
            "TTL": line[3],
            "State": line[4],
            "Mac_addr": line[6]}
        final_list.append(structured_data)
        structured_data = {
            "Lease": "",
            "Ip": "",
            "Pool": "",
            "TTL": "",
            "State": "",
            "Mac_addr": ""}
    return final_list


def parse_syslog_messages(data):

    output = {
        "ALL_SYSLOG_LINES": data,
        "CODE_14": [],
        "CODE_37": [],
        "CODE_102": [],
        "CODE_148": [],
        "CODE_173": [],
        "CODE_NUMBER_NOT_IMPLEMENTED": [],

    }

    for line in data:
        if "<14>" in line:
            output["CODE_14"].append(line)
        elif "<37>" in line:
            output["CODE_37"].append(line)
        elif "<102>" in line:
            output["CODE_102"].append(line)
        elif "<148>" in line:
            output["CODE_148"].append(line)
        elif "<173>" in line:
            output["CODE_173"].append(line)
        else:
            output["CODE_NUMBER_NOT_IMPLEMENTED"].append(line)

    return output


def parse_device_env(data):
    """
    parse something like this:
                {meo}=>env list
                _SW_FLAG=E1
                _ETHERNET=SWITCH
                _COMPANY_NAME=THOMSON
                _COMPANY_URL=http://www.thomson.net
                _PROD_NAME=Thomson TG
                _BRAND_NAME=Thomson
                _PROD_URL=http://www.thomson-broadband.com
                _PROD_DESCRIPTION=DSL Internet Gateway Device
                _PROD_NUMBER=784n
                _SSID_SERIAL_PREFIX=Thomson
                _BOARD_SERIAL_NBR=134TAP7
                _PROD_SERIAL_NBR=CP1430NTAP7
                _FII=9.5.16.16.0
                ...
                ...
                ...
    WE WILL SPLIT EACH LINE in the '=' Character.
        - left part will be the key in our dict.
        - right part will be the value
            E.G.
            line = "_PROD_SERIAL_NBR=CP1430NTAP7"
            splitted_line = ["_PROD_SERIAL_NBR", "CP1430NTAP7"]
            key = "_PROD_SERIAL_NBR"
            val = "CP1430NTAP7"
    :param data: <list> data for parsing
    :return:<dictionary> Dynamic Structured Data
    """
    output = {}
    data = data[1:-1]
    for line in data:
        #EXAMPLE: line: '\nSTS_TelnetSshFtp_Fix=Enabled'
        new_line = line.split("\n")[1].split("=")
        output[new_line[0]] = new_line[1]
    return output


def parse_connection_list(data):
    """
            ID   proto      state       substate                  flags         NAT helper   Helper flags timeout
        --   -----      -----       --------                  -----         ----------   ------------ -------
        4    igmp       ACTIVE      0                         [...........]              [.....]      48"
          INIT: 8                                192.168.1.254:0                                           224.0.0.1:0           [.......S..U] loop              96422 igmp       0xC0
          RESP: 9                                    224.0.0.1:0                                       192.168.1.254:0           [RD.........] LocalNetwork          0 igmp       0x88
        82   udp        ACTIVE      0                         [..........R]              [.....]      41"
          INIT: 164                                  127.0.0.1:8080                                        127.0.0.1:8080        [.......S..U] loop                  1 udp        0x00
          RESP: 165                                  127.0.0.1:8080                                        127.0.0.1:8080        [R......S..U] loop              68627 udp        0x00
        257  tcp        ACTIVE      [ESTABLISHED-ESTABLISHED] [...L......R]              [.....]      15' 8"
          INIT: 514                               192.168.1.69:41660                                   192.168.1.254:23          [.......S..U] LocalNetwork        126 tcp        0x10
          RESP: 515                              192.168.1.254:23                                       192.168.1.69:41660       [R......S..U] loop                 90 tcp        0x00

    :param data:
    :return:
    """
    # The firts 10 lines ... we don't need them
    """
          
        Flags Legend for Connections : [I]dle,        Respa[W]n,      [T]imeout,          [L]ong Timeout, Loo[S]e
                                       [F]ixed,       Fl[O]at,        [E]ven,             No reco[V]ery,  [C]one
                                       [R]eserved
        Flags Legend for NAT helpers : [I]nit seq,    [R]esp seq,     Compute [C]hecksum, [E]xpected,     TCP [D]ata
        Flags Legend for Streams :     [R]esponder,   [D]isabled,     [B]roadcast,        [M]ulticast,    NAT [L]oopback
                                       [I]dle,        [A]ccelerated,  [S]low path,        [P]rioritized,  AIP [N]/A
                                       [U]sed
        
        ID   proto      state       substate                  flags         NAT helper   Helper flags timeout   
        --   -----      -----       --------                  -----         ----------   ------------ -------   
    """
    # first_ten = data[0:10]
    #print(first_ten )
    data = data[10:]
    output = []
    counter_0_lst = []
    counter_1_lst = []
    counter_2_lst = []
    connections_counter = 0
    counter = 0  # will be 0, 1 ,2 .... 0, 1, 2, ... 0, 1, 2 ...... n
    for count, line in enumerate(data):
        if len(line) < 2:
            continue
        if count == 0:
            #print("OUTPUT - Printing line {} : {}".format(count, line))
            line = line.split("\n")  # split the second element <-- ['', 'ID   proto      state
            # substate                  flags         NAT helper   Helper flags timeout   ']
            keys = line[1].split(" ")

           #['ID', '', '', 'proto', '', '', '', '', '', 'state', '', '', '', '', '', '', 'substate', '',
            # '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'flags', '', '', '', '', '',
            # '', '', '', 'NAT', 'helper', '', '', 'Helper', 'flags', 'timeout', '', '', '']
            final_keys = []
            for k in keys:
                if k != "":
                    final_keys.append(k)
           #print("OUTPUT- {}".format(final_keys))
            keys = [final_keys[0], final_keys[1], final_keys[2], final_keys[3], final_keys[4],
                    final_keys[5] + "_" + final_keys[6], final_keys[7] + "_" + final_keys[8], final_keys[9]]

            output.append(keys)

            #print("OUTPUT - ==========================================================================================")
        elif count == 1: # JUMP ONE LINE '\n--   -----      -----       --------                  ---------------   ------------ -------   '
            #print("OUTPUT - Printing line {} : {}".format(count, line))
            #print("OUTPUT - Jump this line")
            continue
        # FOR Line 3 to end of lines ..... in data
        else:
            #print("OUTPUT - Printing line {} : {}".format(count, line))
            #print("OUTPUT - Line count is: ", count)
            #print("OUTPUT - Start Sub-Recording")  # recoder line 1 from 3
            #print("OUTPUT - line data is: ", line)
            if counter == 0:
                #print("---------------------------------------------------------")
                #print("OUTPUT - counter:", counter)
                # new _line will be : ['4', '', '', '', 'igmp', '', '', '', '', '', '', 'ACTIVE', '', '', '',
                # '', '', '0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                # '', '', '', '', '[...........]', '', '', '', '', '', '', '', '', '', '', '', '', '', '[.....]',
                # '', '', '', '', '', '50"']
                n_line = line.split("\n")[1].split(" ")

                res = [x for x in n_line if x != ""]   # after this command new_line is = ['4', 'igmp', 'ACTIVE',
                # '0', '[...........]', '[.....]', '50"']

                connection = {keys[0]: res[0],
                              keys[1]: res[1],
                              keys[2]: res[2],
                              }
                counter = counter + 1
                #print("OUTPUT - connection: ", connection)

                # EXPORT LIST
                counter_0_lst = res

                continue  # MAKE the jump to new line
            if counter == 1:

                #print("OUTPUT - counter:", counter)
                #print("OUTPUT - GRAB line 1 from 2:", counter)
                # line is : '\n  INIT: 8                                192.168.1.254:0
                # 224.0.0.1:0           [.......S..U] loop              96685 igmp       0xC0'
                n_line = line.split("\n")[1].split(" ")
                res = [x for x in n_line if x != ""]
                #### OUTPUT- res: ['INIT:', '10', '192.168.1.254:0', '224.0.0.1:0', '[.......S..U]', 'loop', '124463', 'igmp', '0xC0']
                counter = counter + 1
                counter_1_lst = res
                continue  # JUMP TO NEXT LINE

            if counter == 2:
                #print("OUTPUT - counter:", counter)
                #print("OUTPUT - GRAB line 2 from 2:", counter)

                # line is : '\n  INIT: 8                                192.168.1.254:0
                # 224.0.0.1:0           [.......S..U] loop              96685 igmp       0xC0'
                n_line = line.split("\n")[1].split(" ")
                res = [x for x in n_line if x != ""]  #

                counter_2_lst = res
                output.append((counter_0_lst, counter_1_lst, counter_2_lst))

                # RESET VALUES
                counter = 0
                counter_0_lst = []
                counter_1_lst = []
                counter_2_lst = []
                continue  # JUMP TO NEXT LINE

    #print("Terminating ....")
    # PRINTING THE OUTPUT IN HUMAN READABLE
    #for element_number, connection in enumerate(output):
    #    print("ELEMENT NUMBER: ", element_number)
    #    if element_number == 0:
    #        print("{} : NUMERO ELEMENTOS: {}".format(connection, len(connection)))
    #    if element_number >= 1:
    #        for sub_element in connection:
    #            print("{} : NUMERO ELEMENTOS: {}".format(sub_element, len(sub_element)))
    return output


def parse_ip_arplist(data):
    """
    PARSE DATA like this:
    ['ip arplist', '\nInterface           IP-address             HW-address        Type', '\n2   LocalNetwork    192.168.1.251          62:97:47:g6:f8:b9 DYNAMIC', '\n3   InternetGPON    39.196.73.10           01:34:fe:02:02:02DYNAMIC', '\n2   LocalNetwork    192.168.1.67           3c:97:70:b1:58:f7 DYNAMIC', '\n2   LocalNetwork    192.168.1.65           88:9e:33:00:b8:06 DYNAMIC', '\n2   LocalNetwork    192.168.1.66           1c:67:58:9f:61:73 DYNAMIC', '\n2   LocalNetwork    192.168.1.67           20:7c:8f:d8:31:1e DYNAMIC', '\n2   LocalNetwork    192.168.1.91           f9:29:20:01:b:fe DYNAMIC', '\n']
    :param data:<list> like the above list...
    :return: <list> list with entries. Each entry is a dict:
                                                                {'Interface_ID': ',
                                                                 'Interface': '',
                                                                 'IP_Address': '',
                                                                 'MAC_Address': '',
                                                                 'Type': ''}
    """
    output_list = []
    for line in data[2:-1]:
        nl = []
        for element in line.split(" "):
            if element != "" and element != " \n":
                nl.append(element)
        line_dict = {"Interface_ID": nl[0].split("\n")[1],
                     "Interface": nl[1],
                     "IP_Address": nl[2],
                     "MAC_Address": nl[3],
                     "Type": nl[4]}
        output_list.append(line_dict)
    return output_list


def get_raw_data(host, credentials, command):
    """
    CONNECT TO THOMSON, SEND A COMMAND AND GET THE RESULT.
    WE ONLY ACCEPT ONE COMMAND per CONNECTION.

    # IMPORTANT NOTE:
        - WE ARE NOT VALIDATING THE INPUT DATA. SO WE NEED CORRECT data types and "GOOD CREDENTIALS" as well as "IP's"

    :param host:<string> Device ip to connect
    :param credentials: <dictionary> with username and password keys (strings)
    :param command: <string> command to send to Thomson
    :return: <List> CLI OUTPUT after the command
    """

    # NOTE: WE ARE NOT VALIDATING THE DATA INPUT.

    username = credentials["username"] + "\r"
    password = credentials["password"] + "\r"

    make_connection_cmd = "telnet" + " " + host
    print("OUTPUT - Connecting to Device ip:{} ... ".format(host))
    child = pexpect.spawn(command=make_connection_cmd)

    child.expect("Username :")
    child.send(username)
    child.expect("Password : ")
    child.send(password)
    child.expect("{meo}=>")

    # CONSTRUCT COMMAND TO SEND TO DEVICE
    command_to_send = command + "\r"
    print("OUTPUT - Sending command: '{}' to device:{}. ".format(command, host))
    child.send(command_to_send)
    child.expect("{meo}=>")
    data = child.before.decode("utf-8")

    # make a list for exporting, ready for parsing....
    #print("OUTPUT data - \n{}".format(data))
    data = data.split("\r")
    # Disconnect and retreive output list
    child.send("exit\r")
    return data


def write_log(output_dict, file_name, commands_list):

    # logs
    # hosts
    # dhcp-list
    # env-variables
    # connections-list
    # arp-list

    try:
        with open(file_name, "w") as file:
            # print(dumps(out_dict, indent=4))
            # file.write(dumps(out_dict, indent=4))

            if "connections-list" in out_dict:
                print("### Connections")
                file.write("Connections\n")
                for count, line in enumerate(out_dict["connections-list"]):
                    if count == 0:
                        print(line)
                        file.write(str(line) + "\n")
                    else:
                        for value in line:
                            print(value)
                            file.write(str(value) + "\n")
            if "env-variables" in out_dict:
                print("\n### env list ")
                file.write("### env list\n")
                for count, line in enumerate(out_dict["env-variables"]):
                    print("{}:{}".format(line, out_dict["env-variables"][line]))
                    file.write("{}:{}\n".format(line, out_dict["env-variables"][line]))

            if "dhcp-list" in out_dict:
                print("### \nDHCP LIST ")
                file.write("### DHCP LIST \n")
                for dictionary_element in out_dict["dhcp-list"]:
                    print("{}".format(dictionary_element))
                    file.write("{}\n".format(dictionary_element))

            if "arp-list" in out_dict:
                print("### Arp list")
                file.write("\n### ARP list\n")
                for count, line in enumerate(out_dict["arp-list"]):
                    print(line)
                    file.write("{}\n".format(line))
                    # for k, v in line.items():
                    #    print(k, v)

            if "hosts" in out_dict:
                print("###\n HOST MGR  ")
                file.write(" ### HOST MGR\n")
                for dictionary_element in out_dict["hosts"]:
                    print("{}".format(dictionary_element))

                    file.write("{}\n".format(dictionary_element))

            if "logs" in out_dict:
                print("\n### LOGS ")
                file.write("### LOGS \n")
                for count, line in enumerate(out_dict["logs"]):
                    print(count, line)
                    file.write("\n" + line + ":\n")
                    for element in out_dict["logs"][line]:
                        print("{}".format(repr(element)))
                        file.write("{}".format(element))
    except OSError as error:
        print("Error. {}".format(error))
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    helpp = "Try to parse Thomson TG784n Network device:\n" \
            "\tdhcp-list: dhcp leases\n" \
            "\tconnections-list: active connectionsn\n" \
            "\tlogs: device system logs\n"\
            "\tarp-list: arp table\n" \
            "\tenv-variables: device environment variables\n" \
            "\tall: all the options "
    parser.add_argument("-t", "-type", dest="type", choices=["dhcp-list", "connections-list", "logs",
                                                             "arp-list", "env-variables", "host", "all"], required=True,
                        help=helpp)

    args = parser.parse_args()

    out_dict = {}

    # PREPARE TO WRITE IN FILE
    file_name = str(datetime.now()) + "Report_ThomsonTG784n.log"
    # TODO : PARSE command :
    #  nat maplist

    if args.type:
        if args.type =="all":
            for command_name, command_to_send in commands_list.items():
                try:
                    du = get_raw_data(host=host, credentials=CREDENTIALS, command=commands_list[command_name])
                except pexpect.ExceptionPexpect as error:
                    print("ERROR. Please check the network connection: error:\n{}".format(error))
                    exit("ERROR. Please check the network connection")
                if command_name == "logs":
                    dt = parse_syslog_messages(data=du)
                    out_dict[command_name] = dt
                if command_name == "hosts":
                    dt = parse_meo_hostmgr(data=du)
                    out_dict[command_name] = dt
                if command_name == "dhcp-list":
                    dt = parse_DHCP_leases(data=du)
                    out_dict[command_name] = dt
                if command_name == "env-variables":
                    dt = parse_device_env(data=du)
                    out_dict[command_name] = dt
                if command_name == "connections-list":
                    dt = parse_connection_list(data=du)
                    out_dict[command_name] = dt
                if command_name == "arp-list":
                    dt = parse_ip_arplist(data=du)
                    out_dict[command_name] = dt
        else:
            command_name = args.type
            try:
                du = get_raw_data(host=host, credentials=CREDENTIALS, command=commands_list[command_name])
            except pexpect.ExceptionPexpect as error:
                print("ERROR. Please check the network connection: error:\n{}".format(error))
                exit("ERROR. Please check the network connection")

            if command_name == "logs":
                dt = parse_syslog_messages(data=du)
                out_dict[command_name] = dt

            if command_name == "hosts":
                dt = parse_meo_hostmgr(data=du)
                out_dict[command_name] = dt

            if command_name == "dhcp-list":
                dt = parse_DHCP_leases(data=du)
                out_dict[command_name] = dt

            if command_name == "env-variables":
                dt = parse_device_env(data=du)
                out_dict[command_name] = dt

            if command_name == "connections-list":
                dt = parse_connection_list(data=du)
                out_dict[command_name] = dt

            if command_name == "arp-list":
                dt = parse_ip_arplist(data=du)
                out_dict[command_name] = dt


        ## WRITE always LOG ...
        write_log(out_dict, file_name, commands_list)


        #         while True:
        #             if command_name == "connection list":
        #                 dt = parse_connection_list(data=du)
        #                 #print(dumps(dt, indent=4))
        #                 print("@" * 120)
        #                 print(du)
        #                 out_dict[command_name] = dt
        #                 sleep(1)




