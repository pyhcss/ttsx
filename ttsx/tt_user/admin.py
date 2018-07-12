#coding=utf-8
from django.contrib import admin
import models

class UserAdmin(admin.ModelAdmin):
    # 列表页显示的属性
    list_display = ["id","uname","utel"]
    # 过滤条件
    list_filter = ["isDelete"]
    # 搜索框字段
    search_fields = ["uname","ushou"]
    # 每页显示数据量
    list_per_page = 20
    # 修改页显示方式
    fieldsets = [("个人信息",{"fields":["uname","upwd","uemail","isDelete"]}),
                 ("收货地址",{"fields":["ushou","uadder","uyoubian","utel"]})]

admin.site.register(models.UserInfo,UserAdmin)

