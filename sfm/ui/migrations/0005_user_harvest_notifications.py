# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0004_auto_20161021_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='harvest_notifications',
            field=models.BooleanField(default=True),
        ),
    ]
