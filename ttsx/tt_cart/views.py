# coding=utf-8
from models import *
from tt_user.models import *
from tt_goods.models import *
from tt_user import user_decorator
from django.http import JsonResponse
from django.shortcuts import render,redirect


@user_decorator.login
def cartInfo(request):
    """购物车页面"""
    content={}                                              # 初始化数据字典
    username = request.session.get("user",default=None)     # 获取用户信息
    user_id = request.session.get("id",default=None)
    content["carts"] = CartInfo.objects.filter(cuser=user_id)# 获取购物车模型中储存的信息
    content["user"] = {"uname":username,"id":user_id}
    content["title"] = "天天生鲜－购物车"
    return render(request,"tt_cart/cart.html",content)      # 渲染模板返回信息


@user_decorator.login
def updateCart(request,type,userlogin,goodsid,count):
    """更新购物车数据 更新类型 是否登录 商品id　商品数量"""
    if userlogin == '0':                                    # 如果用户未登录跳转到商品详情页面
        return redirect("/goods/detail/"+goodsid)
    try:
        goods = Goods.objects.get(id=int(goodsid))          # 查询商品数据
        user_id = request.session.get("id",default=None)    # 查询用户数据
        user = UserInfo.objects.get(id=user_id) if user_id else None
    except Exception as e:
        print e; return JsonResponse({'data': 0})
    if (not goods) or (not user) or int(count) > goods.gkucun:# 如果用户数据为空或者商品数据为空或者数量大于库存
        return JsonResponse({'data': 0})
    try:                                                    # 根据异常判断是不是已经存过该用户的该商品
        usercart = CartInfo.objects.get(cuser=int(user.id),cgoods=int(goods.id))
    except Exception as e:                                  # 如果有异常则没存过 新增
        if type == "add":                                   # 如果类型是增加
            cart = CartInfo()                               # 实例化模型对象
            cart.cuser = user; cart.cgoods = goods          # 增加数据信息
            cart.count = int(count); cart.save()
        else:
            return JsonResponse({'data': 0})
    else:                                                   # 如果没有异常则直接修改该数量
        if type == "add":                                   # 如果类型是增加 在原数据基础上变更
            usercart.count += int(count)
            if usercart.count > goods.gkucun:               # 判断增加后的数据是否大于库存
                return JsonResponse({'data': 0})
            usercart.save()
        elif type == "update" and count == "0":             # 如果类型是更新且数量为0
            usercart.delete()                               # 删除数据
            return redirect("/cart/cartinfo")
        elif type == "update":                              # 如果类型是更新
            usercart.count = int(count)                     # 直接变更原数据
            usercart.save()
            return redirect("/cart/cartinfo")
        else:
            return JsonResponse({'data': 0})
    num = CartInfo.objects.filter(cuser=int(user.id)).count()# 根据返回数量更新购物车图标的数字
    return JsonResponse({'data':num})