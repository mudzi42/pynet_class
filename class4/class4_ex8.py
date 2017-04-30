#!/usr/bin/env python

"""
8. Use Netmiko to change the logging buffer size (logging buffered <size>)
 and to disable console logging (no logging console) from a file on both pynet-rtr1 and pynet-rtr2
 (see 'Errata and Other Info, item #4).
 
 Netmiko supports a method (send_config_from_file) that allows you to execute configuration commands
  directly from a file.
 For example, if you had a set of commands in a file called 'config_file.txt',
  then you could execute those commands via the SSH channel as follows:
     
     net_connect.send_config_from_file(config_file='config_file.txt')
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

from netmiko import ConnectHandler
from class4_devices import pynet1, pynet2
import sys

def main():
    print("Updating  logging buffer size and disable console logging via file on pynet-rtr1 and pynet-rtr2.")
    for device in pynet1, pynet2:
        try:
            n_conn = ConnectHandler(**device)
            print("Connected to {}.".format(device['ip']))
            print("Entering config mode ...")
            if n_conn.config_mode():
                print n_conn.send_config_from_file(config_file='rt_config_file.txt')
                n_conn.exit_config_mode()
                print("Checking for changes on {}...".format(device['ip']))
                print n_conn.send_command('show run | in logging')
            print("Disconnecting from {}".format(device['ip']))
            pynet_rtr2.disconnect()
        except Exception, e:
            sys.exit("SSH connection to {} failed: {}".format(device['ip'], e))



if __name__ == '__main__':
    main()