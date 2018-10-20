# coding=utf-8

import hashlib,user_decorator,forms,random

from models import *
from tt_goods.models import *
from tt_order.models import *
from libs.send_email import sendemail
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect


def nameycl(request,name):
    """用户名预处理 是否注册过"""
    try:
        num = UserInfo.objects.filter(uname=name).count()
    except Exception as e:
        print e
        return JsonResponse({"data":1})
    else:
        return JsonResponse({"data":num})


def register(request):
    """注册页"""
    context = {}; context["title"] = "天天生鲜－注册"
    if request.method == "GET":                 # 如果请求方式是GET请求 代表请求注册页面
        context["user"] = None                  # 初始化模板user参数为None
        context["captcha"] = forms.Check_Code() # 传递验证码 直接返回模板
        return render(request, "tt_user/register.html", context)
    try:                                        # 如果请求方式是POST请求　代表请求注册数据
        form = forms.Check_Code(request.POST)   # 判断验证码的对错
        fbool = form.is_valid()
    except Exception as e:
        print(e)                                # 出现异常默认验证码错误
        fbool = False
    if fbool:                                   # 如果验证码正确　接受用户参数
        user = request.POST
        uname = user["user_name"]; upwd = user["pwd"]
        upwd2 = user["cpwd"]; uemail = user["email"]
        count = UserInfo.objects.filter(uname=uname).count()
                                                # 以下情况一般为非正常请求 重新返回模板
        if count != 0 or len(uname) < 5 or len(uname) > 20 or\
                len(upwd) < 8 or len(upwd) > 20 or upwd != upwd2 or\
                uname == "" or upwd == "" or upwd2 == "" or\
                uemail == "":
            context["user"] = None
            context["captcha"] = forms.Check_Code()
            return render(request,"tt_user/register.html",context)
        upwd3 = hashlib.sha1(upwd).hexdigest()  # 使用sha1加密
        user = UserInfo()                       # 创建数据库模型对象并写入
        user.uname = uname; user.upwd = upwd3
        user.uemail = uemail; user.save()
        return redirect("/user/login")
    else:                                       # 如果验证码错误　返回模板并提示验证码错误
        context["user"] = request.POST
        context["captcha"] = forms.Check_Code()
        context["errorcode"] = 1
        return render(request, "tt_user/register.html", context)


def login(request):
    """登录界面"""
    context = {}                                # 初始化字典对象
    cookie = request.COOKIES                    # 接收cookie对象
    uname = cookie.get("uname","")              # 判断cookie用户名信息
    url = cookie.get("url","/")                 # 提取cookie的url信息
    context["title"] = "天天生鲜－登录"
    context["uname"] = uname                    # 用户名信息传递到模板
    context["captcha"] = forms.Check_Code()     # 生成验证码传递到模板
    if request.method == "GET":                 # 如果get请求方式则代表用户请求页面信息
        user = request.session.get('user', default=None)
        if user:                                # 如果用户已经登录则限制再次登录
            rspred = HttpResponseRedirect(url)
            if cookie.has_key("url"):           # 如果cookie有储存url 则删除url的cookie信息
                rspred.set_cookie("url","",max_age=-1)
            return rspred                       # 如果已经登录则跳转到其他页面
                                                # 如果用户没有登录则返回页面模板信息
        return render(request,"tt_user/login.html",context)
    else:                                       # 如果post请求方式则代表用户请求登录
        try:
            form = forms.Check_Code(request.POST)
            fbool = form.is_valid()             # 判断验证码的对错
        except Exception as e:
            print(e)
            fbool = False                       # 出现异常默认验证码错误
        if fbool:                               # 如果验证码正确 接受用户参数
            name = request.POST["username"]; pwd = request.POST["pwd"]
            try:                                # 从数据库获取用户信息
                user = UserInfo.objects.get(uname=name)
            except Exception as e:
                print e                         # 出现异常返回用户名错误
                context["error_user"] = True
                return render(request, "tt_user/login.html", context)
            pwd2 = user.upwd                    # 调出数据库密码
            pwd3 = hashlib.sha1(pwd).hexdigest()# 使用sha1加密用户传入信息
            if pwd2 != pwd3:                    # 如果密码不正确　返回页面并给出提示
                context["error_user"] = True
                return render(request,"tt_user/login.html",context)
            elif pwd2 == pwd3 and name == user.uname:
                request.session['user'] = name  # 保存登录信息到session
                request.session["id"] = user.id
                request.session.set_expiry(60*60)# session有效期
                rspred = HttpResponseRedirect(url)
                                                # 如果用户有储存url 则删除url的cookie信息
                if cookie.has_key("url"):
                    rspred.set_cookie("url","",max_age=-1)
                return rspred
        else:                                   # 如果验证码错误　返回页面并提示
            context["error_code"] = True
            return render(request,"tt_user/login.html",context)


def cookie(request,name):
    """用户登录时处理记住用户名"""
    response = HttpResponse()
    if name:                                    # 如果参数不为空
        response.set_cookie("uname",name,max_age=1209600)
    else:
        response.set_cookie("uname",name, max_age=-1)
    return response


