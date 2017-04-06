#!/usr/bin/env python

"""
6. Write a Python program that creates a list. One of the elements of the list should be a dictionary with at least
 two keys. 
Write this list out to a file using both YAML and JSON formats. The YAML file should be in the expanded form.
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import yaml
import json
from glob import glob

def create_list():
    this_list = range(8)
    this_list.append("Thebe")
    this_list.append("Ganymede")
    this_list.append({})
    this_list[-1]['ip_address'] = '5.5.5.5'
    this_list[-1]['hostname'] = 'Europa'
    return this_list

def yaml_file(list, file_prefix):
    with open(file_prefix + '.yml', 'w') as outfile:
        yaml.dump(list, outfile, explicit_start=True, default_flow_style=False)

def json_file(list, file_prefix):
    with open(file_prefix + '.json', 'w') as outfile:
        json.dump(list, outfile)

def main():
    file_prefix = 'class1_list'
    my_list = create_list()
    print("6. my_list: \n{}".format(my_list))
    print("6. One element in my_list is a {} with {} keys.".format(type(my_list[-1]), len(my_list[-1])))
    yaml_file(my_list, file_prefix)
    json_file(my_list, file_prefix)
    print("6. Files created: {}".format(glob(file_prefix + '.*')))


if __name__ == '__main__':
    main()
