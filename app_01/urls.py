"""app_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import re_path, include, url
import app_01_app.views
#patterns package not usable,use re_path instead
urlpatterns = [
    url(r'^$', app_01_app.views.index),
    url(r'^login$', app_01_app.views.login_view),
    url(r'^logout$', app_01_app.views.logout_view),
    url(r'^signup$', app_01_app.views.signup),
    url(r'^app_01s$', app_01_app.views.public),
    url(r'^submit$', app_01_app.views.submit),
    url(r'^users/$', app_01_app.views.users),
    url(r'^users/(?P<username>\w{0,30})/$', app_01_app.views.users),
    url(r'^follow$', app_01_app.views.follow),
]
