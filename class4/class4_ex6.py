#!/usr/bin/env python

"""
6. Use Netmiko to execute 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'


from netmiko import ConnectHandler
from class4_devices import pynet1, pynet2, juniper_srx
import sys

def main():
    print("Checking 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.")
    for device in pynet1, pynet2, juniper_srx:
        try:
            n_conn = ConnectHandler(**device)
            print("Connected to {}.".format(device['ip']))
            n_conn.disable_paging()
            print n_conn.send_command('show arp')
            n_conn.disconnect()
        except Exception, e:
            sys.exit("SSH connection to {} failed: {}".format(device['ip'], e))

if __name__ == '__main__':
    main()