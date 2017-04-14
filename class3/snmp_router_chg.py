#!/usr/bin/env python

"""
   1. Using SNMPv3 create a script that detects router configuration changes.
"""

from snmp_helper import snmp_get_oid_v3, snmp_extract

SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'

def main():
    a_user = 'pysnmp'
    auth_key = 'galileo1'
    encrypt_key = 'galileo1'
    snmp_user = (a_user, auth_key, encrypt_key)

    pynet_rtr1 = ('184.105.247.70', 161)
    pynet_rtr2 = ('184.105.247.71', 161)

    for a_device in (pynet_rtr1, pynet_rtr2):

        print "\n"
        for the_oid in (SYS_NAME, SYS_DESCR):
            snmp_data = snmp_get_oid_v3(a_device, snmp_user, oid=the_oid)
            output = snmp_extract(snmp_data)

            print output
        print "\n"

if __name__ == "__main__":
    main()