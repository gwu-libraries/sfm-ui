# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0016_auto_20170523_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalcollection',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
