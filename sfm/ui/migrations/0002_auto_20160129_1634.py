# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seedset',
            name='max_count',
        ),
        migrations.AlterField(
            model_name='seedset',
            name='harvest_type',
            field=models.CharField(blank=True, max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'flickr_user', b'Flickr user')]),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks')]),
        ),
    ]
