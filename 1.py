#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


import os,sys,time,hashlib,shutil

time_now=time.strftime('%Y%m%d%H%M', time.localtime())


apath = 'E:\PyCharmScripts\CMDB\AsyncTask'
afiles = []
bfiles = []
for root, dirs , files in os.walk(apath):
    for f in files:
        afiles.append(root)
apathlen = len(apath)
aadirs = []
for d in afiles:
    aadirs.append(d[apathlen:])
for i in aadirs:
    print(i)
