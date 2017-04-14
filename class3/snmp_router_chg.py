#!/usr/bin/env python

"""
   1. Using SNMPv3 create a script that detects router configuration changes.
   
   If the running configuration has changed, then send an email notification to yourself identifying the router
    that changed and the time that it changed.

Check if the running-configuration has changed, send an email notification when
this occurs.
Logic for detecting the running-config has changed:
    Normal (non-reboot):
        # Did RUN_LAST_CHANGED increase
        if RUN_LAST_CHANGED > network_device_object.last_changed:
            config_changed = True
    Reboot case:
        RUN_LAST_CHANGED decreases (i.e. < network_device_object.last_changed)
        Right after reboot, RUN_LAST_CHANGED is updated upon
        load of running-config from startup-config.
        Create a grace window (RELOAD_WINDOW) for values of RUN_LAST_CHANGED.
        In other words as long as RUN_LAST_CHANGED is <= RELOAD_WINDOW assume
        no running-config changes.
        If RUN_LAST_CHANGED is > RELOAD_WINDOW assume running-config was changed
"""

from snmp_helper import snmp_get_oid_v3, snmp_extract

# OID constants
SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'
SYS_UPTIME = '1.3.6.1.2.1.1.3.0'
RUN_LAST_CHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'

def send_email():
    pass

def has_router_changed():
    pass

def main():
    a_user = 'pysnmp'
    auth_key = 'galileo1'
    encrypt_key = 'galileo1'
    snmp_user = (a_user, auth_key, encrypt_key)

    pynet_rtr1 = ('184.105.247.70', 161)
    pynet_rtr2 = ('184.105.247.71', 161)

    for a_device in (pynet_rtr1, pynet_rtr2):

        print "\n"
        for the_oid in (SYS_NAME, SYS_DESCR, SYS_UPTIME, RUN_LAST_CHANGED):
            snmp_data = snmp_get_oid_v3(a_device, snmp_user, oid=the_oid)
            output = snmp_extract(snmp_data)

            print output
        print "\n"

if __name__ == "__main__":
    main()