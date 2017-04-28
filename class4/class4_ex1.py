#!/usr/bin/env python

"""
1. Use Paramiko to retrieve the entire 'show version' output from pynet-rtr2. 

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
    password = device['secret']
    port = device['port']
    try:
        p_conn_prep = paramiko.SSHClient()
        p_conn_prep.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        p_conn_prep.connect(ip, username=username, password=password,
                            look_for_keys=False, allow_agent=False, port=port)
        p_conn = p_conn_prep.invoke_shell()
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

def main():
    p_conn = router_connect(devices.pynet2)
    send_command(p_conn, 'show version\n')
    if p_conn.recv_ready():
        print p_conn.recv(MAX_BUFFER)
    else:
        print "No output received from {}".format(devices.pynet2['ip'])

if __name__ == '__main__':
    main()
