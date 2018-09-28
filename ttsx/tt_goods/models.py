# coding=utf-8
from django.db import models
from tinymce.models import HTMLField


class TypeGoods(models.Model):
    """商品类型模型类"""
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode("utf-8")


class Goods(models.Model):
    """商品模型类"""
    gname = models.CharField(max_length=30)
    gimg = models.ImageField(upload_to="tt_goods")
    grmb = models.DecimalField(max_digits=5,decimal_places=2)
    gdanwei = models.CharField(max_length=20)
    gjianjie = models.CharField(max_length=1000)
    gkucun = models.IntegerField()
    gjieshao = HTMLField()
    isDelete = models.BooleanField(default=False)
    typegoods = models.ForeignKey(TypeGoods)
    gliulan = models.IntegerField(default=0)

    def __str__(self):
        return self.gname.encode("utf-8")