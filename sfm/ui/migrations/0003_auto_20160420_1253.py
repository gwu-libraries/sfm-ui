# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0002_auto_20160407_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalseedset',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='seedset',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='historicalseedset',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalseedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
    ]
