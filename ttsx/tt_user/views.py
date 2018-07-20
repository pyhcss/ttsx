#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from hashlib import sha1
from models import *
from tt_goods.models import *
from tt_order.models import *
import redis,base64,user_decorator,forms


# 用户名预处理　是否注册过
def nameycl(request,name):
    num = UserInfo.objects.filter(uname=name).count()
    return JsonResponse({"data":num})


# 注册页
def register(request):
    context = {}
    context["title"] = "天天生鲜－注册"
    if request.method == "GET":  # 如果请求方式是GET请求　代表请求注册页面
        context["post"] = None   # 初始化模板post参数为None
        context["captcha"] = forms.Check_Code()  # 传递验证码
        return render(request, "tt_user/register.html", context)
    else:                        # 如果请求方式是POST请求　代表请求注册数据
        try:
            form = forms.Check_Code(request.POST)  # 判断验证码的对错
            fbool = form.is_valid()
        except Exception as e:
            print(e)             # 出现异常则非正常请求　默认验证码错误
            fbool = False
        if fbool == True:        # 如果验证码正确　接受用户参数
            post = request.POST
            uname = post["user_name"]
            upwd = post["pwd"]
            upwd2 = post["cpwd"]
            uemail = post["email"]
            count = UserInfo.objects.filter(uname=uname).count()
            # 出现以下情况一般为非正常请求　直接重新返回模板
            if count != 0 or len(uname) < 5 or len(uname) > 20 or\
                    len(upwd) < 8 or len(upwd) >20 or upwd != upwd2 or\
                    uname == "" or upwd == "" or upwd2 == "" or\
                    uemail == "":
                return render(request,"tt_user/register.html",context)
            else:
                s = sha1()          # 使用sha1加密
                s.update(upwd)
                upwd3 = s.hexdigest()

                user = UserInfo()   # 创建数据库模型对象并写入
                user.uname = uname
                user.upwd = upwd3
                user.uemail = uemail
                user.save()
                return redirect("/user/login")
        else:                       # 如果验证码错误　返回模板并提示验证码错误
            context["post"] = request.POST
            context["captcha"] = forms.Check_Code()
            context["errorcode"] = 1
            return render(request, "tt_user/register.html", context)


# 跳转到登录界面
def login(request):
    uname = ""                          # 初始化用户名输入框为空
    context = {}                        # 初始化字典对象
    cookie = request.COOKIES            # 接收一个cookie对象
    if cookie.has_key("uname"):
        uname = cookie["uname"]         # 判断用户本地cookie是否有用户名信息
    url = cookie.get("url","/")         # 提取用户储存的url信息
    context["title"] = "天天生鲜－登录"
    context["uname"] = uname            # 如果用户本地有用户名信息则传递到模板
    context["captcha"] = forms.Check_Code()     # 生成验证码传递到模板
    if request.method == "GET":         # 如果get请求方式则代表用户请求页面信息
        user = request.session.get('user', default=None)
        if user != None:                # 如果用户已经登录则限制再次登录
            rspred = HttpResponseRedirect(url)
            if cookie.has_key("url"):   # 如果用户有储存url 则删除url的cookie信息
                rspred.set_cookie("url","",max_age=-1)
            return rspred               # 如果已经登录则跳转到其他页面
        # 如果用户没有登录则返回页面模板信息
        return render(request,"tt_user/login.html",context)
    else:                               # 如果post请求方式则代表用户请求登录
        try:
            form = forms.Check_Code(request.POST)
            fbool = form.is_valid()     # 判断验证码的对错
        except Exception as e:
            print(e)                    # 出现异常则非正常请求　默认验证码错误
            fbool = False
        if fbool == True:               # 如果验证码正确　接受用户参数
            name = request.POST["username"]
            pwd = request.POST["pwd"]
            try:                        # 使用sha1加密用户传入信息 与数据库对比
                user = UserInfo.objects.get(uname=name)
                pwd2 = user.upwd
                s = sha1()
                s.update(pwd)
                pwd3 = s.hexdigest()
                if pwd2 != pwd3:        # 如果密码不正确　返回页面并给出提示
                    context["error_user"] = True
                    return render(request,"tt_user/login.html",context)
                elif pwd2 == pwd3 and name == user.uname:
                    request.session['user'] = name  # 保存登录信息到session
                    request.session.set_expiry(0)
                    rspred = HttpResponseRedirect(url)
                    # 如果用户有储存url 则删除url的cookie信息
                    if cookie.has_key("url"):
                        rspred.set_cookie("url", "", max_age=-1)
                    return rspred
            except Exception as e:
                print(e)                # 出现异常一般为非正常访问　返回页面
                context["error_user"] = True
                return render(request, "tt_user/login.html", context)
        else:                           # 如果验证码错误　返回页面并提示
            context["error_code"] = True
            return render(request,"tt_user/login.html",context)


# 用户登录时处理记住用户名
def cookie(request,name):
    response = HttpResponse()
    if name != "":
        response.set_cookie("uname",name,max_age=1209600)
    else:
        response.set_cookie("uname",name, max_age=-1)
    return response


# 跳转到用户中心 个人信息 装饰器为登录验证
@user_decorator.login
def centerInfo(request):
    user = request.session.get('user',default=None)
    content = {}
    user = UserInfo.objects.get(uname=user)
    content["title"] = "天天生鲜－用户中心"
    content["user"] = user
    content['active'] = 1
    cookie = request.COOKIES.get("liulan",None) # 接收cookie中的最近浏览信息
    liulanlist = []
    if cookie != None:
        liulan = cookie.split("-")              # 分割字符串、返回列表
        for i in liulan:
            goods = Goods.objects.get(id=i)     # 拿到id对应的商品并构成列表返回
            liulanlist.append(goods)
    content["liulan"] = liulanlist
    return render(request,"tt_user/user_center_info.html",content)


# 跳转到用户中心　收货地址 装饰器为登录验证
@user_decorator.login
def centerSite(request):
    user = request.session.get("user",default=None)
    content = {}
    if request.method == 'GET':  # 如果是get提交、是来获取信息的
        user = UserInfo.objects.get(uname = user)
        content["title"] = "天天生鲜－用户中心"
        content["user"] = user
        content['active'] = 3
        return render(request,"tt_user/user_center_site.html",content)
    else:                        # 如果是POST提交、是来修改信息的
        newuser = UserInfo.objects.get(uname=user)
        newuser.uadder = request.POST["uaddr"]
        newuser.ushou = request.POST["uname"]
        newuser.uyoubian = request.POST["uyoub"]
        newuser.utel = request.POST["utel"]
        newuser.save()
        return redirect("/user/centersite")


# 跳转到用户中心　全部订单 装饰器为登录验证
@user_decorator.login
def centerOrder(request,id):
    print(id)
    user = request.session.get("user", default=None)
    content = {}
    user = UserInfo.objects.get(uname = user)
    content['user'] = user
    content["title"] = "天天生鲜－用户中心"
    content['active'] = 2
    content["order"] = None
    try:                            # 拿到用户的订单　分页返回
        order = OrderInfo.objects.filter(ouser=user)
        paginator = Paginator(order,2)
        if id == "":
            id = 1
        page = paginator.page(int(id))
        content["order"] = page
    except Exception as e:
        print(e)
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
