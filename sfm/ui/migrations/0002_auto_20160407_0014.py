# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='name',
            field=models.CharField(default=b'Credential', max_length=50),
        ),
        migrations.AddField(
            model_name='historicalcredential',
            name='name',
            field=models.CharField(default=b'Credential', max_length=50),
        ),
        migrations.AlterField(
            model_name='credential',
            name='platform',
            field=models.CharField(max_length=255, choices=[(b'twitter', b'twitter'), (b'flickr', b'flickr'), (b'weibo', b'weibo'), (b'tumblr', b'tumblr')]),
        ),
        migrations.AlterField(
            model_name='historicalcredential',
            name='platform',
            field=models.CharField(max_length=255, choices=[(b'twitter', b'twitter'), (b'flickr', b'flickr'), (b'weibo', b'weibo'), (b'tumblr', b'tumblr')]),
        ),
        migrations.AlterField(
            model_name='historicalseedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks')]),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks')]),
        ),
    ]
