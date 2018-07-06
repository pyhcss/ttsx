# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tt_goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='gliulan',
            field=models.IntegerField(default=0),
        ),
    ]
