#!/usr/bin/env python

"""
2. telnetlib

    a. Write a script that connects using telnet to the pynet-rtr1 router. Execute the 'show ip int brief'
     command on the router and return the output.

Try to do this on your own (i.e. do not copy what I did previously). You should be
 able to do this by using the following items:

telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
remote_conn.read_until(<string_pattern>, TELNET_TIMEOUT)
remote_conn.read_very_eager()
remote_conn.write(<command> + '\n')
remote_conn.close()
"""

import telnetlib

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

pynet-rtr1 host=184.105.247.70 port=22 username=pyclass password=88newclass

ip_addr = '184.105.247.70'
username = 'pyclass'
password = '88newclass'
TELNET_PORT = 23
TELNET_TIMEOUT = 6

def telnet_connect(ip_addr, TELNET_PORT, TELNET_TIMEOUT):
    return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)

def telnet_login():
    pass

def send_command():
    pass

def disable_paging():
    pass

def main():
    telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    remote_conn.read_until( < string_pattern >, TELNET_TIMEOUT)
    remote_conn.read_very_eager()
    remote_conn.write( < command > + '\n')
    remote_conn.close()

if __name__ == '__main__':
    main()