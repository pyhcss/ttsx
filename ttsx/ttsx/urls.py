# coding=utf-8
"""ttsx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),          # 后台模块
    url(r"^user/",include("tt_user.urls")),             # 用户模块
    url(r"^tinymce/",include("tinymce.urls")),          # 富文本编辑器
    url(r"^",include("tt_goods.urls")),                 # 主页
    url(r"^goods/",include("tt_goods.urls")),           # 商品模块
    url(r"^cart/",include("tt_cart.urls")),             # 购物车模块
    url(r"^order/",include("tt_order.urls")),           # 订单模块
    url(r'^captcha/', include('captcha.urls')),         # 验证码模块
]
