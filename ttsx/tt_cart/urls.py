# coding=utf-8
import views
from django.conf.urls import url

urlpatterns = [
    url(r"^cartinfo$",views.cartInfo),                              # 购物车信息页面
    url(r"^updatecart/(\w+)/(\d)/(\d+)/(-?\d+)$",views.updateCart), # 增加或修改购物车信息
]