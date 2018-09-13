#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db import transaction
from tt_user.models import *
from tt_user import user_decorator
from tt_cart.models import *
from tt_goods.models import *
from models import *
import time


@user_decorator.login
# 根据购物车提交的信息显示订单提交页的信息
# id和count 为直接从商品详情页跳转来的　商品id和数量
def orderInfo(request,id,count):
    content = {}
    content["title"] = "天天生鲜－提交订单"
    username = request.session.get("user")
    user = UserInfo.objects.get(uname=username)
    content["user"] = user
    if id == "":  # 没有商品id代表从购物车跳转的
        data = request.GET
        carts = []
        # 从购物车数据库根据id获取信息并返回
        for i in data:
            cart = CartInfo.objects.get(id=data[i])
            carts.append(cart)
        content["carts"] = carts
        content["active"] = 1
    else: # 有商品id代表从商品详情页跳转的
        content["active"] = 2
        goods = Goods.objects.get(id=id)
        content["goods"] = goods
        content["count"] = count
    return render(request,"tt_order/order.html",content)


@user_decorator.login
@transaction.atomic()
# 登录验证　使用事务执行数据库操作
# 后台提交购物车时订单时处理的视图
def ordercl(request,id):
    # 设置事务的起始点
    tran_id = transaction.savepoint()
    username = request.session.get("user")
    user = UserInfo.objects.get(uname=username)
    # 使用time.time生成一个订单号
    oid = "".join(str(time.time()).split("."))
    try:  # 生成数据库中订单信息
        order = OrderInfo()
        order.oid = oid
        order.ouser = user
        order.oaddress = "%s （ %s 收） %s" %(user.uadder,user.ushou,user.utel)
        order.ozrmb = 10
        order.save()
        if id == "": # 代表从购物车转过来的订单
            # 遍历提交的购物车id　生成数据库中订单的详细商品信息
            data = request.POST
            for i in data:
                goods = OrderGoods()
                order = OrderInfo.objects.get(oid=oid)
                cart = CartInfo.objects.get(id=data[i])
                # 如果订单数量大于库存数量　则返回未提交成功
                if cart.cgoods.gkucun < cart.count:
                    # 回滚事务
                    transaction.savepoint_rollback(tran_id)
                    return JsonResponse({"data":0})
                else:
                    goods.ogoods = cart.cgoods
                    goods.orderinfo = order
                    goods.ogrmb = cart.cgoods.grmb
                    goods.ocount = cart.count
                    # 更新订单总金额
                    order.ozrmb += cart.cgoods.grmb * cart.count
                    # 从商品库存中减去订单中商品数量
                    goodsinfo = Goods.objects.get(id=cart.cgoods.id)
                    goodsinfo.gkucun -= cart.count
                    goodsinfo.save()
                    # 删除购物车中的信息
                    cart.delete()
                    order.save()
                    goods.save()
        elif id == "0": # 代表从商品详情页转来的订单
            goodsid = request.POST["id"]
            count = int(request.POST["count"])
            goodsinfo = Goods.objects.get(id=goodsid)
            if count > goodsinfo.gkucun:
                # 如果订单数量大于库存数量　则返回未提交成功
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({"data": 0})
            else :
                goods = OrderGoods()
                order = OrderInfo.objects.get(oid=oid)
                goods.ogoods = goodsinfo
                goods.orderinfo = order
                goods.ogrmb = goodsinfo.grmb
                goods.ocount = count
                # 更新订单总金额
                order.ozrmb += goodsinfo.grmb * count
                # 从商品库存中减去订单中商品数量
                goodsinfo.gkucun -= count
                goodsinfo.save()
                order.save()
                goods.save()
        # 执行事务
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print(e)
        # 出现异常则回滚事务
        transaction.savepoint_rollback(tran_id)
        return JsonResponse({"data":0})
    return JsonResponse({"data":1})


