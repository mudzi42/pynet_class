#!/usr/bin/env python

"""
7. Use Netmiko to change the logging buffer size (logging buffered <size>) on pynet-rtr2.

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

from netmiko import ConnectHandler
from class4_devices import pynet2
import sys

def main():
    hostname = 'pynet-rtr2'
    print("Changing logging buffer size on {}.".format(hostname))
    try:
        pynet_rtr2 = ConnectHandler(**pynet2)
        print("Connected to {}.".format(hostname))
        print("Checking logging buffer size before change on {}...".format(hostname))
        print pynet_rtr2.send_command('show run | in logging buffered')
        print("Entering config mode ...")
        if pynet_rtr2.config_mode():
            pynet_rtr2.send_command('logging buffered 20012')
            pynet_rtr2.exit_config_mode()
            print("Checking logging buffer size after change on {}...".format(hostname))
            print pynet_rtr2.send_command('show run | in logging buffered')
        print("Disconnecting from {}".format(hostname))
        pynet_rtr2.disconnect()
    except Exception, e:
        sys.exit("SSH connection to {} failed: {}".format(hostname, e))

if __name__ == '__main__':
    main()