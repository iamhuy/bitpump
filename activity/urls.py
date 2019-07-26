# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^category/get/$', views.ActivityCategoryGetView.as_view(), name='activity_category_get'),
    url(r'^lucky_draw/get/$', views.LuckyDrawGetView.as_view(), name='lucky_draw_get'),
    url(r'^lucky_draw/update/$', views.LuckyDrawUpdateView.as_view(), name='lucky_draw_update'),
    url(r'^get/$', views.ActivityGetView.as_view(), name='activity_get'),
    url(r'^update/$', views.ActivityUpdateView.as_view(), name='activity_update'),
    url(r'^image/upload/$', views.ActivityImageUploadView.as_view(), name='activity_image_update'),
]
