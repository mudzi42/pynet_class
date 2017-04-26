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

#from snmp_helper import snmp_get_oid_v3, snmp_extract
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

# YAML or PICKLE file?
# 'yaml_file' or 'pickle_file'
FILE_TYPE = 'yaml_file'

def load_file(filepath):
    if os.path.isfile(filepath):
        with open(filepath, "r") as file:
            if FILE_TYPE == 'yaml_file':
                router_data = yaml.load(file)
            else:
                router_data = pickle.load(file)
            file.close()

        return router_data

    else:
        print "No file {} to load.".format(filepath)
        return None

def save_file(device, device_data, filepath):
    data = load_file(filepath)
    data[device] = device_data

    with open(filepath, 'w') as file:
        if FILE_TYPE == 'yaml_file':
            yaml.dump(data, file, default_flow_style=False)
        else:
            pickle.dump(data, file)

def has_router_changed(snmp_data, router_data):
    if snmp_data['last_changed'] > router_data['last_changed']:
        return True

    elif snmp_data['uptime'] < router_data['uptime']:
        # reload has occurred
        # check if changed has happened since reload
        if snmp_data['last_changed'] >= RELOAD_WINDOW:
            return True

    return False

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

def run_first_time(filepath):
    if not os.path.isfile(filepath):
        data = {'pynet_rtr2': {'uptime': 0, 'last_changed': 0},
                'pynet_rtr1': {'uptime': 0, 'last_changed': 0}}

        with open(filepath, 'w') as file:
            if FILE_TYPE == 'yaml_file':
                yaml.dump(data, file, default_flow_style=False)
            else:
                pickle.dump(data, file)


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

    for a_device in (pynet_rtr1, pynet_rtr2):
        for the_oid in (SYS_NAME, SYS_DESCR, SYS_UPTIME, RUN_LAST_CHANGED):
            snmp_data = snmp_get_oid_v3(a_device, snmp_user, oid=the_oid)
            snmp_extract_output = snmp_extract(snmp_data)

    #snmp_extract_output = {'pynet_rtr2': {'uptime': 2445540900, 'last_changed': 3045457714},
    #                        'pynet_rtr1': {'uptime': 2575100104, 'last_changed': 3045681252}}

    run_first_time(router_file)

    router_info = load_file(router_file)

    for a_device in snmp_extract_output:
        if has_router_changed(snmp_extract_output[a_device], router_info[a_device]):
            mail_notification(a_device)
            save_file(a_device, snmp_extract_output[a_device], router_file)

        else:
            print "No configuration changes detected on {}\n".format(a_device)


if __name__ == "__main__":
    main()