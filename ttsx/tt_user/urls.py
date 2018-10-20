# coding=utf-8
import views
from django.conf.urls import url

urlpatterns = [
    url("^register$",views.register),               # 注册
    url("^nameycl/(\w+)$",views.nameycl),           # 用户名预处理
    url("^login$",views.login),                     # 登录
    url("^cookie/(\w*)",views.cookie),              # 登录时记住用户名
    url("^centerinfo$",views.centerInfo),           # 个人信息页
    url("^centersite$",views.centerSite),           # 收货地址页
    url("^centerorder/?(\d*)$",views.centerOrder),  # 个人订单页
    url("^logout$",views.logOut),                   # 注销
    url("^updatepwd$",views.update_pwd),            # 忘记密码
    url("^emailcode$",views.email_code),            # 邮箱验证码接口
]