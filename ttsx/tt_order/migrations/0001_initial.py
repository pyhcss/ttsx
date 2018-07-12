# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tt_goods', '0002_goods_gliulan'),
        ('tt_user', '0002_userinfo_isdelete'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ogrmb', models.DecimalField(max_digits=5, decimal_places=2)),
                ('ocount', models.IntegerField()),
                ('ogoods', models.ForeignKey(to='tt_goods.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('otime', models.DateTimeField(auto_now=True)),
                ('oispay', models.BooleanField(default=False)),
                ('ozrmb', models.DecimalField(max_digits=7, decimal_places=2)),
                ('oaddress', models.CharField(max_length=150)),
                ('ouser', models.ForeignKey(to='tt_user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='orderinfo',
            field=models.ForeignKey(to='tt_order.OrderInfo'),
        ),
    ]
