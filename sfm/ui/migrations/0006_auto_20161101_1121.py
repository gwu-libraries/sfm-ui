# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ui.models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_user_harvest_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='credential_id',
            field=models.CharField(default=ui.models.default_uuid, unique=True, max_length=32),
        ),
        migrations.AddField(
            model_name='historicalcredential',
            name='credential_id',
            field=models.CharField(default=ui.models.default_uuid, max_length=32, db_index=True),
        ),
    ]
