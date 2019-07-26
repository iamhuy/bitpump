# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegisterView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^info/update/$', views.UserInfoUpdateView.as_view(), name='update_info'),
    url(r'^info/get/$', views.UserInfoGetView.as_view(), name='get_info'),
]
