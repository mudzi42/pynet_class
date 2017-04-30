#!/usr/bin/env python

"""
3. Use Pexpect to retrieve the output of 'show ip int brief' from pynet-rtr2.

"""

__author__ = 'Chip Hudgins'
__email__ = 'mudzi42@gmail.com'

import pexpect
import sys
import class4_devices as devices

def router_connect(device):
    '''
    pexpect connection
    '''
    # device information
    ip = device['ip']
    username = device['username']
    password = device['password']
    port = device['port']
    timeout = 3
    try:
        expect_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip, port))
        expect_conn.timeout = timeout
        expect_conn.expect('ssword')
        expect_conn.sendline(password)
        expect_conn.expect('#')
        prompt = get_prompt(expect_conn)
        return expect_conn, prompt
    except Exception, e:
        sys.exit("SSH connection to {} failed: {}".format(ip, e))

def get_prompt(expect_conn):
    '''
    set prompt fpr pexpect connection
    '''
    router_name = expect_conn.before
    router_name = router_name.strip(': \r\n\r\n')
    prompt = router_name + expect_conn.after
    return prompt.strip()

def main():
    expect_conn, prompt = router_connect(devices.pynet2)
    try:
        expect_conn.sendline('terminal length 0')
        expect_conn.expect(prompt)
        expect_conn.sendline('show ip int brief')
        expect_conn.expect(prompt)
        print expect_conn.before
    except pexpect.TIMEOUT, e:
        print ("SSH connection timed out on {}: {}".format(devices.pynet2['ip'], e))

if __name__ == '__main__':
    main()