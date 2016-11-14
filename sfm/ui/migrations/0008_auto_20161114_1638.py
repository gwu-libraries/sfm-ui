# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ui.models

class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0007_auto_20161114_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='credential_id',
            field=models.CharField(default=ui.models.default_uuid, unique=True, max_length=32),
        ),
    ]
