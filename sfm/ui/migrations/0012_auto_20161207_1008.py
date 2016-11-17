# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0011_export_export_segment_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvest',
            name='status',
            field=models.CharField(default=b'requested', max_length=20, choices=[(b'requested', b'Requested'), (b'completed success', b'Success'), (b'completed failure', b'Failure'), (b'running', b'Running'), (b'stop requested', b'Stop requested'), (b'voided', b'Voided'), (b'skipped', b'Skipped')]),
        ),
    ]
