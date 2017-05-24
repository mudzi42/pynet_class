#!/usr/bin/env python

"""
1b. Update the NetworkDevice objects such that each NetworkDevice links to
 the correct Credentials.


"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import django
from net_system.models import NetworkDevice, Credentials

def main():
    """Link credentials to devices"""
    django.setup()
    net_devices = NetworkDevice.objects.all()
    creds = Credentials.objects.all()

    std_creds = creds[0]
    arista_creds = creds[1]

    for a_device in net_devices:
        if 'pynet-sw' in a_device.device_name:
            a_device.credentials = arista_creds
        else:
            a_device.credentials = std_creds
        a_device.save()

    for a_device in net_devices:
        print a_device, a_device.credentials


if __name__ == '__main__':
    main()