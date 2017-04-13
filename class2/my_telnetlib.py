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
    telnet connection
    '''

    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        sys.exit("Telnet connection timed out after {} seconds".format(TELNET_TIMEOUT))

def telnet_login(t_conn, username, password):
    '''
    login to network device
    '''

    output = t_conn.read_until("sername:", TELNET_TIMEOUT)
    send_command(t_conn, username)
    output += t_conn.read_until("assword:", TELNET_TIMEOUT)
    output += send_command(t_conn, password)

    return output

def send_command(t_conn, cmd):
    '''
    send a command down the telnet connection
    '''

    t_conn.write(cmd.rstrip() + '\n')
    sleep(1)

    return t_conn.read_very_eager()

def disable_paging(t_conn, cmd='terminal length 0'):
    '''
    disable the paging of output
    '''

    return send_command(t_conn, cmd)

def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'

    t_conn = telnet_connect(ip_addr)
    telnet_login(t_conn, username, password)

    disable_paging(t_conn)
    output = send_command(t_conn, 'sh ip int br')

    print "\n\n"
    print output
    print "\n\n"
    t_conn.close()

if __name__ == '__main__':
    main()
