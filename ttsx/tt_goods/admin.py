#coding=utf-8
from django.contrib import admin
import models


class GoodsAdmin(admin.ModelAdmin):
    # 列表页显示的属性
    list_display = ["id","gname","gliulan"]
    # 过滤条件
    list_filter = ["isDelete"]
    # 搜索框字段
    search_fields = ["gname"]
    # 每页显示数据量
    list_per_page = 20
    # 修改页显示方式
    fieldsets = [("基本信息",{"fields":["gname","grmb","gdanwei","gkucun","isDelete"]}),
                 ("商品情况",{"fields":["typegoods","gimg","gjianjie","gliulan"]}),
                 ("详细介绍",{"fields":["gjieshao"]})]


class TypeAdmin(admin.ModelAdmin):
    # 列表页显示的属性
    list_display = ["id", "ttitle"]
    # 过滤条件
    list_filter = ["isDelete"]
    # 搜索框字段
    search_fields = ["ttitle"]
    # 每页显示数据量
    list_per_page = 20

admin.site.register(models.TypeGoods,TypeAdmin)
admin.site.register(models.Goods,GoodsAdmin)

