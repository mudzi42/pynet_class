#!/usr/bin/env python

"""
6. Use threads and Netmiko to execute 'show version' on each device in the database.
   Calculate the amount of time required to do this. What is the difference in time between executing
   'show version' sequentially versus using threads?

(applied_python)[chudgins@ip-172-30-0-251 class8]$ ./class8_ex6.py
Final elapsed time: 0:20:05.866715 ?? something wrong here

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials
from netmiko import ConnectHandler
from datetime import datetime
import threading

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
        my_thread = threading.Thread(target=show_version, args=(a_device,))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            print some_thread
            some_thread.join()

    elapsed_time = datetime.now() - start_time
    print "Final elapsed time: {}".format(elapsed_time)

if __name__ == '__main__':
    main()