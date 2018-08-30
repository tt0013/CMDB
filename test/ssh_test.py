#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


import paramiko

for i in range(3):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='192.168.9.169', port=22, username='root', password='1')
        stdin, stdout, stderr = ssh.exec_command('df -hl')
        print(stdout.read().decode())
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException:
        print("content error")