#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import paramiko


def Cncremote(comm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='122.226.254.248', port=22, username='root', password='eARtw6rpC4#xVy4SPvAppI7oqpEO24gQ')
    stdin, stdout, stderr = ssh.exec_command(comm)
    return stdout.read().decode()
    ssh.close()

def Telremote(comm):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='115.231.235.153', port=22, username='root', password='zRSpx99QR9C@#oYvu@0xQZlv2H6bdsA5')
    stdin, stdout, stderr = ssh.exec_command('df -hl')
    print(stdout.read().decode())
    ssh.close()