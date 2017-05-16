#!/usr/bin/env python

"""
2. Using Arista's pyeapi, create a script that allows you to add a VLAN (both the VLAN ID and the VLAN name).

  Your script should first check that the VLAN ID is available and only add the VLAN if it doesn't already exist.
  Use VLAN IDs between 100 and 999.  You should be able to call the script from the command line as follows:

   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

   If you call the script with the --remove option, the VLAN will be removed.

   python eapi_vlan.py --remove 100          # remove VLAN100

   Once again only remove the VLAN if it exists on the switch.  You will probably want to use
   Python's argparse to accomplish the argument processing.

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import pyeapi
import argparse

DEBUG = True

def check_if_vlan_exists(eapi_conn, vlan_id):
    vlan_id = str(vlan_id)
    command_str = 'show vlan id {}'.format(vlan_id)
    print command_str
    commands_list = [command_str]

    try:
        response = eapi_conn.enable(commands_list)
        print response
        # [{u'sourceDetail': u'', u'vlans': {u'817':
        # {u'status': u'active', u'interfaces': {}, u'dynamic': False, u'name': u'ch_cheng'}}}]
        # response[0]['vlans']['817']['name']
        check_vlan = response[0]['vlans']
        if check_vlan.get(vlan_id) is not None:
            vlan_name = check_vlan[vlan_id]['name']
            return vlan_name

    except (pyeapi.eapilib.CommandError, KeyError):
        pass

    return False


def configure_vlan(eapi_conn, vlan_id, vlan_name=None):

    command_vlan = 'vlan {}'.format(vlan_id)
    commands = [command_vlan]
    print command_vlan

    if vlan_id is not None:
        print("name provided")
        command_vlan_name = 'name {}'.format(vlan_name)
        commands.append(command_vlan_name)

    return eapi_conn.config(commands)

def main():
    eapi_conn = pyeapi.connect_to("pynet-sw3")

    # Argument parsing
    parser = argparse.ArgumentParser(description="ARISTA VLAN tool")
    parser.add_argument("vlan_id", help="VLAN number to create or remove", action="store", type=int)
    parser.add_argument("--name", help="Specify VLAN name", action="store", dest="vlan_name", type=str)
    parser.add_argument("--remove", help="Remove the given VLAN ID", action="store_true")

    cli_args = parser.parse_args()
    if DEBUG:
        print("CLI ARGS: {}").format(cli_args)

    vlan_id = cli_args.vlan_id  # int
    vlan_name = cli_args.vlan_name  # str
    remove = cli_args.remove  # True False

    # Check if VLAN exists
    check = check_if_vlan_exists(eapi_conn, vlan_id)
    if DEBUG:
        print("Does VLAN {} exists: {}").format(vlan_id, check)

    # action remove / add
    if remove:
        if DEBUG:
            print "action is remove"
        if check:
            # name found
            print("VLAN {} exists, removing it".format(vlan_id))
            # removing vlan
            command_str = 'no VLAN {}'.format(vlan_id)
            eapi_conn.config([command_str])
        # results = eapi_conn.config([command_str])
        # print results # should return empty string

        else:
            print("VLAN {} does not exist, no action required".format(vlan_id))
    else:
        # print "action is add"
        if check:
            # name found
            if vlan_name is not None and check != vlan_name:
                print("VLAN {} already exists, setting VLAN name to {}".format(vlan_id, vlan_name))
                # renaming vlan
                configure_vlan(eapi_conn, vlan_id, vlan_name)
            else:
                print("VLAN {} with name {} already exists, no action required".format(vlan_id, vlan_name))
        else:
            print("Adding VLAN {} with name {} (if present)".format(vlan_id, vlan_name))
            configure_vlan(eapi_conn, vlan_id, vlan_name)


if __name__ == '__main__':
    main()