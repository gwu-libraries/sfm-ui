# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0004_auto_20160509_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='credential',
            name='platform',
            field=models.CharField(help_text=b'Platform name', max_length=255, choices=[(b'twitter', b'Twitter'), (b'flickr', b'Flickr'), (b'weibo', b'Weibo')]),
        ),
        migrations.AlterField(
            model_name='export',
            name='status',
            field=models.CharField(default=b'not requested', max_length=20, choices=[(b'not requested', b'Not requested'), (b'requested', b'Requested'), (b'completed success', b'Success'), (b'completed failure', b'Failure')]),
        ),
        migrations.AlterField(
            model_name='harvest',
            name='parent_harvest',
            field=models.ForeignKey(related_name='child_harvests', blank=True, to='ui.Harvest', null=True),
        ),
        migrations.AlterField(
            model_name='harvest',
            name='status',
            field=models.CharField(default=b'requested', max_length=20, choices=[(b'requested', b'Requested'), (b'completed success', b'Success'), (b'completed failure', b'Failure'), (b'running', b'Running'), (b'stop requested', b'Stop requested')]),
        ),
        migrations.AlterField(
            model_name='historicalcredential',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalcredential',
            name='platform',
            field=models.CharField(help_text=b'Platform name', max_length=255, choices=[(b'twitter', b'Twitter'), (b'flickr', b'Flickr'), (b'weibo', b'Weibo')]),
        ),
        migrations.AlterField(
            model_name='historicalseedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, null=True, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, null=True, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
    ]
