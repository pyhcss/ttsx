#coding=utf-8
from django.shortcuts import render,redirect
from tt_user import user_decorator
from tt_user.models import *
from tt_goods.models import *
from models import *
from django.http import JsonResponse,HttpResponseRedirect


# 执行登录验证
@user_decorator.login
# 跳转到购物车页面
def cartInfo(request):
    username = request.session.get("user")
    user = UserInfo.objects.get(uname=username)
    # 获取购物车模型中储存的信息并返回
    carts = CartInfo.objects.filter(cuser=user)
    content={}
    content["carts"] = carts
    content["user"] = user
    content["title"] = "天天生鲜－购物车"
    return render(request,"tt_cart/cart.html",content)


# 执行登录验证
@user_decorator.login
# 后台处理新增购物车信息
# 用户id 商品id　商品数量
def cartadd(request,userid,goodsid,count):
    # 用户添加购物车登录成功后继续转到商品页面
    if userid == '0' and count == '0':
        return redirect("/goods/detail/"+goodsid)
    # 根据用户id和商品id获取数据库信息
    user = UserInfo.objects.get(id=int(userid))
    goods = Goods.objects.get(id=int(goodsid))
    try:  #根据异常判断数据库是不是已经存过该用户的该商品
        usercart = CartInfo.objects.get(cuser=user,cgoods=goods)
    except Exception as e:  # 如果有异常则没存过　新增
        print(e)
        cart = CartInfo()
        cart.cuser = user
        cart.cgoods = goods
        cart.count = int(count)
        cart.save()
    else:  # 如果没有异常则直接修改该数量
        usercart.count += int(count)
        usercart.save()
    # 根据返回数量更新购物车图标的数字
    num = CartInfo.objects.filter(cuser=user).count()
    return JsonResponse({'data':num})


@user_decorator.login
# 在购物车中修改数量时后台异步修改或删除数据库数据
def revcart(request,userid,goodsid,count):
    user = UserInfo.objects.get(id=int(userid))
    goods = Goods.objects.get(id=int(goodsid))
    usercart = CartInfo.objects.get(cuser=user, cgoods=goods)
    if int(count) == 0:  # 如果商品数量是0则删除
        usercart.delete()
        return redirect("/cart/cartinfo")
    else :               # 否则是修改
        usercart.count = int(count)
        usercart.save()
        return JsonResponse({"data":1})


