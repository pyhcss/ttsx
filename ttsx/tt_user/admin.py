# coding=utf-8
import models
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    """自定义admin显示"""
    list_display = ["id","uname","udate"]               # 列表页显示的属性
    list_filter = ["isDelete"]                          # 过滤条件
    search_fields = ["uname","ushou"]                   # 搜索框字段
    list_per_page = 20                                  # 每页显示数据量
                                                        # 修改页显示方式
    fieldsets = [("个人信息",{"fields":["uname","upwd","uemail","isDelete"]}),
                 ("收货地址",{"fields":["ushou","uadder","uyoubian","utel"]})]

admin.site.register(models.UserInfo,UserAdmin)          # 注册自定义类

