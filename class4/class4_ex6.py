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
            print("Connected to {}.".format(device.hostname))
            print("Config mode?")
            print(pynet_rtr2.check_config_mode())
            print("Entering config mode ...")
            pynet_rtr2.config_mode()
            print("Config mode?")
            print(pynet_rtr2.check_config_mode())
            print("Disconnecting from {}".format(hostname))
            pynet_rtr2.disconnect()
            print pynet_rtr2.send_command('sh run')

        except Exception, e:
            sys.exit("SSH connection to {} failed: {}".format(hostname, e))

if __name__ == '__main__':
    main()