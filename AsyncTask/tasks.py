#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

from __future__ import absolute_import, unicode_literals
import paramiko
from celery import task
from AsyncTask.mail.CreateHtml import CreateHtml
from AsyncTask.mail.SendMail import SendMail


# 日志异步
@task
def Cncremote(comm,net):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if net == 'tel':
            ip = '122.226.254.248';passwd = '$hu)8#MbT0ZKTiRQ&736g4tb5hr$N%rl'
        else:
            ip = '115.231.235.153';passwd = 'lrqF)(JhNrjpaL2EZ#$yCIFX5B8y(gXt'
        ssh.connect(hostname=ip, port=22, username='root', password=passwd)
        stdin, stdout, stderr = ssh.exec_command(comm)
        res = stdout.read().decode()
        print(res)
        # stdout.read().decode()
        ssh.close()
        return res
    except Exception as e:
        return 'Auth Fail'

#邮件发送
@task
def Mail(platform,program,group,day,filename='E:\PyCharmScripts\CMDB\AsyncTask\mail\CreateHtml.html'):
    CreateHtml(filename, platform, program, day)
    if platform == 'SinaShow':
        Title = u'[重要通知]-[程序更新]-[SHOW平台程序更新]-[%s]' % day
    else:
        Title = u'[重要通知]-[程序更新]-[疯播平台程序更新]-[%s]' % day
    m = SendMail(
        platform,program,group,day,title=Title,file=filename
    )
    return m.send_mail()




