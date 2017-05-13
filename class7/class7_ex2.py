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

def main():



if __name__ == '__main__':
    main()