@user_decorator.login
def centerInfo(request):
    """跳转到用户中心 个人信息 """
    content = {}                                # 初始化数据字典
    user_id = request.session.get('id',default=None)
    user = UserInfo.objects.get(id=user_id)
    content["title"] = "天天生鲜－用户中心"
    content["user"] = user;content['active'] = 1# active 展示效果编号
    cookie = request.COOKIES.get("liulan",None) # 接收cookie中的最近浏览信息
    liulanlist = []
    if cookie :
        liulan = cookie.split("-")              # 分割字符串、返回列表
        liulanlist = [Goods.objects.get(id=i) for i in liulan]
    content["liulan"] = liulanlist              # 拿到id对应的商品并构成列表返回
    return render(request,"tt_user/user_center_info.html",content)


@user_decorator.login
def centerSite(request):
    """跳转到用户中心 收货地址 """
    content = {}                                # 初始化数据字典
    user_id = request.session.get("id",default=None)
    if request.method == 'GET':                 # 如果是get提交、是来获取信息的
        user = UserInfo.objects.get(id=user_id)
        content["title"] = "天天生鲜－用户中心"
        content["user"] = user
        content['active'] = 3                   # active 展示效果编号
        return render(request,"tt_user/user_center_site.html",content)
    else:                                       # 如果是POST提交、是来修改信息的
        user = UserInfo.objects.get(id=user_id)
        user.uadder = request.POST["uaddr"]
        user.ushou = request.POST["uname"]
        user.uyoubian = request.POST["uyoub"]
        user.utel = request.POST["utel"]
        user.save()
        return redirect("/user/centersite")


@user_decorator.login
def centerOrder(request,page):
    """跳转到用户中心　全部订单"""
    content = {}                                # 初始化数据字典
    user_id = request.session.get("id", default=None)
    user = request.session.get("user", default=None)
    content['user'] = {"uname":user}
    content["title"] = "天天生鲜－用户中心"
    content['active'] = 2; content["order"] = None
    try:                                        # 拿到用户的订单　分页返回
        order = OrderInfo.objects.filter(ouser=user_id).order_by("-oid")
        paginator = Paginator(order,2)          # 获取分页对象
        page_id = page if page else 1           # 没参数默认第一页
        page = paginator.page(int(page_id))     # 按参数获取页面
        content["order"] = page
    except Exception as e:
        print(e)
    return render(request,"tt_user/user_center_order.html",content)


@user_decorator.login
def logOut(request):
    """注销登录"""
    request.session.clear()
    return redirect("/")


def update_pwd(request):
    """忘记密码"""
    if request.method == "GET":                 # get请求返回模板
        content = {}; content["title"] = "天天生鲜－忘记密码"
        content["captcha"] = forms.Check_Code() # 传递图片验证码
        content["active"] = 4
        return render(request,"tt_user/user_update_pwd.html",content)
    try:                                        # post请求
        user_name = request.POST['name']        # 获取传递的参数
        captcha = request.POST['captcha']
        pwd = request.POST['pwd']
    except Exception as e:
        return JsonResponse({"errcode":1,"errmsg":"参数错误"})
    if len(pwd) < 8 or len(pwd) > 20:
        return JsonResponse({"errcode":1,"errmsg":"密码不能小于8位或大于20位"})
    try:                                        # 获取缓存中的验证码
        email_code = cache.get(user_name+"_email_code")
    except Exception as e:
        return JsonResponse({"errcode":2,"errmsg":"邮箱验证码已过期,请重新获取"})
    if email_code != captcha:
        return JsonResponse({"errcode": 2, "errmsg": "邮箱验证码错误,请重新获取"})
    user = UserInfo.objects.get(uname=user_name)# 获取用户信息
    user.upwd = hashlib.sha1(pwd).hexdigest()   # 修改用户信息
    user.save()
    return JsonResponse({"errcode":0, "errmsg": "密码修改成功,请直接使用新密码登录"})


def email_code(request):
    """发送邮箱验证码"""
    try:
        user_name = request.GET['username']     # 获取用户名
    except Exception as e:
        return JsonResponse({"errcode":1,"errmsg":"参数错误"})
    try:
        form = forms.Check_Code(request.GET)    # 判断验证码的对错
        fbool = form.is_valid()
    except Exception as e:
        return JsonResponse({"errcode":2,"errmsg":"验证码错误"})
    if not fbool:
        return JsonResponse({"errcode": 2, "errmsg": "验证码错误"})
    else:
        try:                                    # 从数据库获取用户
            user = UserInfo.objects.get(uname=user_name)
        except Exception as e:
            return JsonResponse({"errcode": 3, "errmsg": "该用户名未注册"})
        email = user.uemail                     # 查询用户邮箱
        code = str(random.randint(0,999999)).zfill(6)# 生成验证码
        cache.set(user_name+"_email_code",code,60*5)# 利用缓存储存验证码
        resp = sendemail(email,code)            # 发送邮件
        if resp == '发送成功':                   # 成功返回
            show_email = email[:3] + "***" + email[-8:]
            return JsonResponse({"errcode":0,"errmsg":show_email.decode('gbk').encode('utf-8')+'邮件发送成功'})
        else:                                   # 失败返回
            return JsonResponse({"errcode":4,"errmsg":"邮箱验证码发送失败,请稍后重试或联系管理员"})
