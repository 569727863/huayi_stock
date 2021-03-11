# coding=utf-8
# @Time：2021/3/1 17:00
# @Author:jia
# @File:urls.py
# @Software:PyCharm
from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    # url(r'^image_codes/(?P<uuid>[\w-]+)/$',views.ImageCodeView.as_view()),
    url(r'^index/$',views.IndexView.as_view(),name='index'),
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    url(r'^test$',views.TestView.as_view()),
    url(r'^logout$',views.LoginView.as_view(),name='logout'),
    url(r'^$',views.LoginView.as_view()),

]
