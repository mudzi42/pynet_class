#!/usr/bin/env python

"""
2. Use Paramiko to change the 'logging buffered <size>' configuration on pynet-rtr2. 
This will require that you enter into configuration mode.

pynet-rtr2#sh run | in logging
logging buffered 20000
no logging console
 logging synchronous

pynet-rtr2#conf t
pynet-rtr2(config)#logging buffered 20001
pynet-rtr2(config)#end
pynet-rtr2#sh run | in logging buffered
logging buffered 20001

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import paramiko
from time import sleep
import sys
import class4_devices as devices

MAX_BUFFER = 65535

def router_connect(device):
    '''
    paramiko connection
    '''
    # device information
    ip = device['ip']
    username = device['username']
    password = device['password']
    port = device['port']
    timeout = 60
    try:
        p_conn_prep = paramiko.SSHClient()
        p_conn_prep.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        p_conn_prep.connect(ip, username=username, password=password,
                            look_for_keys=False, allow_agent=False, port=port)
        p_conn = p_conn_prep.invoke_shell()
        p_conn.settimeout(timeout)
        disable_paging(p_conn)
        return p_conn
    except Exception, e:
        sys.exit("SSH connection to {} failed: {}".format(ip, e))

def send_command(p_conn, cmd):
    '''
    send a command down the paramiko connection
    '''
    p_conn.send(cmd.rstrip() + '\n')
    sleep(1)

def disable_paging(p_conn, cmd='terminal length 0'):
    '''
    disable the paging on router via 'terminal length 0'
    '''
    send_command(p_conn, cmd)
    clear_buffer(p_conn)

def clear_buffer(p_conn):
    '''
    clear out any buffer in paramiko connection
    '''
    p_conn.recv(MAX_BUFFER)
    sleep(1)

def print_router_output(p_conn, device):
    if p_conn.recv_ready():
        print p_conn.recv(MAX_BUFFER)
    else:
        print "No output received from {}".format(device['ip'])

def main():
    p_conn = router_connect(devices.pynet2)
    send_command(p_conn, 'show run | in logging buffered\n')
    print_router_output(p_conn, devices.pynet2)
    send_command(p_conn, 'conf t\n')
    send_command(p_conn, 'logging buffered 20002\n')
    send_command(p_conn, 'end\n')
    send_command(p_conn, 'show run | in logging buffered\n')
    print_router_output(p_conn, devices.pynet2)

if __name__ == '__main__':
    main()