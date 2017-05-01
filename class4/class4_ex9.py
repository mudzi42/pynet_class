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
import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from class4_devices import all_devices
from datetime import datetime

def print_output(results):
    print "\nSuccessful devices:"
    for a_dict in results:
        for identifier, v in a_dict.iteritems():
            (success, out_string) = v
            if success:
                print '\n\n'
                print '#' * 80
                print 'Device = {0}\n'.format(identifier)
                print out_string
                print '#' * 80

    print "\n\nFailed devices:\n"
    for a_dict in results:
        for identifier, v in a_dict.iteritems():
            (success, out_string) = v
            if not success:
                print 'Device failed = {0}'.format(identifier)

    print "\nEnd time: " + str(datetime.now())
    print


def worker_show_arp(a_device, mp_queue):
    '''
    Return a dictionary where the key is the device identifier
    Value is (success|fail(boolean), return_string)
    '''

    try:
        a_device['port']
    except KeyError:
        a_device['port'] = 22

    identifier = '{ip}:{port}'.format(**a_device)
    return_data = {}

    show_arp_command = 'show arp'
    SSHClass = netmiko.ssh_dispatcher(a_device['device_type'])

    try:
        net_connect = SSHClass(**a_device)
        show_arp = net_connect.send_command(show_arp_command)
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return_data[identifier] = (False, e)

        # Add data to the queue (for parent process)
        mp_queue.put(return_data)
        return None

    return_data[identifier] = (True, show_arp)
    mp_queue.put(return_data)


def main():
    mp_queue = multiprocessing.Queue()
    processes = []

    print "\nStart time: " + str(datetime.now())

    for a_device in all_devices:
        p = multiprocessing.Process(target=worker_show_arp, args=(a_device, mp_queue))
        processes.append(p)
        # start the work process
        p.start()

    # wait until the child processes have completed
    for p in processes:
        p.join()

    # retrieve all the data from the queue
    results = []
    for p in processes:
        results.append(mp_queue.get())

    print_output(results)


if __name__ == '__main__':
    main()
