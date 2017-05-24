#!/usr/bin/env python

"""
3. Create two new test NetworkDevices in the database. Use both direct object creation and the
   .get_or_create() method to create the devices

(applied_python)[chudgins@ip-172-30-0-251 class8]$ ./class8_ex3.py
pynet-rtr1 Cisco
pynet-rtr2 Cisco
pynet-sw1 Arista
pynet-sw2 Arista
pynet-sw3 Arista
pynet-sw4 Arista
juniper-srx Juniper
router1 Cumulus
router2 Cumulus
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