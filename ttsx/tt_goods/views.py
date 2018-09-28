# coding=utf-8
from models import *
from tt_user.models import *
from tt_cart.models import *
from django.core.cache import cache
from haystack.views import SearchView
from django.core.paginator import Paginator
from django.shortcuts import render,redirect


def index(request):
    """主页"""
    try:
        content = cache.get("index_cache")                  # 从缓存中提取数据
    except Exception as e:                                  # 出现异常或者没有数据 初始化数据字典
        print e; content = {}
    content = content if content else {}
    content["user"] = getinfo(request,"user")               # 获取用户信息
    content['count'] = getinfo(request,"cart")              # 获取用户购物车数量
    if content.has_key("title"):                            # 如果缓存不为空
        return render(request,"tt_goods/index.html",content)
    else:                                                   # 如果缓存为空
        typelist = TypeGoods.objects.filter(isDelete=False) # 查询所有商品分类
                                                            # 按最新商品传递四个商品 变量不带0
        goods1 = typelist[0].goods_set.filter(isDelete=False).order_by("-id")[:4]
                                                            # 按点击量最高传递四个商品　变量带0
        goods01 = typelist[0].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
        goods2 = typelist[1].goods_set.filter(isDelete=False).order_by("-id")[:4]
        goods02 = typelist[1].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
        goods3 = typelist[2].goods_set.filter(isDelete=False).order_by("-id")[:4]
        goods03 = typelist[2].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
        goods4 = typelist[3].goods_set.filter(isDelete=False).order_by("-id")[:4]
        goods04 = typelist[3].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
        goods5 = typelist[4].goods_set.filter(isDelete=False).order_by("-id")[:4]
        goods05 = typelist[4].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
        goods6 = typelist[5].goods_set.filter(isDelete=False).order_by("-id")[:4]
        goods06 = typelist[5].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
        content["goods1"] = goods1;content["goods01"] = goods01
        content["goods2"] = goods2;content["goods02"] = goods02
        content["goods3"] = goods3;content["goods03"] = goods03
        content["goods4"] = goods4;content["goods04"] = goods04
        content["goods5"] = goods5;content["goods05"] = goods05
        content["goods6"] = goods6;content["goods06"] = goods06
        content["title"] = "天天生鲜－首页"; content["show"] = 1# show 页面显示方式
        try:
            cache.set("index_cache",content,60*60*2)        # 设置缓存
        except Exception as e:                              # 出现异常直接pass
            print e; pass
        return render(request,"tt_goods/index.html",content)


def goodslist(request,type,px,xh):
    """商品列表页 type:代表商品类别 px: 代表按什么排序 xh: 代表取出第几页"""
    try:
        content = cache.get("list_"+type+px+xh)             # 从缓存中提取数据
    except Exception as e:
        print e; content = {}                               # 出现异常或者没有数据 初始化数据字典
    content = content if content else {}
    content["user"] = getinfo(request,"user")               # 获取用户信息
    content['count'] = getinfo(request,"cart")              # 获取用户购物车数量
    if content.has_key("title"):                            # 如果缓存不为空 直接返回
        return render(request, "tt_goods/list.html", content)
    else:                                                   # 如果缓存为空
        goods_type = TypeGoods.objects.get(id=int(type))    # 获取商品类别
                                                            # 按分类查询最新的两条商品
        new_goods = goods_type.goods_set.filter(isDelete=False).order_by("-id")[:2]
        if px == "1":                                       # 判断排序类型 查询商品数据
            goods = goods_type.goods_set.filter(isDelete=False).order_by("-id")
        elif px == "2":
            goods = goods_type.goods_set.filter(isDelete=False).order_by("grmb")
        elif px == "3":
            goods = goods_type.goods_set.filter(isDelete=False).order_by("-gliulan")
        else:
            return redirect("/")
        content["newgoods"] = new_goods                     # 传递最新的两条商品对象
        paginator = Paginator(goods,10)                     # 传入所有商品返回一个分页对象
        goodsdata = paginator.page(int(xh))                 # 取出分页对象对应的页码参数的数据
        content["goods"] = goodsdata                        # 传递商品数据
        content["paixu"] = px                               # 传递当前页面排序方式
        content["type"] = goods_type                        # 传递当前页面所属分类对象
        content["title"] = "天天生鲜－商品列表"; content["show"] = 2# show 页面显示方式
        try:
            cache.set("list_"+type+px+xh,content,60*60*2)   # 添加缓存
        except Exception as e:
            print e; pass                                   # 出现异常直接pass
        return render(request,"tt_goods/list.html",content)


def detail(request,id):
    """商品详情页 商品id"""
    try:
        content = cache.get("detail_"+id)                   # 获取缓存信息
    except Exception as e:
        print e; content = {}                               # 出现异常或没有数据初始化数据字典
    content = content if content else {}
    content["user"] = getinfo(request,"user")               # 获取用户信息
    content['count'] = getinfo(request,"cart")              # 获取用户购物车数量
    goods = Goods.objects.get(pk=int(id))                   # 调出商品数据
    goods.gliulan = goods.gliulan + 1                       # 修改浏览量
    goods.save()
    content["goods"] = goods                                # 传递当前商品信息
    if content.has_key("title"):                            # 如果有缓存直接渲染模板
        response = render(request, "tt_goods/detail.html", content)
    else:                                                   # 如果没有缓存
        content["title"] = "天天生鲜－商品详情"; content["show"] = 2# show 页面显示方式
                                                            # 查询两个最新商品
        content["newgoods"] = Goods.objects.filter(isDelete=False).order_by("-id")[:2]
        try:
            cache.set("detail_"+id,content,60*60*2)         # 设置缓存
        except Exception as e:
            print e; pass                                   # 出现异常直接pass
        response = render(request,"tt_goods/detail.html",content)
    cookie = request.COOKIES.get("liulan","")               # 获取cookie中的浏览信息
    if not cookie:                                          # 如果浏览信息为空 则直接添加
        liulanstr = "%s"%int(id)
    else:
        liulan = cookie.split("-")                          # 把字符串分割成列表
        if liulan.count("%s"%int(id)) >= 1 :                # 如果列表中已经有这个商品id则删除
            liulan.remove("%s"%int(id))
        liulan.insert(0,"%s"%int(id))                       # 把商品id添加到列表第一个元素
        if len(liulan) >= 6:                                # 判断列表是否大于６
            del liulan[-1]                                  # 删除最后一个商品id
        liulanstr ="-".join(liulan)                         # 用字符串拼接列表
    response.set_cookie("liulan",liulanstr,None)            # 设置cookie
    return response


def getinfo(request,type):
    """查询用户名及购物车辅助函数"""
    user = request.session.get('user', default=None)
    user_id = request.session.get('id', default=None)
    if type == "user":                                      # 获取用户信息
        return {"uname":user,"id":user_id}
    elif type == "cart":                                    # 获取购物车数量信息
        return CartInfo.objects.filter(cuser=user_id).count() if user_id else 0


class MySearchViews(SearchView):
    """搜索视图"""
    def extra_context(self):
        content = super(MySearchViews,self).extra_context()
        content["title"] = "天天生鲜－搜索"                   # 设置标题
        content["show"] = 2                                 # 显示方式
        content["user"] = getinfo(self.request,"user")      # 获取用户名
        content["count"] = getinfo(self.request,"cart")     # 获取购物车数量
                                                            # 获取两条最新商品信息
        content["newgoods"] = Goods.objects.filter(isDelete=False).order_by("-id")[:2]
        return content