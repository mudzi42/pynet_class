#!/usr/bin/env python

"""
8. Optional bonus question--use a queue to get the output data back from the child processes
   in question #7. Print this output data to the screen in the main process.
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials
from netmiko import ConnectHandler
from datetime import datetime

from multiprocessing import Process, Queue

def show_version(a_device, output_q):
    output_dict = {}
    remote_conn = ConnectHandler(device_type=a_device.device_type,
                                 ip=a_device.ip_address,
                                 username=a_device.credentials.username,
                                 password=a_device.credentials.password,
                                 port=a_device.port, secret='')
    output = '#' * 80
    output += remote_conn.send_command_expect("show version")
    output += '#' * 80
    output_dict[a_device.device_name] = output
    output_q.put(output_dict)

def main():
    django.setup()

    start_time = datetime.now()
    net_devices = NetworkDevice.objects.all()
    output_q = Queue(maxsize=20)

    procs = []
    for a_device in net_devices:
        my_proc = Process(target=show_version, args=(a_device, output_q))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
        a_proc.join()

    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.iteritems():
            print k
            print val

    elapsed_time = datetime.now() - start_time
    print "Final elapsed time: {}".format(elapsed_time)

if __name__ == '__main__':
    main()