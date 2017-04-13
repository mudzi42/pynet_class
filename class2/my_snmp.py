#!/usr/bin/env python

"""
    4c. Create a script that connects to both routers (pynet-rtr1 and pynet-rtr2)
     and prints out both the MIB2 sysName and sysDescr.
"""

from snmp_helper import snmp_get_oid, snmp_extract

COMMUNITY_STRING = 'galileo'
SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'

def main():
    pynet_rtr1 = ('184.105.247.70', COMMUNITY_STRING, 161)
    pynet_rtr2 = ('184.105.247.71', COMMUNITY_STRING, 161)

    for a_device in (pynet_rtr1, pynet_rtr2):

        print "\n\n"
        for the_oid in (SYS_NAME, SYS_DESCR):
            snmp_data = snmp_get_oid(a_device, oid=the_oid)
            output = snmp_extract(snmp_data)

            print output
        print "\n\n"

if __name__ == "__main__":
    main()