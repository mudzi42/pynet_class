#!/usr/bin/env python

"""
1. Use Paramiko to retrieve the entire 'show version' output from pynet-rtr2. 
pynet-rtr2 host=184.105.247.71 port=22 username=pyclass password=88newclass

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import paramiko
import class4_devices as devices
import pprint as pp

def main():
    print devices.pynet2
    print devices.pynet2['username']
    print devices.pynet2['port']
    print devices.pynet2['ip']
    print devices.pynet2['secret']

    remote_connection = paramiko.SSHClient()
    remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_connection.connect(ip, username=devices.pynet2['username'], password=devices.pynet2['secret'],
                              look_for_keys=False, allow_agent=False, port=devices.pynet2['port'])

    remote_connection.invoke_shell()
    remote_connection.send("show version")
    output = remote_connection.recv(5000)
    pp(output)

if __name__ == '__main__':
    main()