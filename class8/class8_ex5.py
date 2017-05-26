#!/usr/bin/env python

"""
5. Use Netmiko to connect to each of the devices in the database. Execute 'show version' on each device.
   Calculate the amount of time required to do this.

(applied_python)[chudgins@ip-172-30-0-251 class8]$ ./class8_ex5.py
Elapsed time: 0:00:48.645291

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials
from netmiko import ConnectHandler
from datetime import datetime

def show_version(a_device):
    remote_conn = ConnectHandler(device_type=a_device.device_type,
                                 ip=a_device.ip_address,
                                 username=a_device.credentials.username,
                                 password=a_device.credentials.password,
                                 port=a_device.port, secret='')
    print
    print '#' * 80
    print remote_conn.send_command_expect("show version")
    print '#' * 80
    print

def main():
    django.setup()

    start_time = datetime.now()
    net_devices = NetworkDevice.objects.all()
    for a_device in net_devices:
        show_version(a_device)

    elapsed_time = datetime.now() - start_time
    print "Elapsed time: {}".format(elapsed_time)

if __name__ == '__main__':
    main()