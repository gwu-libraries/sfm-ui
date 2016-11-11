# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_auto_20161101_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='export',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 4, 18, 54, 9, 637584, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='export',
            name='host',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='export',
            name='instance',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='export',
            name='service',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='harvest',
            name='host',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='harvest',
            name='instance',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='harvest',
            name='service',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='export',
            name='status',
            field=models.CharField(default=b'not requested', max_length=20, choices=[(b'not requested', b'Not requested'), (b'requested', b'Requested'), (b'running', b'Running'), (b'completed success', b'Success'), (b'completed failure', b'Failure')]),
        ),
    ]
