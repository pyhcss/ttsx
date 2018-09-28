# coding=utf-8
import views
from django.conf.urls import url

urlpatterns = [
    url(r"^orderinfo/?(\d*)/?(\d*)$",views.orderInfo),              # 提交订单页面
    url(r"^ordercl/?(\d*)$",views.ordercl),                         # 订单处理
]
