# coding=utf-8
# @Time：2021/3/2 14:21
# @Author:jia
# @File:urls.py
# @Software:PyCharm
from django.conf.urls import url
from goods import views

urlpatterns = [
    url(r'^goodslist/$',views.GoodsListView.as_view(),name='goodslist'),
    url(r'^addgoods/$',views.AddGoodsView.as_view(),name='addgoods'),
    url(r'^addgoodstype/$',views.AddGoodstypeView.as_view(),name='addgoodstype'),
    url(r'^goodstype/$',views.GoodstypelistView.as_view(),name='goodstype'),
    url(r'^goodsinfo/(?P<goodsid>\d+)$',views.GoodsinfoView.as_view(),name='goodsinfo'),
    url(r'^delgoods/(?P<goodsid>\d+)$',views.DeletegoodsView.as_view(),name='delgoods'),
    url(r'^delgoodstype/(?P<typeid>\d+)$',views.DeletetypeView.as_view(),name='delgoodstype'),
    url(r'^tj$',views.TjView.as_view(),name='tj'),


]