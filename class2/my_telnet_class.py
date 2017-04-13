#!/usr/bin/env python

"""
3. telnetlib (optional - challenge question)

    Convert the telnetlib code to a class-based solution 
    (i.e. convert over from functions to a class with methods).
"""

import telnetlib
import socket
import sys
from time import sleep

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'


TELNET_PORT = 23
TELNET_TIMEOUT = 6


class TelnetConn(object):

    def __init__(self, ip_addr, username, password):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password


        try:
            self.t_conn = telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Telnet connection timed out after {} seconds".format(TELNET_TIMEOUT))


    def telnet_login(self):
        '''
        login to network device
        '''

        output = self.t_conn.read_until("sername:", TELNET_TIMEOUT)
        self.send_command(self.username)
        output += self.t_conn.read_until("assword:", TELNET_TIMEOUT)
        output += self.send_command(self.password)
        self.send_command()
         
        return output


    def send_command(self, cmd="\n", sleep_time=1):
        '''
        send a command down the telnet connection
        '''
        
        cmd = cmd.rstrip()
        self.t_conn.write(cmd + '\n')
        sleep(sleep_time)

        return self.t_conn.read_very_eager()


    def disable_paging(self, cmd='terminal length 0'):
        '''
        disable the paging of output
        '''

        return self.send_command(cmd)

    def telnet_close(self):
        '''
        close telnet connection
        '''

        self.t_conn.close()


def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'

    t_conn = TelnetConn(ip_addr, username, password)
    t_conn.telnet_login()

    t_conn.disable_paging()
    output = t_conn.send_command('sh ip int br')

    print "\n\n"
    print output
    print "\n\n"
    t_conn.telnet_close()

if __name__ == '__main__':
    main()
