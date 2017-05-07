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
    
    a. save data to an external "pickle" file
        http://youtu.be/ZJOJjyhhEvM  
    b. save data to an external "yaml" file
    
    
"""

from snmp_helper import snmp_get_oid_v3, snmp_extract
import os.path
import email_helper
import pickle
import yaml

# Constants
# OIDs
SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'
SYS_UPTIME = '1.3.6.1.2.1.1.3.0'
RUN_LAST_CHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'

# 300 seconds (converted to hundredths of seconds)
RELOAD_WINDOW = 300 * 100

# YAML or PICKLE file? 'yaml_file' or 'pickle_file'
FILE_TYPE = 'yaml_file'

DEBUG = True

def load_devices(filepath):
    if os.path.isfile(filepath):
        with open(filepath, "r") as file:
            if FILE_TYPE == 'yaml_file':
                router_data = yaml.load(file)
            else:
                router_data = pickle.load(file)
            file.close()
        print "{0} devices were previously saved\n".format(len(router_data))
        return router_data
    else:
        print "No devices in {} to load.".format(filepath)
        return {}

def save_devices(devices_dict, filepath):
    data = load_devices(filepath)
    for device in devices_dict:
        data[device] = devices_dict[device]

    with open(filepath, 'w') as file:
        if FILE_TYPE == 'yaml_file':
            yaml.dump(data, file, default_flow_style=False)
        else:
            pickle.dump(data, file)

# def has_router_changed(snmp_data, router_data):
#     if snmp_data['last_changed'] > router_data['last_changed']:
#         return True
#     elif snmp_data['uptime'] < router_data['uptime']:
#         # reload has occurred
#         # check if changed has happened since reload
#         if snmp_data['last_changed'] >= RELOAD_WINDOW:
#             return True
#     return False

def mail_notification(device):
    recipient = 'mudzi42@gmail.com'
    sender = 'mudzi42@gmail.com'
    subject = 'Router {} configurations has changed'.format(device)
    message = '''

    The configuration on router {} has changed since last check.


    Regards,

    Mud Zi

    '''.format(device)

    try:
        email_helper.send_mail(recipient, subject, message, sender)
    except Exception, e:
        print("Email notification failed to send for {} with error: {}.".format(device, e))

#     '''
#     Send email notification regarding modified device
#     '''
#
#     current_time = datetime.now()
#
#     sender = 'sender@twb-tech.com'
#     recipient = 'recipient@twb-tech.com'
#     subject = 'Device {0} was modified'.format(net_device.device_name)
#
#     message = '''
# The running configuration of {0} was modified.
# This change was detected at: {1}
# '''.format(net_device.device_name, current_time)
#
#     if send_mail(recipient, subject, message, sender):
#         print 'Email notification sent to {}'.format(recipient)
#         return True

# def get_snmp_data(snmp_user, routers):
#     snmp_extract_output = {}
#     for a_device in routers:
#         for the_oid in (SYS_NAME, SYS_UPTIME, RUN_LAST_CHANGED):
#             snmp_data = snmp_get_oid_v3(a_device, snmp_user, oid=the_oid)
#             snmp_extract_output.append(snmp_extract(snmp_data))
#     return snmp_extract_output
#     #return {'pynet_rtr2': {'uptime': 2445540900, 'last_changed': 3045457714},
#     #                       'pynet_rtr1': {'uptime': 2575100104, 'last_changed': 3045681252}}

def main():
    a_user = 'pysnmp'
    auth_key = 'galileo1'
    encrypt_key = 'galileo1'
    snmp_user = (a_user, auth_key, encrypt_key)
    if FILE_TYPE == 'yaml_file':
        router_file = "router_change.yml"
    else:
        router_file = "router_change.pkl"
    pynet_rtr1 = ('184.105.247.70', 161)
    pynet_rtr2 = ('184.105.247.71', 161)
    print "Checking for router changes ..."
    saved_devices = load_devices(router_file)

    # Temporarily store the current devices in a dictionary
    devices = {}

    # Connect to each device / retrieve last_changed time
    for a_device in (pynet_rtr1, pynet_rtr2):
        snmp_results = []
        for oid in (SYS_NAME, SYS_UPTIME, RUN_LAST_CHANGED):
            try:
                value = snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=oid))
                snmp_results.append(int(value))
            except ValueError:
                snmp_results.append(value)
        fqdn_name, uptime, last_changed = snmp_results
        device_name = fqdn_name.split('.')[0]
        if DEBUG:
            print "\nConnected to device = {0}".format(device_name)
            print "Last changed timestamp = {0}".format(last_changed)
            print "Uptime = {0}".format(uptime)

        # see if this device has been previously saved
        if device_name in saved_devices:
            saved_device = saved_devices[device_name]
            print "{0} {1}".format(device_name, (35 - len(device_name))*'.'),

            # Check for a reboot (did uptime decrease or last_changed decrease?)
            if uptime < saved_device['uptime'] or last_changed < saved_device['last_changed']:
                if last_changed <= RELOAD_WINDOW:
                    print "DEVICE RELOADED...not changed"
                else:
                    print "DEVICE RELOADED...and changed"
                    devices[device_name] = {'uptime': uptime, 'last_changed': last_changed}
                    mail_notification(devices[device_name])
            elif last_changed == saved_device['last_changed']:
                # running-config last_changed is the same
                print "not changed"
            elif last_changed > saved_device['last_changed']:
                # running-config was modified
                print "CHANGED"
                devices[device_name] = {'uptime': uptime, 'last_changed': last_changed}
                mail_notification(devices[device_name])
            else:
                raise ValueError()
        else:
            # New device, just save it
            print "{0} {1}".format(device_name, (35 - len(device_name))*'.'),
            print "saving new device"
            devices[device_name] = {'uptime': uptime, 'last_changed': last_changed}

    # Write the devices to file
    save_devices(devices, router_file)

if __name__ == "__main__":
    main()