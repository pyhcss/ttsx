# coding=utf-8
import views
from views import *
from django.conf.urls import url

urlpatterns = [
    url("^$",views.index),                              # 主页
    url("^list/(\d)(\d)(\d+)",views.goodslist),         # 列表页
    url("^detail/(\d+)",views.detail),                  # 商品详情页
    url(r'^search/', MySearchViews()),                  # 搜索页
]