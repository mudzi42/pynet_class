#!/usr/bin/env python

"""
4. Remove the two objects created in the previous exercise from the database.


"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials

def main():
    django.setup()

    try:
        router1 = NetworkDevice.objects.get(device_name='router1')
        router2 = NetworkDevice.objects.get(device_name='router2')
        router1.delete()
        router2.delete()
    except NetworkDevice.DoesNotExist:
        pass

    net_devices = NetworkDevice.objects.all()
    for a_device in net_devices:
        print a_device, a_device.vendor

if __name__ == '__main__':
    main()