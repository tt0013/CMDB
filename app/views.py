# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,render_to_response
from app import models
from AsyncTask.tasks import Cncremote,Mail
from djcelery.models import TaskMeta,states
# from function.Remote import Cncremote
import time

# Create your views here.
ctime = time.strftime("%Y-%m-%d %X", time.localtime())

# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        obj = models.Userinfo.objects.filter(username=u, password=p).first()
        user = models.Userinfo.objects.filter(username=u).first()
        if obj:
            role_id = obj.user_role_id
            response = redirect('/index/')
            response.set_cookie('username', u, 3600)
            response.set_cookie('role', role_id, 3600)
            return response
        elif not user:
            return HttpResponse('<html><script type="text/javascript">alert("用户不存在"); window.location="/login/"</script></html>')
        else:
            return HttpResponse('<html><script type="text/javascript">alert("密码错误"); window.location="/login/"</script></html>')
    else:
        return redirect("/login/")

# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'soucre/register.html')
    elif request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        beuser = models.Userinfo.objects.filter(username=u).first()
        if beuser:
            return HttpResponse('<html><script type="text/javascript">alert("用户已存在"); window.location="/register/"</script></html>')
        else:
            models.Userinfo.objects.create(username=u, password=p)
            return HttpResponse('<html><script type="text/javascript">alert("注册成功"); window.location="/login/"</script></html>')

# 登录成功
def index(request):
    username = request.COOKIES.get('username','')
    if username:
        obj = models.Userinfo.objects.filter(username=username).first()
        return render_to_response('soucre/index.html', {'obj': obj})
    else:
        return redirect("/login/")

# 修改用户信息
def useredit(request):
    username = request.COOKIES.get('username', '')
    obj = models.Userinfo.objects.filter(username=username).first()
    if not username:
        return redirect("/login/")
    if request.method == 'GET':
        return render_to_response('user/useredit.html', {'obj': obj})
    elif request.method == 'POST':
        user = request.POST.get('user')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if username == user:
            models.Userinfo.objects.filter(username=username).update(username=user, email=email, telephone=phone)
            return HttpResponse('<html><script type="text/javascript">alert("信息已修改"); window.location="/index/"</script></html>')
        else:
            obj = models.Userinfo.objects.filter(username=user).first()
            if obj:
                return HttpResponse('<html><script type="text/javascript">alert("用户已存在"); window.location="/index/useredit.html"</script></html>')
            else:
                models.Userinfo.objects.filter(username=username).update(username=user,email=email,telephone=phone)
                return HttpResponse('<html><script type="text/javascript">alert("修改完成，请重新登录"); window.location="/login/"</script></html>')
    else:
        return redirect("/login/")

# 添加用户权限
def useradd(request):
    username = request.COOKIES.get('username', '')
    role = int(request.COOKIES.get('role', ''))
    obj = models.Userinfo.objects.filter(username=username).first()
    if role == 2:
        if not username:
            return redirect("/login/")
        if request.method == 'GET':
            return render_to_response('user/useradd.html', {'obj': obj})
        elif request.method == 'POST':
            user = request.POST.get('user')
            group = request.POST.get('group')
            power = request.POST.get('power')
            models.Userinfo.objects.filter(username=username).update(username=user,user_group=group,user_role=power)
            return HttpResponse('<html><script type="text/javascript">alert("权限已添加,请重新登录"); window.location="/index/useradd.html/"</script></html>')
    elif role == 1:
        return render_to_response("user/permissions.html", {'obj': obj})
    else:
        return render_to_response("user/permissions.html", {'obj': obj})

# 用户列表
def userlist(request):
    username = request.COOKIES.get('username', '')
    role = int(request.COOKIES.get('role', ''))
    obj = models.Userinfo.objects.filter(username=username).first()
    if role == 2:
        if not username:
            return redirect("/login/")
        userlist = models.Userinfo.objects.all()
        return render(request, 'user/userlist.html', {'userlist': userlist, 'obj': obj})
    elif role == 1:
        return render_to_response("user/permissions.html", {'obj': obj})
    else:
        return render_to_response("user/permissions.html", {'obj': obj})

