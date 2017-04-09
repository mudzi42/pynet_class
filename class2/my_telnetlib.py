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
import socket
import sys
from time import sleep

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'


TELNET_PORT = 23
TELNET_TIMEOUT = 6

def telnet_connect(ip_addr):
    '''
    Establish telnet connection
    '''
    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        print "Telnet connection timed out after {} seconds".format(TELNET_TIMEOUT)
        sys.exit()

def telnet_login(t_conn, username, password):
    '''
    Login to network device
    '''
    output = t_conn.read_until("username:", TELNET_TIMEOUT)
    print output
    t_conn.write(username + '\n')
    output += t_conn.read_until("assword:", TELNET_TIMEOUT)
    print output
    t_conn.write(password + '\n')
    return output

def send_command():
    '''
    Send a command down the telnet channel
    Return the response
'''

    pass

def disable_paging():
    '''
    Disable the paging of output (i.e. --More--)
    '''
    pass
def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'
    t_conn = telnet_connect(ip_addr)
    output = telnet_login(t_conn, username, password)
    sleep(1)
    output += t_conn.read_very_eager()
    print output 
    t_conn.write('terminal length 0' + '\n')
    t_conn.write('sh ip int br' + '\n')
    sleep(1)
    output += t_conn.read_very_eager()
    print "\n\n"
    print output
    print "\n\n"
    #remote_conn.read_until( < string_pattern >, TELNET_TIMEOUT)
    #remote_conn.read_very_eager()
    #remote_conn.write( < command > + '\n')
    t_conn.close()

if __name__ == '__main__':
    main()
