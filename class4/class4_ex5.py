#!/usr/bin/env python

"""
5. Use Netmiko to enter into configuration mode on pynet-rtr2. 
Also use Netmiko to verify your state (i.e. that you are currently in configuration mode).

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

from netmiko import ConnectHandler
from class4_devices import pynet2
import sys

def main():
    hostname = 'pynet-rtr2'
    print("Checking configuration mode on {}.".format(hostname))
    try:
        pynet_rtr2 = ConnectHandler(**pynet2)
        print("Connected to {}.".format(hostname))
        print("Config mode?")
        print(pynet_rtr2.check_config_mode())
        print("Entering config mode ...")
        pynet_rtr2.config_mode()
        print("Config mode?")
        print(pynet_rtr2.check_config_mode())
        print("Disconnecting from {}".format(hostname))
        pynet_rtr2.disconnect()
    except Exception, e:
        sys.exit("SSH connection to {} failed: {}".format(hostname, e))

if __name__ == '__main__':
    main()