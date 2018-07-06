# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gname', models.CharField(max_length=30)),
                ('gimg', models.ImageField(upload_to=b'tt_goods')),
                ('grmb', models.DecimalField(max_digits=5, decimal_places=2)),
                ('gdanwei', models.CharField(max_length=20)),
                ('gjianjie', models.CharField(max_length=1000)),
                ('gkucun', models.IntegerField()),
                ('gjieshao', tinymce.models.HTMLField()),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ttitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='typegoods',
            field=models.ForeignKey(to='tt_goods.TypeGoods'),
        ),
    ]
