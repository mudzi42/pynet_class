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
            self.tconn = telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Telnet connection timed out after {} seconds".format(TELNET_TIMEOUT))


    def telnet_login(self):
        '''
        login to network device
        '''

        output = self.t_conn.read_until("sername:", TELNET_TIMEOUT)
        send_command(self.t_conn, self.username)
        output += self.t_conn.read_until("assword:", TELNET_TIMEOUT)
        output += self.send_command(self.t_conn, self.password)

        return output


    def send_command(self, cmd="\n", sleep_time=1):
        '''
        send a command down the telnet connection
        '''

        self.t_conn.write(cmd.rstrip() + '\n')
        sleep(sleep_time)

        return self.t_conn.read_very_eager()


    def disable_paging(self, cmd='terminal length 0'):
        '''
        disable the paging of output
        '''

        return send_command(self.t_conn, cmd)


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
    t_conn.close()

if __name__ == '__main__':
    main()
