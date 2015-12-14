# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0002_auto_20151013_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seedset',
            name='end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='schedule',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
