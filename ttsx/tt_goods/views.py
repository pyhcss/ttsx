# coding=utf-8
from django.shortcuts import render
from tt_user.models import *
from tt_cart.models import *
from models import *
from django.core.paginator import Paginator


# 主页
def index(request):
    content = {}
    # 判断用户是否登录
    user = request.session.get('user', default=None)
    try:
        user = UserInfo.objects.get(uname=user)
    except Exception as e:
        print(e)
        content['user'] = None
    else:
        content['user'] = user
        num = CartInfo.objects.filter(cuser=user).count()
        content['count'] = num
    typelist = TypeGoods.objects.filter(isDelete=False)
    # 查询所有商品分类
    goods1 = typelist[0].goods_set.filter(isDelete=False).order_by("-id")[:4]
    # 按最新商品传递四个商品 变量不带0
    goods01 = typelist[0].goods_set.filter(isDelete=False).order_by("-gliulan")[:4]
    # 按点击量最高传递四个商品　变量带0
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
    content["title"] = "天天生鲜－首页"
    content["show"] = 1  # show 页面显示方式
    return render(request,"tt_goods/index.html",content)


# 商品列表页　type代表分类　px代表按什么排序 xh代表取出第几页
def goodslist(request,type,px,xh):
    type = int(type)
    content = {}
    # 判断用户是否登录
    user = request.session.get('user', default=None)
    try:
        user = UserInfo.objects.get(uname=user)
    except Exception as e:
        print(e)
        content['user'] = None
    else:
        content['user'] = user
        num = CartInfo.objects.filter(cuser=user).count()
        content['count'] = num
    content["title"] = "天天生鲜－商品列表"
    content["show"] = 2 # show 页面显示方式
    typelist = TypeGoods.objects.filter(isDelete=False) # 获取所有商品列表
    newgoods = typelist[type-1].goods_set.filter(isDelete=False).order_by("-id")[:2]
    # 按分类查询最新的两条商品并传递
    content["newgoods"] = newgoods
    if px == "1":  # 判断排序类型
        goods = typelist[type-1].goods_set.filter(isDelete=False).order_by("-id")
    elif px == "2":
        goods = typelist[type-1].goods_set.filter(isDelete=False).order_by("grmb")
    elif px == "3":
        goods = typelist[type-1].goods_set.filter(isDelete=False).order_by("-gliulan")
    # 按排序方式和类别查询商品
    paginator = Paginator(goods,10)      # 返回一个分页对象
    goodsdata = paginator.page(int(xh))  # 取出分页对象对应的页码参数的数据
    content["goods"] = goodsdata         # 传递当前页面数据
    content["paixu"] = px                # 传递当前页面排序方式
    content["type"] = typelist[type-1]   # 传递当前页面所属分类的对象
    return render(request,"tt_goods/list.html",content)


def detail(request,id):
    id = int(id)
    content = {}
    # 判断用户是否登录
    user = request.session.get('user', default=None)
    try:
        user = UserInfo.objects.get(uname=user)
    except Exception as e:
        print(e)
        content['user'] = None
    else:
        content['user'] = user
        num = CartInfo.objects.filter(cuser=user).count()
        content['count'] = num
    # 记录用户点击量　修改数据
    goods = Goods.objects.get(pk=id)
    goods.gliulan = goods.gliulan + 1
    goods.save()
    content["goods"] = goods # 传递当前商品信息
    content["title"] = "天天生鲜－商品详情"
    content["show"] = 2 # show 页面显示方式
    # 传递两个最新商品
    newgoods = Goods.objects.filter(isDelete=False).order_by("-id")[:2]
    content["newgoods"] = newgoods
    response = render(request,"tt_goods/detail.html",content)
    # 用cookie记录用户的浏览记录
    cookie = request.COOKIES.get("liulan","")   # 获取cookie中的浏览信息
    if cookie == "":                            # 如果浏览信息为空、则直接添加
        liulanstr = "%s"%goods.id
    else:
        liulan = cookie.split("-")              # 把字符串分割成列表
        if liulan.count("%s"%goods.id) >= 1 :   # 判断列表中是否已经有这个商品id
            liulan.remove("%s"%goods.id)
        liulan.insert(0,"%s"%goods.id)          # 把商品id添加到列表第一个元素
        if len(liulan) >= 6:                    # 判断列表是否大于６
            del liulan[-1]
        liulanstr ="-".join(liulan)             # 用字符串拼接列表
    response.set_cookie("liulan",liulanstr,None)# 设置cookie
    return response


def user(request,count):
    user = request.session.get('user', default=None)
    if count == "":
        try:
            user = UserInfo.objects.get(uname=user)
        except Exception as e:
            print(e)
            return None
        else:
            return user
    elif count != "":
        try:
            user = UserInfo.objects.get(uname=user)
            cartcount = CartInfo.objects.filter(cuser=user).count()
        except Exception as e:
            print(e)
            return 0
        else:
            return cartcount


from haystack.views import SearchView
class MySearchViews(SearchView):
    def extra_context(self):
        content = super(MySearchViews,self).extra_context()
        content["title"] = "天天生鲜－搜索"
        content["show"] = 2
        content["user"] = user(self.request,"")
        content["count"] = user(self.request,1)
        newgoods = Goods.objects.filter(isDelete=False).order_by("-id")[:2]
        content["newgoods"] = newgoods
        return content