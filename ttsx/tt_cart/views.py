#coding=utf-8
from django.shortcuts import render,redirect
from tt_user import user_decorator
from tt_user.models import *
from tt_goods.models import *
from models import *
from django.http import JsonResponse,HttpResponseRedirect


# 执行登录验证
@user_decorator.login
def cartInfo(request):
    username = request.session.get("user")
    user = UserInfo.objects.get(uname=username)
    carts = CartInfo.objects.filter(cuser=user)
    content={}
    content["carts"] = carts
    content["user"] = user
    return render(request,"tt_cart/cart.html",content)


# 执行登录验证
@user_decorator.login
def cartadd(request,userid,goodsid,count):
    if userid == '0' and count == '0':
        return redirect("/goods/detail/"+goodsid)
    user = UserInfo.objects.get(id=int(userid))
    goods = Goods.objects.get(id=int(goodsid))
    try:
        usercart = CartInfo.objects.get(cuser=user,cgoods=goods)
    except Exception as e:
        print(e)
        cart = CartInfo()
        cart.cuser = user
        cart.cgoods = goods
        cart.count = int(count)
        cart.save()
    else:
        usercart.count += int(count)
        usercart.save()
    num = CartInfo.objects.filter(cuser=user).count()
    return JsonResponse({'data':num})


@user_decorator.login
def revcart(request,userid,goodsid,count):
    user = UserInfo.objects.get(id=int(userid))
    goods = Goods.objects.get(id=int(goodsid))
    usercart = CartInfo.objects.get(cuser=user, cgoods=goods)
    if int(count) == 0:
        usercart.delete()
        return redirect("/cart/cartinfo")
    else :
        usercart.count = int(count)
        usercart.save()
        return JsonResponse({"data":1})
