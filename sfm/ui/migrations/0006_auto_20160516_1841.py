# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_auto_20160510_0621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='stats',
        ),
        migrations.RemoveField(
            model_name='harvest',
            name='stats',
        ),
        migrations.RemoveField(
            model_name='historicalcollection',
            name='stats',
        ),
        migrations.RemoveField(
            model_name='historicalseedset',
            name='stats',
        ),
        migrations.RemoveField(
            model_name='seedset',
            name='stats',
        ),
    ]