# 删除用户
def userdel(request,nid):
    username = request.COOKIES.get('username', '')
    if not username:
        return redirect("/login/")
    models.Userinfo.objects.filter(id=nid).delete()
    userlist = models.Userinfo.objects.all()
    obj = models.Userinfo.objects.filter(username=username).first()
    return render_to_response('user/userlist.html', {'userlist': userlist, 'obj': obj})

# 用户密码修改
def passchange(request):
    username = request.COOKIES.get('username', '')
    if not username:
        return redirect("/login/")
    if request.method == 'GET':
        obj = models.Userinfo.objects.filter(username=username).first()
        return render_to_response('user/passchange.html', {'obj': obj})
    elif request.method == 'POST':
        pwd = request.POST.get('pwd')
        models.Userinfo.objects.filter(username=username).update(username=username,password=pwd)
        return HttpResponse('<html><script type="text/javascript">alert("密码修改成功"); window.location="/index/passchange.html/"</script></html>')

# 日志提取
def rsyslog(request):
    username = request.COOKIES.get('username', '')
    obj = models.Userinfo.objects.filter(username=username).first()
    loglist = models.Rsyslog.objects.all()
    if not username:
        return redirect("/login/")
    elif request.method == 'GET':
        return render_to_response('rsyslog/rsyslog.html', {'loglist': loglist, 'obj': obj})
    elif request.method == 'POST':
        net = request.POST.get('net')
        host = request.POST.get('host')
        ip = request.POST.get('ip')
        dates = request.POST.get('date')
        if net == 'tel':
            result = Cncremote.apply_async(('python /data0/Extractlog.py %s %s %s' % (host, ip, dates),'tel'))
            while not result.ready():
                time.sleep(2)
            models.Rsyslog.objects.create(ip=ip,dates=dates,state=result.ready(),result=result.get())
            return render_to_response('rsyslog/rsyslog.html', {'loglist': loglist, 'obj': obj})
        elif net == 'ctc':
            result = Cncremote.apply_async(('python /data0/Extractlog.py %s %s %s' % (host, ip, dates),'ctc'))
            while not result.ready():
                time.sleep(2)
            models.Rsyslog.objects.create(ip=ip,dates=dates,state=result.ready(),result=result.get())
            return render_to_response('rsyslog/rsyslog.html', {'loglist': loglist, 'obj': obj})
    else:
        return render_to_response('rsyslog/rsyslog.html', {'loglist': loglist, 'obj': obj})

#更新邮件发送
def sendmail(request):
    username = request.COOKIES.get('username', '')
    obj = models.Userinfo.objects.filter(username=username).first()
    loglist = models.Sendmail.objects.all()
    if not username:
        return redirect("/login/")
    elif request.method == 'GET':
        return render_to_response('update/sendmail.html', {'loglist': loglist, 'obj': obj})
    elif request.method == 'POST':
        platform = request.POST.get('platform')
        program = request.POST.get('program')
        group = request.POST.get('group')
        dates = request.POST.get('date')
        result = Mail.apply_async((platform,program,group,dates))
        models.Sendmail.objects.create(platform=platform, program=program, group=group, dates=dates, result=result.get())
        return render_to_response('update/sendmail.html', {'loglist': loglist, 'obj': obj})
    else:
        return render_to_response('update/sendmail.html', {'loglist': loglist, 'obj': obj})

#程序更新操作
def update(request):
    username = request.COOKIES.get('username', '')
    obj = models.Userinfo.objects.filter(username=username).first()
    if not username:
        return redirect("/login/")
    elif request.method == 'GET':
        return render_to_response('update/update.html', {'obj': obj})
    elif request.method == 'POST':
        platform = request.POST.get('platform')
        program = request.POST.get('program')
        version = request.POST.get('version')
        address = request.POST.get('add')
        group = request.POST.get('group')
        dates = request.POST.get('date')
        return render_to_response('update/update.html', {'obj': obj})