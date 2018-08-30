#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import time,ConfigParser
from CreateHtml import CreateHtml
from SendMail import SendMail

conf = ConfigParser.ConfigParser()
conf.read('E:\PyCharmScripts\CMDB\AsyncTask\mail\mail.ini')

class Result(object):
    def __init__(self):
        self.platform = conf.get('MAIL','platform')
        self.program = conf.get('MAIL','program')
        self.group = conf.get('MAIL','group')
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.state = conf.get('MAIL','state')
        self.filename = 'E:\PyCharmScripts\CMDB\AsyncTask\mail\CreateHtml.html'


    def send(self):
        # 根据状态码判断是否发送邮件
        if self.state == '1':
            CreateHtml(self.filename,self.platform,self.program,self.date)
            if self.platform == 'SinaShow':
                Title = u'[重要通知]-[程序更新]-[SHOW平台程序更新]-[%s]' % self.date
            else:
                Title = u'[重要通知]-[程序更新]-[疯播平台程序更新]-[%s]' % self.date
            m = SendMail(
                self.platform, self.program, self.group, self.date, title=Title, file=self.filename
            )
            m.send_mail()
        else:
            pass


if __name__ == '__main__':
    s = Result()
    s.send()
    #邮件更新完毕，状态码恢复
    if conf.get('MAIL','state') == '1':
        conf.set('MAIL', 'state', 0)
        conf.write(open('E:\PyCharmScripts\CMDB\AsyncTask\mail\mail.ini','w'))
    else:
        pass
