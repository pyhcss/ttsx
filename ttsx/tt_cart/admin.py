#coding=utf-8
from django.contrib import admin
import models


class CartAdmin(admin.ModelAdmin):
    # 列表页显示的属性
    list_display = ["id","cuser","count"]
    # 过滤条件
    list_filter = ["cgoods"]
    # 搜索框字段
    search_fields = ["cuser"]
    # 每页显示数据量
    list_per_page = 20


admin.site.register(models.CartInfo,CartAdmin)
