#!/usr/bin/env python

"""
8. Write a Python program using ciscoconfparse that parses the cisco_ipsec.txt file.
Note, this config file is not fully valid (i.e. parts of the configuration are missing). 
The script should find all of the crypto map entries in the file (lines that begin with 'crypto map CRYPTO') and
 for each crypto map entry print out its children.
 
9. Find all of the crypto map entries that are using PFS group2

10. Using ciscoconfparse find the crypto maps that are not using AES (based-on the transform set name). 
Print these entries and their corresponding transform set name. 
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

from ciscoconfparse import CiscoConfParse

def print_parent_child(lists):
    for parent in lists:
        print parent.text
        for child in parent.children:
            print child.text
    print("\n")

def main():
    cisco_cfg = CiscoConfParse('cisco_ipsec.txt')

    print("8. All of the crypto map entries and their children:")
    crypto_cfg = cisco_cfg.find_objects(r"^crypto map")
    print_parent_child(crypto_cfg)

    print("9. All of the crypto map entries using PFS group2:")
    pfsgroup2 = cisco_cfg.find_objects_w_child(parentspec=r"^crypto map", childspec=r"set pfs group2" )
    print_parent_child(pfsgroup2)

    print("10. All of the crypto map entries not using AES:")
    noAES = cisco_cfg.find_objects_wo_child(parentspec=r"^crypto map", childspec=r"set transform-set AES-SHA" )
    print_parent_child(noAES)

if __name__ == '__main__':
    main()