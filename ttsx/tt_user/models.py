#coding=utf-8
from django.db import models

# 定义用户数据库
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ushou = models.CharField(max_length=20,default="")
    uadder = models.CharField(max_length=100,default="")
    uyoubian = models.CharField(max_length=6,default="")
    utel = models.CharField(max_length=11,default="")
