# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_auto_20151202_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seedset',
            name='schedule',
        ),
        migrations.AddField(
            model_name='seedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks')]),
        ),
    ]
