# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegisterView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^info/update/$', views.UserInfoUpdateView.as_view(), name='update_info'),
    url(r'^info/get/$', views.UserInfoGetView.as_view(), name='get_info'),
    url(r'^attribute/get/$', views.AttributeGetView.as_view(), name='get_attribute'),
    url(r'^ranking/get/$', views.UserRankingGetView.as_view(), name='get_ranking'),
    url(r'^connection_graph/get/$', views.UserConnectionGetView.as_view(), name='get_connection_graph'),
]
