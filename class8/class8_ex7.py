#!/usr/bin/env python

"""
7. Repeat exercise #6 except use processes.
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials

def main():
    django.setup()
    net_devices = NetworkDevice.objects.all()

    for a_device in net_devices:
        if 'cisco' in a_device.device_type:
            a_device.vendor = 'Cisco'
        elif 'juniper' in a_device.device_type:
            a_device.vendor = 'Juniper'
        elif 'arista' in a_device.device_type:
            a_device.vendor = 'Arista'

        a_device.save()

    for a_device in net_devices:
        print a_device, a_device.device_type

if __name__ == '__main__':
    main()