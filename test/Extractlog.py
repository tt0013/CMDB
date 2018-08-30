#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os,sys
import shutil
import random
import tarfile
import datetime
import subprocess

class Putlog(object):
    def __init__(self, hostname, ip, day):
        self.hostname = hostname
        self.ip = ip
        self.day = day
        self.num = ''.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'], 12)).replace(" ", "")
        self.crsformat = ["show_tps_crs", "show_tps_crs_online", "show_tps_crs_onmic", "show_tps_crs_waitmic","show_tps_xmgp"]
        self.avsformat = ["show_tps_avs","show_tps_avsrp","show_tps_ratio"]

    def ShowCrs(self):
        try:
            with open("/data0/tps/show/%s-%s.log" % ((self.crsformat)[0], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/reg_crs-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass

            with open("/data0/tps/show/%s-%s.log" % ((self.crsformat)[1], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/online_time-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass

            with open("/data0/tps/show/%s-%s.log" % ((self.crsformat)[2], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/onmic_time-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass

            with open("/data0/tps/show/%s-%s.log" % ((self.crsformat)[3], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/waitmic_time-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass

            with open("/data0/tps/show/%s-%s.log" % ((self.crsformat)[4], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/xml_crs-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass
        except(IOError) as e:
            return e

    def ShowAvs(self):
        try:
            with open("/data0/tps/show/%s-%s.log" % ((self.avsformat)[0], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/avs_rep-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass

            with open("/data0/tps/show/%s-%s.log" % ((self.avsformat)[1], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/reg_avs-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass

            with open("/data0/tps/show/%s-%s.log" % ((self.avsformat)[2], self.day), 'r') as files:
                for line in files:
                    if self.hostname in line:
                        with open("/data0/Log/ratio_avs-%s-%s%s.log" % (self.ip, (self.day).replace('-', ''), self.num),'a') as new:
                            new.write(line.replace(self.hostname, ' ').strip() + '\n')
                    else:
                        pass
        except IOError as e:
            return e

    def TarFile(self):
	if len(os.listdir("/data0/Log")) == 0:
            return "Not Log Produced!!!"
        else:
            os.chdir('/data0/Log')
            for root, dir, files in os.walk('/data0/Log'):
                for log in files:
                    bz2file = tarfile.open(log + '.bz2', 'w:bz2')
                    bz2file.add(log)
                    bz2file.close()
                    os.remove(log)
            try:
                for root, dir, files in os.walk('/data0/Log'):
                    for bz2 in files:
                        retcode = subprocess.call("/usr/bin/rsync -rutz %s 183.131.72.254::Tps_Log" % bz2, shell=True)
                        if retcode < 0:
                            arg = False
                        else:
                            arg = True
                if arg == False:
                    return "Log extraction failure!"
                elif arg == True:
                    return "Log extraction success!"
            except OSError as e:
                return ("Execution failed:", e)



if __name__ == '__main__':
    if not os.path.isdir('/data0/Log'):
        os.mkdir('/data0/Log')
    else:
        shutil.rmtree('/data0/Log')
        os.mkdir('/data0/Log')
    log = Putlog(sys.argv[1], sys.argv[2], sys.argv[3])
    if 'Chat' in sys.argv[1]:
        log.ShowCrs()
        print log.TarFile()
    elif 'Avs' in sys.argv[1]:
        log.ShowAvs()
	print log.TarFile()
    else:
        print "Not The machine"