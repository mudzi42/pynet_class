#!/usr/bin/env python

"""
1. Use Arista's eAPI to obtain 'show interfaces' from the switch. Parse the 'show interfaces' output to obtain
   the 'inOctets' and 'outOctets' fields for each of the interfaces on the switch.  
   Accomplish this using Arista's pyeapi.

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import pyeapi

def main():
    """
    username: eapi
    password: ZZteslaX
    host: 184.105.247.74
    transport: https
    """

    arista_server_dict = dict(
        ip='184.105.247.74',
        port='8243',
        username='eapi',
        password='ZZteslaX',
    )

    eapi_conn = pyeapi.connect_to("pynet-sw3")

    interfaces = eapi_conn.enable("show interfaces")

    interfaces_data = interfaces[0]['interfaces']

    # print results
    pprint(interfaces)
    pprint(interfaces_data)



    # get inOctets & outOctets
    # eapi_results_interfaces[0]['interfaces']['Ethernet1']['interfaceCounters']['inOctets']
    # eapi_results_interfaces[0]['interfaces']['Ethernet1']['interfaceCounters']['outOctets']
    interfaces_output_dict = {}

    for interface_name, interface_stats in interfaces_data.items():
        interface_counters = interface_stats.get('interfaceCounters', {})
        interfaces_output_dict[interface_name] = (
        interface_counters.get('inOctets'), interface_counters.get('outOctets'))

    # Print
    pprint(interfaces_output_dict)
    print "\n{:20} {:<20} {:<20}".format("Interface:", "inOctets", "outOctets")
    for intf, octets in interfaces_output_dict.items():
        print "{:20} {:<20} {:<20}".format(intf, octets[0], octets[1])

    print

if __name__ == '__main__':
    main()