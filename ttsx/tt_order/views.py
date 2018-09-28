# coding=utf-8
import time
from models import *
from tt_cart.models import *
from tt_user.models import *
from tt_goods.models import *
from django.db import transaction
from tt_user import user_decorator
from django.shortcuts import render
from django.http import JsonResponse


@user_decorator.login
def orderInfo(request,id,count):
    """
    根据购物车提交的信息显示订单提交页的信息
    id和count 为直接从商品详情页跳转来的　商品id和数量
    """
    content = {}; content["title"] = "天天生鲜－提交订单" # 初始化数据字典
    user_id = request.session.get("id",default=None)    # 获取用户信息
    content["user"] = UserInfo.objects.get(id=user_id)
    if (not id) and (not count):                        # 没有商品id代表从购物车跳转的
        data = request.GET                              # 从购物车数据库根据id获取信息并返回
        content["carts"] = [CartInfo.objects.get(id=data[i]) for i in data]
        content["active"] = 1
    else:                                               # 有商品id代表从商品详情页跳转的
        content["goods"] = Goods.objects.get(id=id)     # 根据id查到商品组合成数据
        content["count"] = count; content["active"] = 2
    return render(request,"tt_order/order.html",content)


@user_decorator.login
@transaction.atomic()                                   # 使用事务执行数据库操作
def ordercl(request,id):
    """后台提交购物车时订单时处理的视图"""
    tran_id = transaction.savepoint()                   # 设置事务的起始点
    user_id = request.session.get("id",default=None)    # 查询用户信息
    user = UserInfo.objects.get(id=user_id)
    oid = "".join(str(time.time()).split("."))          # 使用time.time生成一个订单号
    oid = oid+"0" if len(oid) == 11 else oid
    try:                                                # 生成数据库中订单信息
        order = OrderInfo(); order.oid = oid
        order.ouser = user; order.ozrmb = 10
        order.oaddress = (u"%s ( %s 收) %s" %(user.uadder,user.ushou,user.utel)).encode('utf-8')
        order.save()
        if not id:                                      # 代表从购物车转过来的订单
            data = request.POST                         # 获取购物车id列表
            for i in data:                              # 遍历提交的购物车id
                if i.startswith("cart"):                # 数据以cart开头代表订单id
                    order_goods = OrderGoods()          # 生成购买商品详表模型
                    cart = CartInfo.objects.get(id=data[i])# 获取购物车对象
                    if cart.cgoods.gkucun < cart.count: # 如果订单数量大于库存数量　
                        transaction.savepoint_rollback(tran_id)# 回滚事务
                        return JsonResponse({"data":0}) # 返回未提交成功
                    order_goods.ogoods = cart.cgoods    # 关联商品表
                    order_goods.orderinfo = order       # 关联订单表
                    order_goods.ogrmb = cart.cgoods.grmb# 商品单价
                    order_goods.ocount = cart.count     # 购买数量
                    order.ozrmb += cart.cgoods.grmb * cart.count# 更新订单总金额
                    goods_info = cart.cgoods            # 获取商品表对象
                    goods_info.gkucun -= cart.count     # 从商品库存中减去订单中商品数量
                    goods_info.save()                   # 执行修改商品表库存
                    cart.delete()                       # 删除购物车中的信息
                    order.save()                        # 执行修改订单总金额
                    order_goods.save()                  # 执行增加订单详表数据
        elif id == "1":                                 # 代表从商品详情页转来的订单
            goodsid = request.POST["id"]                # 获取商品id
            count = int(request.POST["count"])          # 获取购买商品数量
            goodsinfo = Goods.objects.get(id=goodsid)   # 获取商品信息
            if count > goodsinfo.gkucun:                # 如果订单数量大于库存数量　则返回未提交成功
                transaction.savepoint_rollback(tran_id) # 回滚事务
                return JsonResponse({"data": 0})        # 返回未提交成功
            else :
                order_goods = OrderGoods()              # 生成购买商品详表模型
                order_goods.ogoods = goodsinfo          # 关联商品表
                order_goods.orderinfo = order           # 关联订单表
                order_goods.ogrmb = goodsinfo.grmb      # 商品单价
                order_goods.ocount = count              # 购买数量
                order.ozrmb += goodsinfo.grmb * count   # 更新订单总金额
                goodsinfo.gkucun -= count               # 从商品库存中减去订单中商品数量
                goodsinfo.save()                        # 执行修改商品表库存
                order.save()                            # 执行修改订单总金额
                order_goods.save()                      # 执行增加订单详表数据
        transaction.savepoint_commit(tran_id)           # 执行事务
    except Exception as e:
        print(e); transaction.savepoint_rollback(tran_id)# 回滚事务
        return JsonResponse({"data":0})
    return JsonResponse({"data":1})


