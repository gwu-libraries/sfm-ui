# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_auto_20160901_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, null=True, verbose_name=b'schedule', choices=[(1, b'One time harvest'), (30, b'Every 30 minutes'), (60, b'Every hour'), (240, b'Every 4 hours'), (720, b'Every 12 hours'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
        migrations.AlterField(
            model_name='historicalcollection',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, null=True, verbose_name=b'schedule', choices=[(1, b'One time harvest'), (30, b'Every 30 minutes'), (60, b'Every hour'), (240, b'Every 4 hours'), (720, b'Every 12 hours'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
    ]
