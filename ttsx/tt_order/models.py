from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)
    otime = models.DateTimeField(auto_now=True)
    ouser = models.ForeignKey("tt_user.UserInfo")
    oispay = models.BooleanField(default=False)
    ozrmb = models.DecimalField(max_digits=7,decimal_places=2)
    oaddress = models.CharField(max_length=150)

    def __str__(self):
        return self.oid


class OrderGoods(models.Model):
    ogoods = models.ForeignKey("tt_goods.Goods")
    orderinfo = models.ForeignKey("OrderInfo")
    ogrmb = models.DecimalField(max_digits=5,decimal_places=2)
    ocount = models.IntegerField()
