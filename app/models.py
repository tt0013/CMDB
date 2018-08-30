# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



# 用户信息数据
class Userinfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=60)
    telephone = models.CharField(max_length=30)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    uptime = models.DateTimeField(auto_now=True, null=True)
    user_group = models.ForeignKey("UserGroup", to_field='uid', default=1)
    user_role = models.ForeignKey("UserRole", to_field='tid', default=1)

class UserRole(models.Model):
    tid = models.AutoField(primary_key=True)
    role = models.CharField(max_length=32, unique=True)

class UserGroup(models.Model):
    uid = models.AutoField(primary_key=True)
    group = models.CharField(max_length=32, unique=True)


# 日志提取数据
class Rsyslog(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=32)
    dates = models.DateField(null=True)
    ltime = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=64)
    result = models.CharField(max_length=64)

    def __str__(self):
        return self.result

# saltstack
class Host(models.Model):
    hostname = models.CharField(max_length=128,unique=True)
    key = models.TextField()
    status_choices = ((0,'Waiting Approval'),
                      (1,'Accepted'),
                      (2,'Rejected'))


    # os_type = models.CharField(choices=os_type_choices,max_length=64,default='redhat')
    status = models.SmallIntegerField(choices=status_choices,default=0)

    def __str__(self):
        return self.hostname
class HostGroup(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    hosts = models.ManyToManyField(Host,blank=True)

    def __str__(self):
        return self.name

#邮件发送
class Sendmail(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=32)
    program = models.CharField(max_length=32)
    group = models.CharField(max_length=32)
    dates = models.DateField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=64)

    def __str__(self):
        return self.result

#更新信息
class Updatemessage(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=32)
    program = models.CharField(max_length=32)
    version = models.CharField(max_length=64)
    group = models.CharField(max_length=32)
    dates = models.DateField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=64)

    def __str__(self):
        return self.result