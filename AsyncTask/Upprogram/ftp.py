#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os,subprocess,tarfile
import zipfile,stat,shutil


def tarpkg(platform,program,version,add):
    Initialdir = os.getcwd()
    zipf = add.split('/').pop()
    if os.path.exists(os.getcwd() +'/'+zipf):
        os.remove(os.getcwd() +'/'+zipf)
    ftp = subprocess.call("wget %s" % add,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)
    if ftp == 0:
        if not os.path.isdir(os.getcwd() +'/'+zipf[:-4]):
            os.mkdir(zipf[:-4])
        shutil.rmtree(os.getcwd() +'/'+zipf[:-4])
        os.mkdir(zipf[:-4])
        zipf = os.getcwd() +'/'+ zipf
        oldfile = zipfile.ZipFile(zipf,'r')
        for f in oldfile.namelist():
            oldfile.extract(f,'/'+zipf[:-4])
            os.chmod(zipf[:-4]+'/'+f,stat.S_IRWXU|stat.S_IXGRP|stat.S_IRGRP|stat.S_IROTH|stat.S_IXOTH)
        oldfile.close()
        newfile = tarfile.open(program+'-'+version+'.tar.gz',"w:gz")
        os.chdir(zipf[:-4])
        for root,dir,files in os.walk(zipf[:-4]):
            for f in files:
                newfile.add(f)
        newfile.close()
        nfile = Initialdir+'/'+program+'-'+version+'.tar.gz'
        if platform == 'SinaShow':
#            shutil.move(nfile,'/srv/salt/Sinashow/files/')
            shutil.move(nfile,'/data0/test/filedir/')
        else:
            shutil.move(nfile,'/srv/salt/FengBo_PhoneChat/files/')
    else:
        print 'Fail'
#        return 'Fail'

platform = 'SinaShow'
add = 'ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/show_crs/ChatServer_4.3.1.36.zip'
program = 'ChatServer'
version = '4.3.1.36'
tarpkg(platform,program,version,add)
a


