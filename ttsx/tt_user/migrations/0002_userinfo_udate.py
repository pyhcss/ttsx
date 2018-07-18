# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tt_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='udate',
            field=models.DateTimeField(default='1970-1-1 00:00', auto_now_add=True),
            preserve_default=False,
        ),
    ]
