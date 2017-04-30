#!/usr/bin/env python

"""
9. Bonus Question - Redo ex6 but have the SSH connections happen concurrently using either threads or processes
 see example =>
 http://t.dripemail2.com/c/eyJhY2NvdW50X2lkIjoiNDI1NDQ5NyIsImRlbGl2ZXJ5X2lkIjoiNzUwNTExODU4IiwidXJsIjoiaHR0cHM6Ly9naXRodWIuY29tL2t0YnllcnMvbmV0bWlrby9ibG9iL21hc3Rlci9leGFtcGxlcy9tdWx0aXByb2Nlc3NfZXhhbXBsZS5weT9fX3M9emF5cW1vcXVjY3FubXAyanRuY3EifQ
 What main issue is there with using threads in Python? => Implicit mutability everywhere

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import multiprocessing
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