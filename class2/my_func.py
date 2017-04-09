#!/usr/bin/env python

"""
1c. Write a simple Python module that contains one function that prints 'hello'
 (module name = my_func.py). 
 Do a test where you import my_func into a new Python script. 
 Test this using the following contexts:
    * my_func.py is located in the same directory as your script
    * my_func.py is located in some random subdirectory (not the same directory as your script)
    * my_func.py is located in ~/applied_python/lib/python2.7/site-packages/
"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

def print_hello():
    print("Hello python module World")
