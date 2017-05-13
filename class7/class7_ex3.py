#!/usr/bin/env python

"""
3. Challenge exercise (optional) -- Using Arista's eAPI, write an Ansible module that adds a VLAN
   (both a VLAN ID and a VLAN name).  Do this in an idempotent manner i.e. only add the VLAN if it doesn't exist;
    only change the VLAN name if it is not correct.

    To simplify this process, use the .eapi.conf file to store the connection arguments
     (username, password, host, port, transport).

    For additional reference, see here
    http://docs.ansible.com/ansible/dev_guide/developing_modules_general.html
    The 'Common Module Boilerplate' section is important.

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import pyeapi

def main():



if __name__ == '__main__':
    main()