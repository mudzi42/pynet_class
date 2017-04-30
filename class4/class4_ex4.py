#!/usr/bin/env python

"""
4. Use PExpect to change the logging buffer size (logging buffered <size>) on pynet-rtr2. 
Verify this change by examining the output of 'show run'.

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
        disable_paging(expect_conn, prompt)
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

def get_enable_prompt():
    '''
    set enable prompt fpr pexpect connection
    router_name(config)# or router_name(config-if)#
    '''
    return '\)#'

def send_command(expect_conn, prompt, cmd):
    '''
    send a command down the pexpect connection
    '''
    try:
        expect_conn.sendline(cmd.rstrip())
        expect_conn.expect(prompt)
        return expect_conn.before
    except pexpect.TIMEOUT, e:
        print ("SSH connection timed out on {}: {}".format(ip, e))

def disable_paging(expect_conn, prompt, cmd='terminal length 0'):
    '''
    disable the paging on router via 'terminal length 0'
    '''
    send_command(expect_conn, prompt, cmd)

def main():
    expect_conn, prompt = router_connect(devices.pynet2)
    enable_prompt = get_enable_prompt()
    print send_command(expect_conn, prompt, 'show run | in logging buffered')
    send_command(expect_conn, enable_prompt, 'conf t')
    send_command(expect_conn, enable_prompt, 'logging buffered 20012')
    send_command(expect_conn, prompt, 'end')
    print send_command(expect_conn, prompt, 'show run | in logging buffered')

if __name__ == '__main__':
    main()