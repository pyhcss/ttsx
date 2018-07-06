#coding=utf-8
from django.contrib import admin
import models


class GoodsAdmin(admin.ModelAdmin):
    list_display = ["id","gname","gliulan"]
    list_filter = ["isDelete"]
    search_fields = ["gname"]
    list_per_page = 20
    fieldsets = [("基本信息",{"fields":["gname","grmb","gdanwei","gkucun","isDelete"]}),
                 ("商品情况",{"fields":["typegoods","gimg","gjianjie","gliulan"]}),
                 ("详细介绍",{"fields":["gjieshao"]})]


class TypeAdmin(admin.ModelAdmin):
    list_display = ["id", "ttitle"]
    list_filter = ["isDelete"]
    search_fields = ["ttitle"]
    list_per_page = 20

admin.site.register(models.TypeGoods,TypeAdmin)
admin.site.register(models.Goods,GoodsAdmin)

