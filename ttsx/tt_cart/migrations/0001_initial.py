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
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('cgoods', models.ForeignKey(to='tt_goods.Goods')),
                ('cuser', models.ForeignKey(to='tt_user.UserInfo')),
            ],
        ),
    ]
