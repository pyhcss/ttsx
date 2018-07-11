from django.db import models


class CartInfo(models.Model):
    cuser = models.ForeignKey('tt_user.UserInfo')
    cgoods = models.ForeignKey('tt_goods.Goods')
    count = models.IntegerField()