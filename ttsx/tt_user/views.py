#coding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *

# 返回注册界面
def register(request):
    content = {"title":"天天生鲜－注册"}
    return render(request,"tt_user/register.html",content)

# 提交用户数据
def register_cl(request):
    post = request.POST
    uname = post["user_name"]
    upwd = post["pwd"]
    upwd2 = post["cpwd"]
    uemail = post["email"]
    # 如果密码不正确　返回到注册页面
    if upwd != upwd2:
        return redirect("/user/register")
    if uname == "" or upwd == "" or uemail == "":
        return redirect("/user/register")
    # 使用sha1加密
    s = sha1()
    s.update(upwd)
    upwd3 = s.hexdigest()
    # 创建数据库模型并写入
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    return redirect("/user/login")

def login(request):
    content = {"title":"天天生鲜－登录"}
    return render(request,"tt_user/login.html",content)
def login_cl(request):
    post = request.POST
    uname = post["username"]
    upwd = post["pwd"]
    if uname == "" or upwd == "":
        return redirect("/user/login")
    # 从数据库获取密码
    try:
        user = UserInfo.objects.get(uname=uname)
    except:
        return redirect("/user/login")
    else:
        upwd2 = user.upwd
    # sha1加密用户输入密码
    s = sha1()
    s.update(upwd)
    upwd3 = s.hexdigest()
    if upwd2 != upwd3:
        return redirect("/user/login")
    return redirect("/user/centerInfo")

def centerInfo(request):
    render(request,"tt_user/user_center_info.html")
