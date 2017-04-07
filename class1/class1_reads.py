#!/usr/bin/env python

"""
7. Write a Python program that reads both the YAML file and the JSON file created in exercise6 and pretty prints the
 data structure that is returned.
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import yaml
import json
from pprint import pprint

def yaml_read(file_prefix):
    with open(file_prefix + '.yml', "r") as file:
        new_list = yaml.load(file)
    return new_list

def json_read(file_prefix):
    with open(file_prefix + '.json', "r") as file:
        new_list = json.load(file)
    return new_list

def main():
    file_prefix = 'class1_list'
    print("7. Loading and  pretty printing YAML file:")
    pprint(yaml_read(file_prefix))
    print("7. Loading and pretty printing JSON file:")
    pprint(json_read(file_prefix))

if __name__ == '__main__':
    main()
