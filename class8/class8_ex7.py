#!/usr/bin/env python

"""
7. Repeat exercise #6 except use processes.
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials
from netmiko import ConnectHandler
from datetime import datetime
from multiprocessing import Process

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

    procs = []
    for a_device in net_devices:
        my_proc = Process(target=show_version, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
        print a_proc
        a_proc.join()

    elapsed_time = datetime.now() - start_time
    print "Final elapsed time: {}".format(elapsed_time)

if __name__ == '__main__':
    main()