# coding=utf-8
from django.http import HttpResponseRedirect


def login(func):
    """登录验证装饰器"""
    def login_func(request,*args,**kwargs):
        user = request.session.get("user", default=None)
        if not user:
            rspred = HttpResponseRedirect("/user/login")
            rspred.set_cookie("url",request.get_full_path())
            return rspred
        else:
            return func(request,*args,**kwargs)
    return login_func