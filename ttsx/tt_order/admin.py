# coding=utf-8
import models
from django.contrib import admin


class OrderInfoAdmin(admin.ModelAdmin):
    # 列表页显示的属性
    list_display = ["oid","ouser","ozrmb"]
    # 过滤条件
    list_filter = ["oispay"]
    # 搜索框字段
    search_fields = ["oid"]
    # 每页显示数据量
    list_per_page = 20
    # 修改页显示方式


class OrderGoodsAdmin(admin.ModelAdmin):
    # 列表页显示的属性
    list_display = ["id","orderinfo","ogoods"]
    # 过滤条件
    list_filter = ["ogoods"]
    # 搜索框字段
    search_fields = ["orderinfo"]
    # 每页显示数据量
    list_per_page = 20
    # 修改页显示方式


admin.site.register(models.OrderInfo,OrderInfoAdmin)
admin.site.register(models.OrderGoods,OrderGoodsAdmin)