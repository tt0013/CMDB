"""CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^index/$', views.index),
    url(r'^index/useredit.html', views.useredit, name='useredit_list'),
    url(r'^index/useradd.html', views.useradd, name='useradd_list'),
    url(r'^index/userlist.html/userdel-(?P<nid>\d+)', views.userdel, name='userdel_list'),
    url(r'^index/userlist.html', views.userlist, name='userlist_list'),
    url(r'^index/passchange.html', views.passchange, name='passchange_list'),

    url(r'^index/rsyslog.html', views.rsyslog),
    url(r'^index/sendmail.html', views.sendmail),
    url(r'^index/update.html', views.update),
    # url(r'^tasks/', views.tasks,name='task'),

]
