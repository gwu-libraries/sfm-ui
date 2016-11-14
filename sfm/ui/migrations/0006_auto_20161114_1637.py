# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import ui.models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_user_harvest_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='credential_id',
            field=models.CharField(default=ui.models.default_uuid, null=True, max_length=32),
        ),
        migrations.AddField(
            model_name='export',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 14, 21, 37, 16, 973833, tzinfo=utc), auto_now=True),
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
        migrations.AddField(
            model_name='historicalcredential',
            name='credential_id',
            field=models.CharField(default=ui.models.default_uuid, max_length=32, db_index=True),
        ),
        migrations.AlterField(
            model_name='export',
            name='status',
            field=models.CharField(default=b'not requested', max_length=20, choices=[(b'not requested', b'Not requested'), (b'requested', b'Requested'), (b'running', b'Running'), (b'completed success', b'Success'), (b'completed failure', b'Failure')]),
        ),
    ]
