#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from hashlib import sha1
from models import *
import redis,base64


# 跳转到注册界面
def register(request):
    content = {"title":"天天生鲜－注册"}
    return render(request,"tt_user/register.html",content)


# 用户名预处理　是否注册过
def nameycl(request,name):
    num = UserInfo.objects.filter(uname=name).count()
    return JsonResponse({"data":num})


# 注册页提交用户数据
def register_cl(request):
    post = request.POST
    uname = post["user_name"]
    upwd = post["pwd"]
    upwd2 = post["cpwd"]
    uemail = post["email"]

    # 使用sha1加密
    s = sha1()
    s.update(upwd)
    upwd3 = s.hexdigest()

    # 创建数据库模型对象并写入
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    return redirect("/user/login")


# 跳转到登录界面
def login(request):
    user = request.session.get('user', default=None)
    if user != None:
        return redirect("/user/centerinfo")
    cookie = request.COOKIES
    uname = ""
    if cookie.has_key("uname"):
        uname = cookie["uname"]
    content = {"title":"天天生鲜－登录","uname":uname}
    return render(request,"tt_user/login.html",content)


# 用户登录页密码对比
def pwd_cl(request):
    name = request.POST["name"]
    pwd = request.POST["pwd"]
    data = None
    try:
        user = UserInfo.objects.get(uname=name)
        pwd2 = user.upwd
        s = sha1()
        s.update(pwd)
        pwd3 = s.hexdigest()
        if pwd2 != pwd3:
            data = 0
        elif pwd2 == pwd3 and name == user.uname:
            data = 1
            # 保存登录信息到session
            request.session['user'] = name
            request.session.set_expiry(0)
            # request.session.clear_expired()
    except Exception as e:
        print(e)
    return JsonResponse({'data':data})


# 用户登录时处理记住用户名
def cookie(request,name):
    response = HttpResponse()
    if name != "":
        response.set_cookie("uname",name,max_age=1209600)
    else:
        response.set_cookie("uname",name, max_age=-1)
    return response


# 跳转到用户中心 个人信息
def centerInfo(request):
    user = request.session.get('user',default=None)
    content = {}
    if user == None:
        return redirect("/user/login")
    else:
        user = UserInfo.objects.get(uname=user)
        content["title"] = "天天生鲜－用户中心"
        content["user"] = user
        content['active'] = 1
        content['supername'] = user.uname
    return render(request,"tt_user/user_center_info.html",content)


# 跳转到用户中心　收货地址
def centerSite(request):
    user = request.session.get("user",default=None)
    content = {}
    if user == None:
        return redirect("/user/login")
    else:
        if request.method == 'GET':
            user = UserInfo.objects.get(uname = user)
            content["title"] = "天天生鲜－用户中心"
            content["user"] = user
            content['active'] = 3
            content['supername'] = user.uname
            return render(request,"tt_user/user_center_site.html",content)
        else:
            newuser = UserInfo.objects.get(uname=user)
            newuser.uadder = request.POST["uaddr"]
            newuser.ushou = request.POST["uname"]
            newuser.uyoubian = request.POST["uyoub"]
            newuser.utel = request.POST["utel"]
            newuser.save()
            return redirect("/user/centersite")


# 跳转到用户中心　全部订单
def centerOrder(request):
    user = request.session.get("user", default=None)
    content = {}
    if user == None:
        return redirect("/user/login")
    else:
        user = UserInfo.objects.get(uname = user)
        content['supername'] = user.uname
        content["title"] = "天天生鲜－用户中心"
        content['active'] = 2
    return render(request,"tt_user/user_center_order.html",content)


# 注销登录
def zhuxiao(request):
    user = request.session.get("user", default=None)
    re = redis.StrictRedis()
    rekey = re.keys()
    for i in rekey:
        try:
            jm = base64.b64decode(re.get(i))
            newjm = jm[41:]
            jm = eval(newjm)
            if jm["user"] == user:
                re.delete(i)
        except:
            continue
    return redirect("/")
