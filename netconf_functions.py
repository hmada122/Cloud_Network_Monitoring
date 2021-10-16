#!/usr/bin/env python
import sys
from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
import json 
import socket


# use the NETCONF port for your Nexus device
CPORT = 22
# use the user credentials for your Nexus device
CUSER = 'ciscoxr'
CPASS = 'ciscoxr'

SERVERPORT = 1212
LISTENON = "172.16.2.156"

def shutInterface(interface, state, hostIP):      #Example function for shutting interface
    filter_ = '''
<config>
   <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
         <name>'''+ interface + '''</name>
         <enabled>'''+ state + '''</enabled>
      </interface>
   </interfaces>
</config>
'''


    session = connect_ssh(host=hostIP , port=CPORT, username=CUSER, password=CPASS)
    mgr = Manager(session, timeout=120)
    mgr.edit_config(config=filter_)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(( LISTENON, SERVERPORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = str(data).replace("'",'"').replace('b"',"").replace('\\n"','')
            print (data)
            dict = json.loads(data)
            if dict["function"] == 'shutinterface':
                interface = dict['interface']
                state = dict['state']
                hostIP = dict['routerIP']
                try:
                    shutInterface(interface,state,hostIP)
                except Exception as err :
                    print( err)

