#!/usr/bin/env python

"""
2. Set the vendor field of each NetworkDevice to the appropriate vendor.
   Save this field to the database.

(applied_python)[chudgins@ip-172-30-0-251 class8]$ ./class8_ex2.py
pynet-rtr1 Cisco
pynet-rtr2 Cisco
pynet-sw1 Arista
pynet-sw2 Arista
pynet-sw3 Arista
pynet-sw4 Arista
juniper-srx Juniper
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
        print a_device, a_device.vendor

if __name__ == '__main__':
    main()