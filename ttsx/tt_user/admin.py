#coding=utf-8
from django.contrib import admin
import models

class UserAdmin(admin.ModelAdmin):
    list_display = ["id","uname","utel"]
    list_filter = ["isDelete"]
    search_fields = ["uname","ushou"]
    list_per_page = 20
    fieldsets = [("个人信息",{"fields":["uname","upwd","uemail","isDelete"]}),
                 ("收货地址",{"fields":["ushou","uadder","uyoubian","utel"]})]

admin.site.register(models.UserInfo,UserAdmin)

