#!/usr/bin/env python

"""
3. Create two new test NetworkDevices in the database. Use both direct object creation and the
   .get_or_create() method to create the devices


"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials

def main():
    django.setup()
    router1 = NetworkDevice(
        device_name='router1',
        device_type='cumulus_linux',
        ip_address='1.1.1.1',
        port=1111,
        vendor='Cumulus',
    )
    router1.save()

    NetworkDevice.objects.get_or_create(
        device_name='router2',
        device_type='cumulus_linux',
        ip_address='2.2.2.2',
        port=2222,
        vendor='Cumulus',
    )

    net_devices = NetworkDevice.objects.all()
    for a_device in net_devices:
        print a_device, a_device.vendor

if __name__ == '__main__':
    main()